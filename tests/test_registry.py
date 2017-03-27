import unittest

from esser.registry import register, registry


class RegistryTestCase(unittest.TestCase):

    def test_register(self):

        @register
        class TestAggregate(object):
            pass

        self.assertEquals(
            registry.get_path('TestAggregate'),
            'tests.test_registry.TestAggregate'
        )

