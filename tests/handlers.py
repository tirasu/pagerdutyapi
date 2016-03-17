"""
Tests for logging pieces
"""
import logging.config
from contextlib import contextmanager
from unittest import TestCase

import pagerdutyapi


NOT_PROVIDED = object()


@contextmanager
def override_attribute(obj, attr_name, new_value):
    """Temporarily override attribute of specific object"""
    old_value = getattr(obj, attr_name, NOT_PROVIDED)
    setattr(obj, attr_name, new_value)
    yield
    if old_value is NOT_PROVIDED:
        delattr(obj, attr_name)
    else:
        setattr(obj, attr_name, old_value)


class PagerDutyLoggingHandlerTestCase(TestCase):
    """
    Test case for ``PagerDutyLoggingHandler`` logging handler class
    """
    def configure_logging_dict(self, **params):
        handler_config_dict = {
            'class': 'pagerdutyapi.handlers.PagerDutyHandler',
        }
        handler_config_dict.update(params)
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'pagerduty': handler_config_dict,
            },
            'loggers': {
                'fake_pd': {
                    'propagate': False,
                    'handlers': ['pagerduty'],
                },
            },
        })

    def test_initializing_handler_with_service_id_and_incident_key(self):
        """
        Try to initialize handler with service ID provided, check if it was
        saved for further use
        """
        intercepted = []

        def fake_create_trigger(**kwargs):
            intercepted.append(kwargs)

        service_id = 'ABCDEF'
        incident_key ='DEF123'
        message_template = '%s meets %s'
        args = ('Sally', 'Larry')

        # Configure logging and retrieve logger:
        self.configure_logging_dict(
            service_id=service_id,
            incident_key=incident_key,
        )
        logger = logging.getLogger('fake_pd')

        with override_attribute(
            pagerdutyapi, 'create_trigger', fake_create_trigger,
        ):
            logger.error(message_template, *args)

        self.assertEqual(
            intercepted,
            [
                {
                    'details': {},
                    'incident_key': incident_key,
                    'message': message_template % args,
                    'service_key': service_id,
                },
            ],
        )

    def test_determining_incident_key_based_on_message_template(self):
        """
        Check if called handler without incident key will cause it to be
        created based on the message template
        """
        intercepted = []

        def fake_create_trigger(**kwargs):
            intercepted.append(kwargs)

        service_id = 'ABCDEF'
        incident_key ='DEF123'
        message_template = '%s meets %s'
        args = ('Sally', 'Larry')

        # Configure logging and retrieve logger:
        self.configure_logging_dict(
            service_id=service_id,
        )
        logger = logging.getLogger('fake_pd')

        with override_attribute(
            pagerdutyapi, 'create_trigger', fake_create_trigger,
        ):
            logger.error(message_template, *args)

        self.assertEqual(
            intercepted,
            [
                {
                    'details': {},
                    'incident_key': message_template,
                    'message': message_template % args,
                    'service_key': service_id,
                },
            ],
        )

    def test_passing_incident_key_during_logging(self):
        """
        Check if called handler will respect incident key when passed to it
        during logging
        """
        intercepted = []

        def fake_create_trigger(**kwargs):
            intercepted.append(kwargs)

        service_id = 'ABCDEF'
        incident_key ='DEF123'
        message_template = '%s meets %s'
        args = ('Sally', 'Larry')

        # Configure logging and retrieve logger:
        self.configure_logging_dict(
            service_id=service_id,
        )
        logger = logging.getLogger('fake_pd')

        with override_attribute(
            pagerdutyapi, 'create_trigger', fake_create_trigger,
        ):
            logger.error(
                message_template,
                *args,
                extra={
                    'incident_key': incident_key,
                }
            )

        self.assertEqual(
            intercepted,
            [
                {
                    'details': {},
                    'incident_key': incident_key,
                    'message': message_template % args,
                    'service_key': service_id,
                },
            ],
        )
