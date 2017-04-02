import logging
from esser.handlers import handle_event, handle_stream
from items.aggregate import Item
from basket.aggregate import Basket

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def on_event_received(event, context):
    try:
        event = handle_event(event, context)
        return event.event_data.as_dict()
    except Exception as exc:
        log.exception('Event: %s', event)
        log.exception('Exception: %s', exc)


def on_event_saved(event, context):
    return handle_stream(event, context)


def route(event, context):
    if 'EventName' in event:
        event = on_event_received(event, context)
        log.info(event)
        return event
    else:
        aggregates = on_event_saved(event, context)
        log.info(aggregates)
        return aggregates
