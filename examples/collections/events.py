from esser.events import BaseEvent, CreateEvent, DeleteEvent


class CollectionCreated(CreateEvent):

    schema = {
        'name': {'type': 'string'}
    }


class ItemAdded(BaseEvent):

    schema = {
        'aggregate_id': {'type': 'string'}
    }
