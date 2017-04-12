from esser.commands import BaseCommand, CreateCommand, DeleteCommand


class CreateItem(CreateCommand):

    event_name = 'ItemCreated'
    schema = {
        'name': {'type': 'string'},
        'price': {'type': 'float'}
    }


class UpdatePrice(BaseCommand):

    event_name = 'PriceUpdated'
    schema = {
        'price': {'type': 'float', 'diff': True}
    }


class AddColors(BaseCommand):

    event_name = 'ColorsAdded'
    schema = {
        'colors': {
            'type': 'set',
            'allowed': ['orange', 'black', 'white', 'blue', 'green']
        }
    }


class DeleteItem(DeleteCommand):

    schema = {
        'deleted_by': {'type': 'string'}
    }
