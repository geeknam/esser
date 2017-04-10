from mock import patch
from esser.exceptions import AggregateDoesNotExist
from examples.items.aggregate import Item
from tests.base import BaseTestCase


class EntityTestCase(BaseTestCase):

    def setUp(self):
        super(EntityTestCase, self).setUp()
        self.item = Item()

    def test_aggregate_name(self):
        self.assertEquals(self.item.aggregate_name, 'Item')

    def test_set_price(self):
        self.item.created.save(
            attrs={'name': 'Yummy Choc', 'price': 10.50}
        )
        self.item.price = 12.50
        self.assertEquals(self.item.price, 12.50)

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
        self.assertEquals(event.aggregate_id, '2-higher')
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
            len(list(self.item.repository.get_all_events())), 2
        )
        Item().created.save(
            attrs={'name': 'Pizza', 'price': 15.50}
        )
        self.assertEquals(
            len(list(self.item.repository.get_all_events())), 2
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
