import unittest
from esser.repositories.models import DynamoDBEventModel, Snapshot


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        DynamoDBEventModel.create_table(
            read_capacity_units=1, write_capacity_units=1
        )
        Snapshot.create_table(
            read_capacity_units=1, write_capacity_units=1
        )

    def tearDown(self):
        DynamoDBEventModel.delete_table()
        Snapshot.delete_table()
