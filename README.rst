================
``pagerdutyapi``
================

Very basic wrapper for PagerDuty API

Current functionality:

- create trigger for known service key, with incident key,
- handle all documented errors,
- attach context (links, images) to trigger,
- logging functionality to send alerts to PagerDuty facilities,
- ability to add logging handler configurable from config dict,

TODO:

- write tests for the above,
- write examples on how it is done,

Possible further features:

- other functionality (not only sending alerts, but also reading/changing other
  resources),
- convenience shortcuts for various frameworks,
- make ``pagerdutyapi`` do not have dependencies except ``six``,

---------------------
Logging configuration
---------------------

Logging configuration can make use of this module. Sample dict config could
look like this::

    {
        'version': 1,
        'handlers': {
            'pagerduty': {
                'class': 'pagerdutyapi.handlers.PagerDutyHandler',
                'service_id': 'YOUR_SERVICE_ID',
                'level': 'ERROR',  # process only errors
            },
        },
        'loggers': {
            'pd_logger': {
                'propagate': True,  # call other loggers
                'handlers': ['pagerduty'],
            },
        },
    }

And then you could use it like this::

    import logging

    logger = logging.getLogger('pd_logger')
    logger.error(
        'Error level on instance %s above threshold: %s',
        instance_id,
        current_level,
    )

where ``instance_id`` and ``current_level`` are some variables.

By default the incident will be created based on the template message (in this
case "``Error level on instance %s above threshold: %s``"), so it is important
to pass variable parts as positional arguments to logging method.

Alternatively you could pass ``incident_key`` specifically as part of ``extra``
param during logging call::

    logger.error(
        'Error level on instance %s above threshold: %s',
        instance_id,
        current_level,
        extra={
            'incident_key': 'THRESHOLD_ALERTS_INSTANCE_{}'.format(instance_id),
        },
    )

You can also override incident key during handler configuration::

    {
        ...
        'handlers': {
            'pagerduty': {
                'class': 'pagerdutyapi.handlers.PagerDutyHandler',
                'service_id': 'YOUR_SERVICE_ID',
                'incident_key': 'YOUR_INCIDENT_KEY',  # override incident keys
                'level': 'ERROR',  # process only errors
            },
        },
        ...
    }

This way, incident keys will be overwritten for all logging calls.
