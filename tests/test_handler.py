import unittest
from mock import patch
from esser.handlers import handle_event
from esser.models import Event
from examples.items.aggregate import Item


class HandlerTestCase(unittest.TestCase):

    def setUp(self):
        Event.create_table(
            read_capacity_units=1, write_capacity_units=1
        )
        self.item = Item()

    def tearDown(self):
        Event.delete_table()

    @patch('uuid.uuid4')
    def test_handler(self, mock_uuid):
        mock_uuid.return_value = 'mykey'
        event = {
            'EventName': 'ItemCreated',
            'AggregateId': None,
            'AggregateClassPath': 'examples.items.aggregate.Item',
            'Payload': {
                'name': 'Handler Item',
                'price': 15.0
            }
        }
        result = handle_event(event, {})
        self.assertEquals(result.aggregate_id, 'mykey:1')
        event = {
            'EventName': 'PriceUpdated',
            'AggregateId': 'mykey',
            'AggregateClassPath': 'examples.items.aggregate.Item',
            'Payload': {'price': 12.0}
        }
        result = handle_event(event, {})
        self.assertEquals(result.aggregate_id, 'mykey:2')
