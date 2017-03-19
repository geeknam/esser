from esser.events import BaseEvent, CreateEvent, DeleteEvent


class ItemCreated(CreateEvent):

    schema = {
        'name': {'type': 'string'},
        'price': {'type': 'float'}
    }


class PriceUpdated(BaseEvent):

    schema = {
        'price': {'type': 'float'}
    }


class Deleted(DeleteEvent):

    schema = {
        'deleted_by': {'type': 'string'}
    }
