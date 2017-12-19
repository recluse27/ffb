import unittest
from unit_adapter import UnitAdapter


class TestUnit(unittest.TestCase):
    def setUp(self):
        self.widget = UnitAdapter(IAdapter)

    def checkout_test_len(self):
        self.assertNotEqual(len(self.checkout()), 0)

    def get_categories_test_len(self):
        self.assertEqual(len(self.get_categories()), 12)

    def get_products_test_len(self):
        self.assertNotEqual(len(self.get_products()), 0)

    def get_products_test_type(self):
        self.assertIsInstance(type(self.get_products()), list)

    def is_product_available(self):
        product_ids = []
        for product_id in product_ids:
            with self.subTest(i=product_id):
                self.assertTrue(self.is_product_available(i))
