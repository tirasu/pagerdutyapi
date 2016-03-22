"""
Library for connecting to PagerDuty

@version: 0.1.0
@author: Tomasz Jaskowski
@contact: http://github.com/tadeck
@license: MIT
"""
import json
import requests

from .contexts import PagerDutyContext
from .exceptions import (
    RequestRejected, ServerError, TooManyApiCalls, UnknownPagerDutyApiError,
)


_EVENTS_URL = (
    'https://events.pagerduty.com/generic/2010-04-15/create_event.json'
)


def create_trigger(
    service_key,
    incident_key,
    message,
    client=None,
    client_url=None,
    details=None,
    contexts=None,
):
    """
    Create trigger in PagerDuty API. Triggers are events that, if provided for
    incident key that is currently not assigned to any ongoing event (eg. all
    previous incidents with this incident key have been resolved), or provided
    without any incident key, will cause escalation policy to be triggered and
    someone will probably be called. Triggers for incident key that is ongoing
    issue (has already been triggered and not resolved) will be appended to
    existing incident.
    :param service_key: service key, as provided in PagerDuty settings
    :type service_key: str or unicode
    :param incident_key: identifier of incident, if available
    :type incident_key: str or unicode
    :param message: message that will be spoken through phone (max 1024 chars)
    :type message: str or unicode
    :param client: name of the client who created error
    :type client: str or unicode
    :param client_url: location of the client
    :type client_url: str or unicode
    :param details: more data about specific incident occurrence
    :type details: dict
    :param contexts: list of contexts (images, links) attached to report
    :type contexts: list
    :return: response from PagerDuty
    :rtype: dict
    """
    if len(message) > 1024:
        raise ValueError('Message is too long to be passed to PagerDuty')

    payload = {
        'service_key': service_key,
        'event_type': 'trigger',
        'description': message,
    }

    if incident_key is not None:
        payload['incident_key'] = incident_key

    if client is not None:
        payload['client'] = client

    if client_url is not None:
        payload['client_url'] = client_url

    if details is not None:
        payload['details'] = details

    if contexts is not None:
        parsed_contexts = []
        for context in parsed_contexts:
            assert isinstance(context, PagerDutyContext)
            parsed_contexts.append(context.to_dict())
        payload['contexts'] = parsed_contexts

    response = requests.post(
        _EVENTS_URL,
        data=json.dumps(payload),
        headers={'content-type': 'application/json'},
    )

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        raise RequestRejected(response.json())
    elif response.status_code == 403:
        raise TooManyApiCalls()
    elif response.status_code >= 500:
        raise ServerError(response.status_code)
    else:
        raise UnknownPagerDutyApiError(
            status_code=response.status_code,
            details=response.json(),
        )
