from mock import patch
from tests.base import BaseTestCase
from esser.handlers import handle_event
from examples.items.aggregate import Item


class HandlerTestCase(BaseTestCase):

    def setUp(self):
        super(HandlerTestCase, self).setUp()
        self.item = Item()

    @patch('uuid.uuid4')
    def test_handler(self, mock_uuid):
        mock_uuid.return_value = 'mykey'
        event = {
            'EventName': 'ItemCreated',
            'AggregateId': None,
            'AggregateName': 'Item',
            'Payload': {
                'name': 'Handler Item',
                'price': 15.0
            }
        }
        result = handle_event(event, {})
        self.assertEquals(result.aggregate_id, 'mykey')
        self.assertEquals(result.version, 1)
        event = {
            'EventName': 'PriceUpdated',
            'AggregateId': 'mykey',
            'AggregateName': 'Item',
            'Payload': {'price': 12.0}
        }
        result = handle_event(event, {})
        self.assertEquals(result.aggregate_id, 'mykey')
        self.assertEquals(result.version, 2)
