import unittest
import libmarvin
import libmarvin.settingsloader as settings
from libmarvin import util
import logging

class PizzaTest(unittest.TestCase):

    pizza_order = None

    def setUp(self):
        self.pizza_order = util.plugin("pizzaplugin")
        logging.info(self.pizza_order.requirements.requirements)

    def test_order_start(self):
        t = self.pizza_order.order_pizza()
        self.assertEqual(t, ", Which pizza would you like to order?")
        logging.info("requirements: %s " % self.pizza_order.requirements.requirements)
        t = self.pizza_order.order_pizza(pizza_name="Cacciatore")
        self.assertEqual(t, "You have selected {value}, What is the address?")
        t = self.pizza_order.order_pizza(address="22 wisconsin street")
        self.assertEqual(t, "Address set to: {address}, How would you like to pay")
        t = self.pizza_order.order_pizza(payment_method="cash")
        self.assertEqual(t, "Payment method: {payment_method}, Please confirm your order.")
        t = self.pizza_order.order_pizza(confirm=True)
        self.assertEqual(t, "Your order is complete")

    def test_order_start_then_cancel(self):
        t = self.pizza_order.order_pizza()
        self.assertEqual(t, ", Which pizza would you like to order?")
        logging.info("requirements: %s " % self.pizza_order.requirements.requirements)
        t = self.pizza_order.order_pizza(pizza_name="Cacciatore")
        self.assertEqual(t, "You have selected {value}, What is the address?")
        t = self.pizza_order.order_pizza(address="22 wisconsin street")
        self.assertEqual(t, "Address set to: {address}, How would you like to pay")
        t = self.pizza_order.order_pizza(payment_method="cash")
        self.assertEqual(t, "Payment method: {payment_method}, Please confirm your order.")
        t = self.pizza_order.order_pizza(cancel=True)
        self.assertEqual(t, "Order cancelled")
