from esser.commands import (
    BaseCommand, CreateCommand
)
from items.aggregate import Item


class CreateBasket(CreateCommand):

    event_name = 'BasketCreated'
    schema = {
        'name': {'type': 'string'}
    }


class AddItem(BaseCommand):

    event_name = 'ItemAdded'
    schema = {
        'aggregate_id': {'type': 'string'}
    }


class AddItemWithExistanceValidation(BaseCommand):

    event_name = 'ItemAdded'
    related_aggregate = Item
    schema = {
        'aggregate_id': {
            'type': 'string',
            'aggregate_exists': True
        }
    }


class AddItemWithProjection(BaseCommand):

    event_name = 'ItemAddedWithProjection'
    related_aggregate = Item
    schema = {
        'aggregate_id': {'coerce': 'project'}
    }
