import unittest
import mock

from esser.models import Event
from esser.exceptions import EventValidationException, IntegrityError

from examples.entities import Item


class EventTestCase(unittest.TestCase):

    def setUp(self):
        Event.create_table(
            read_capacity_units=1, write_capacity_units=1
        )
        self.item = Item()

    def tearDown(self):
        Event.delete_table()

    def test_create(self):
        self.item.created.save(
            attrs={'name': 'Yummy Choc', 'price': 10.50}
        )
        self.assertEquals(
            self.item.current_state,
            {'name': 'Yummy Choc', 'price': 10.50}
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
        with self.assertRaises(EventValidationException):
            self.item.price_updated.save(attrs={'price': 12.50})

    def test_delete(self):
        self.item.created.save(
            attrs={'name': 'Yummy Choc', 'price': 10.50}
        )
        self.item.deleted.save(attrs={'deleted_by': 'John'})
        # self.item.price_updated.save(
        #     aggregate_id=event.guid,
        #     attrs={'price': 12.50}
        # )
        self.assertEquals(self.item.current_state, None)

    def test_validation(self):
        with self.assertRaises(EventValidationException):
            self.item.created.save(
                attrs={'name': 'Yummy Choc', 'price': '10.50'}
            )
        with self.assertRaises(EventValidationException):
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
        with self.assertRaises(IntegrityError):
            self.item.created.save(
                attrs={'name': 'Bubble gum', 'price': 11.50}
            )
