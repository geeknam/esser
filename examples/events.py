from esser.events import BaseEvent, CreateEvent, DeleteEvent


class ItemCreated(CreateEvent):

    schema = {
        'name': {'type': 'string'},
        'price': {'type': 'float'}
    }


class PriceUpdated(BaseEvent):

    schema = {
        'price': {'type': 'float', 'diff': True}
    }


class ColorsAdded(BaseEvent):

    schema = {
        'colors': {
            'type': 'set',
            'allowed': ['orange', 'black', 'white', 'blue', 'green']
        }
    }


class Deleted(DeleteEvent):

    schema = {
        'deleted_by': {'type': 'string'}
    }
