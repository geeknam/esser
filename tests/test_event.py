import unittest
import mock

from esser.repositories.models import Event
from esser import exceptions

from examples.items.aggregate import Item
from examples.collections.aggregate import Collection


class EventTestCase(unittest.TestCase):

    def setUp(self):
        Event.create_table(
            read_capacity_units=1, write_capacity_units=1
        )
        self.item = Item()
        self.collection = Collection()

    def tearDown(self):
        Event.delete_table()

    def test_create(self):
        self.item.created.save(
            attrs={'name': 'Yummy Choc', 'price': 10.50}
        )
        self.assertEquals(
            self.item.current_state,
            {'name': 'Yummy Choc', 'price': 10.50, 'latest_version': 1}
        )

    def test_price_update(self):
        self.item.created.save(
            attrs={
                'name': 'Yummy Choc',
                'price': 10.50
            }
        )
        self.item.price_updated.save(attrs={'price': 12.50})
        self.assertEquals(
            self.item.current_state,
            {'name': 'Yummy Choc', 'price': 12.50, 'latest_version': 2}
        )
        with self.assertRaises(exceptions.EventValidationException):
            self.item.price_updated.save(attrs={'price': 12.50})

    def test_delete(self):
        self.item.created.save(
            attrs={'name': 'Yummy Choc', 'price': 10.50}
        )
        self.item.deleted.save(attrs={'deleted_by': 'John'})
        with self.assertRaises(exceptions.AggregateDeleted):
            self.item.current_state

    def test_validation(self):
        with self.assertRaises(exceptions.EventValidationException):
            self.item.created.save(
                attrs={'name': 'Yummy Choc', 'price': '10.50'}
            )
        with self.assertRaises(exceptions.EventValidationException):
            self.item.created.save(
                attrs={
                    'name': 'Yummy Choc', 'price': 10.50,
                    'foo': 'bar'
                }
            )

    @mock.patch('uuid.uuid4')
    def test_save_integrity(self, mock_uuid):
        mock_uuid.return_value = 'notunique'
        self.item.created.save(
            attrs={'name': 'Yummy Choc', 'price': 10.50}
        )
        with self.assertRaises(exceptions.IntegrityError):
            self.item.created.save(
                attrs={'name': 'Bubble gum', 'price': 11.50}
            )

    def test_composition(self):
        self.collection.created.save(attrs={'name': 'Favorite Food'})
        event = self.item.created.save(
            attrs={
                'name': 'Yummy Choc',
                'price': 10.50
            }
        )
        self.collection.item_added.save(
            attrs={'aggregate_id': event.aggregate_id}
        )
        self.assertEquals(
            self.collection.current_state,
            {
                'items': [
                    {'latest_version': 1, 'name': 'Yummy Choc', 'price': 10.5}
                ],
                'latest_version': 2,
                'name': 'Favorite Food'
            }
        )

    def test_composition_invalid_id(self):
        self.collection.created.save(attrs={'name': 'Favorite Food'})
        self.collection.item_added.save(attrs={'aggregate_id': 'incorrectid'})
        self.assertEquals(
            self.collection.current_state,
            {'items': [{}], 'latest_version': 2, u'name': u'Favorite Food'}
        )
        with self.assertRaises(exceptions.EventValidationException):
            self.collection.item_added_with_validation.save(
                attrs={'aggregate_id': 'incorrectid'}
            )
