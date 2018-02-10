"""
Logging support for PagerDuty handlers
"""
import logging

import six

import pagerdutyapi


if six.PY3:
    PRIMITIVE_TYPES = (None.__class__, bool, int, float, bytearray, str)
else:
    PRIMITIVE_TYPES = (None.__class__, bool, int, float, str, unicode)

NOT_PROVIDED = object()


class PagerDutyHandler(logging.Handler):
    """
    Handler using PagerDuty for reporting issues
    """
    def __init__(self, service_id, incident_key=NOT_PROVIDED, **kwargs):
        self.service_id = service_id
        self.incident_key = incident_key
        super(PagerDutyHandler, self).__init__(**kwargs)

    def stringify_details(self, details):
        if isinstance(details, PRIMITIVE_TYPES):
            # no change needed, will be easily serialized
            return details

        elif isinstance(details, (list, tuple)):
            return details.__class__(
                self.stringify_details(item)
                for item in details
            )

        elif isinstance(details, dict):
            return {
                key: self.stringify_details(value)
                for key, value in details.items()
            }

        else:
            # Just string representation
            # TODO: Consider all issues that could occur here:
            return u'{}'.format(details)

    def emit(self, record):
        """
        Emit message to PagerDuty
        :param record: record that needs to be passed to PagerDuty
        :type record: LogRecord
        """
        assert isinstance(record, logging.LogRecord)

        default_attr_names = [
            name for name
            in dir(logging.LogRecord(None, None, "", 0, "", (), None, None))
        ]
        extra_details = {
            attr_name: getattr(record, attr_name)
            for attr_name in dir(record)
            if attr_name not in default_attr_names and
            attr_name not in ('incident_key',)
        }

        if record.exc_info:
            # This is an error case - need to add more information about it
            exc_class, exc_args, trace = record.exc_info
            if six.PY3:
                extra_details['error'] = repr(exc_args)
            else:
                extra_details['error'] = repr(exc_class(*exc_args))

        incident_key = self.incident_key
        if incident_key is NOT_PROVIDED:
            incident_key = getattr(
                record,
                'incident_key',
                record.msg,  # Message template is pretty good incident key
            )

        pagerdutyapi.create_trigger(
            service_key=self.service_id,
            incident_key=incident_key,
            message=record.getMessage(),
            details=self.stringify_details(extra_details),
        )
