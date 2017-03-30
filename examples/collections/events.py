from esser.events import (
    BaseEvent, CreateEvent
)
from examples.items.aggregate import Item


class CollectionCreated(CreateEvent):

    schema = {
        'name': {'type': 'string'}
    }


class ItemAdded(BaseEvent):

    schema = {
        'aggregate_id': {'type': 'string'}
    }


class ItemAddedWithExistanceValidation(BaseEvent):

    related_aggregate = Item

    schema = {
        'aggregate_id': {
            'type': 'string',
            'aggregate_exists': True
        }
    }

    @property
    def event_name(self):
        return 'ItemAdded'


class ItemAddedWithProjection(BaseEvent):

    related_aggregate = Item

    schema = {
        'aggregate_id': {'coerce': 'project'}
    }
