import unittest
from mock import patch
from esser.models import Event
from esser.exceptions import AggregateDoesNotExist
from examples.items.aggregate import Item


class EntityTestCase(unittest.TestCase):

    def setUp(self):
        Event.create_table(
            read_capacity_units=1, write_capacity_units=1
        )
        self.item = Item()

    def tearDown(self):
        Event.delete_table()

    def test_aggregate_name(self):
        self.assertEquals(self.item.aggregate_name, 'Item')

    def test_get_events(self):
        with patch('uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = '2-higher'
            event = self.item.created.save(
                attrs={'name': 'Yummy Choc', 'price': 10.50}
            )
            self.item.price_updated.save(attrs={'price': 12.50})
            self.item.price_updated.save(attrs={'price': 14.50})
        with patch('uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = '1-lower'
            Item().created.save(
                attrs={'name': 'Donut', 'price': 5.50}
            )
        self.assertEquals(event.guid, '2-higher')
        self.assertEquals(
            self.item.get_state_at(version=2),
            {'name': 'Yummy Choc', 'price': 12.50, 'latest_version': 2}
        )

    def test_get_all_events(self):
        self.item.created.save(
            attrs={'name': 'Yummy Choc', 'price': 10.50}
        )
        self.item.price_updated.save(attrs={'price': 12.50})
        self.assertEquals(
            len(list(self.item.get_all_events())), 2
        )
        Item().created.save(
            attrs={'name': 'Pizza', 'price': 15.50}
        )
        self.assertEquals(
            len(list(self.item.get_all_events())), 2
        )

    def test_get_last_aggregate_version(self):
        self.item.created.save(
            attrs={'name': 'Yummy Choc', 'price': 10.50}
        )
        self.assertEquals(
            self.item.get_last_aggregate_version(), 1
        )
        self.item.price_updated.save(attrs={'price': 12.50})
        self.assertEquals(
            self.item.get_last_aggregate_version(), 2
        )

    def test_get_last_aggregate_version_does_not_exist(self):
        with self.assertRaises(AggregateDoesNotExist):
            Item(aggregate_id='someuuid').get_last_aggregate_version()
