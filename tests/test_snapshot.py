import unittest

from esser.models import Event, Snapshot
from examples.entities import Item


class SnapshotTestCase(unittest.TestCase):

    def setUp(self):
        Event.create_table(
            read_capacity_units=1, write_capacity_units=1
        )
        Snapshot.create_table(
            read_capacity_units=1, write_capacity_units=1
        )
        self.item = Item()

    def tearDown(self):
        Event.delete_table()
        Snapshot.delete_table()

    def test_from_aggregate(self):
        self.item.created.save(
            attrs={'name': 'Yummy Choc', 'price': 10.50}
        )
        self.item.price_updated.save(attrs={'price': 12.50})
        snapshot = Snapshot.from_aggregate(self.item)
        self.assertEquals(
            snapshot.state.attribute_values,
            {'name': 'Yummy Choc', 'price': 12.50, 'latest_version': 2}
        )
