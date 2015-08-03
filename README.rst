================
``pagerdutyapi``
================

Very basic wrapper for PagerDuty API

Current functionality:

- create trigger for known service key, with incident key,
- handle all documented errors,
- attach context (links, images) to trigger,

TODO:

- build functionality to send alerts to PagerDuty facilities,
- write tests for the above,
- add logging handler configurable from config dict,
- write examples on how it is done,

Possible further features:

- other functionality (not only sending alerts, but also reading/changing other
  resources),
- convenience shortcuts for various frameworks,
- make ``pagerdutyapi`` do not have dependencies except ``six``,
