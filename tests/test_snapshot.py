from tests.base import BaseTestCase
from esser.repositories.dynamodb.models import Snapshot
from examples.items.aggregate import Item


class SnapshotTestCase(BaseTestCase):

    def setUp(self):
        super(SnapshotTestCase, self).setUp()
        self.item = Item()

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
