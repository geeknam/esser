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
                        "SequenceNumber": "111",
                        "SizeBytes": 26,
                        "StreamViewType": "KEYS_ONLY"
                    },
                    "eventSourceARN": "stream-ARN"
                }
            ]
        }

    def test_handle_stream(self):
        with patch('uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = 'mockuuid'
            self.item.created.save(
                attrs={
                    'name': 'Yummy Choc',
                    'price': 10.50
                }
            )
        event = self.item.price_updated.save(attrs={'price': 12.50})
        stream = self.stream_factory('Item', event.aggregate_key)
        aggregates = handle_stream(stream, {})
        self.assertEquals(
            aggregates,
            {
                'Item': {
                    'mockuuid': {
                        'name': 'Yummy Choc', 'price': 12.50,
                        'latest_version': 2
                    }
                }
            }
        )
