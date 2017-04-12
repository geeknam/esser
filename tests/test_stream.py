from mock import patch
from tests.base import BaseTestCase
from examples.items.aggregate import Item
from esser.handlers import handle_stream


class StreamTestCase(BaseTestCase):

    def setUp(self):
        super(StreamTestCase, self).setUp()
        self.item = Item()

    def stream_factory(self, aggregate_name, aggregate_key):
        return {
            "Records": [
                {
                    "eventID": "1",
                    "eventName": "INSERT",
                    "eventVersion": "1.0",
                    "eventSource": "aws:dynamodb",
                    "awsRegion": "us-east-1",
                    "dynamodb": {
                        "Keys": {
                            "aggregate_name": {
                                "S": aggregate_name
                            },
                            "aggregate_key": {
                                "S": aggregate_key
                            }
                        },
                        'NewImage': {
                            'created_at': {'S': '2017-04-12T06:56:06.191104+0000'},
                            'aggregate_name': {'S': 'Item'},
                            'aggregate_key': {'S': '83e7b629-58a0-4194-80e4-dab5dbbd63c1:1'},
                            'event_type': {'S': 'ItemCreated'},
                            'event_data': {
                                'S': '{"price": 15, "name": "Coffee"}'
                            }
                        },
                        "SequenceNumber": "111",
                        "SizeBytes": 26,
                        "StreamViewType": "KEYS_ONLY"
                    },
                    "eventSourceARN": "stream-ARN"
                }
            ]
        }

    @patch('examples.items.receivers.handle_event_saved')
    def test_handle_stream(self, mock_handle):
        with patch('uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = 'mockuuid'
            self.item.created.save(
                attrs={
                    'name': 'Yummy Choc', 'price': 10.50
                }
            )
        event = self.item.price_updated.save(attrs={'price': 12.50})
        stream = self.stream_factory('Item', event.aggregate_key)
        handle_stream(stream, {})
