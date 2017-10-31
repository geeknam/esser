from mock import patch
import json
from tests.base import BaseTestCase
from examples.items.aggregate import Item
from esser.handlers import handle_stream


class StreamTestCase(BaseTestCase):

    def setUp(self):
        super(StreamTestCase, self).setUp()
        self.item = Item()

    def stream_factory(self, event):
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
                                "S": event.aggregate_name
                            },
                            "aggregate_key": {
                                "S": event.aggregate_key

                            }
                        },
                        'NewImage': {
                            'created_at': {'S': event.created_at.isoformat()},
                            'aggregate_name': {'S': event.aggregate_name},
                            'aggregate_key': {'S': event.aggregate_key},
                            'event_type': {'S': event.event_type},
                            'event_data': {
                                'S': json.dumps(event.event_data)
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
        stream = self.stream_factory(event)
        handle_stream(stream, {})
