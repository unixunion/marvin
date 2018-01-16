import inspect
import unittest

from libmarvin.requirements import Requirement
from libmarvin.requirements import Requirements
from libmarvin.util import get_key_from_kwargs


class UtilTest(unittest.TestCase):

    requirements = Requirements()
    kwargs = {}

    def setUp(self):
        # first we set all the requirements to with thier value to None
        self.requirements.new_requirement("pizza_name", "Which pizza would you like to order?", "You have selected %s", None)
        self.requirements.new_requirement("address", "What is the address?", "Address set to: %s", None)
        self.requirements.new_requirement("payment_method", "How would you like to pay", "Payment method: %s", None)
        self.requirements.new_requirement("confirm", "Please confirm your order: %s", "Order confirmed", None)
        self.requirements.new_requirement("cancel", "Would you like to cancel?", "Order cancelled", None, auto_prompt=False)
        self.kwargs["nothing"] = "here"

    def test_cancel_order(self):
        self.requirements.get_requirement("cancel").set(True)
        self.assertEqual(self.requirements.get_requirement("cancel").value, True)
        self.assertEqual(self.requirements.get_requirement("cancel").set_msg, "Order cancelled")

    def test_order_pizza_cancel(self, order_pizza=True, cancel=True):
        # check if this is a cancelation
        if get_key_from_kwargs("cancel", self.kwargs, is_optional=True):
            self.requirements.requirements["cancel"].set("false")

        if self.requirements.get_requirement("cancel").value:
            return self.requirements.get_requirement("cancel").set_msg

        self.assertEqual("never get here", None)

    def test_order_pizza_req1(self, *args, **kwargs):

        # mimic a kwarg called pizza_name
        kwargs["pizza_name"] = "Chicken Pizza"

        # a place to store final requirement name for unittest
        requirement_name = None

        for requirement in self.requirements.requirements: # type: Requirement
            # if the requirement has no value, we check for if kwargs set it
            if not requirement.value:
                print("examing unmet requirement: %s" % requirement.name)
                if requirement.name in kwargs:
                    print("requirement kwarg: %s is passed" % requirement.name)
                    requirement_name = requirement.name
                else:
                    print("%s not in kw: %s" % (requirement.name, kwargs))
        self.assertEqual(requirement_name, "pizza_name")

    def test_requirements(self):
        requirements = Requirements()
        requirements.new_requirement("req1", "req1_unset_msg", "req1_set_msg %(req1)s", "req1_value")
        requirements.new_requirement("req2", "req2_unset_msg", "req2_set_msg", False)
        requirements.new_requirement("req3", "req3_unset_msg", "req3_set_msg", True)

        self.assertIsInstance(requirements.requirements[0], Requirement)
        self.assertEqual(requirements.requirements[0](), "req1_value")
        self.assertEqual(requirements.requirements[1](), False)

        requirements.requirements[1].set(True)
        self.assertEqual(requirements.requirements[1](), True)

        self.assertEqual(requirements.is_confirmed(), False)

        self.assertEqual(requirements.get_requirement("req1").value, "req1_value")
        with self.assertRaises(KeyError):
            self.assertEqual(requirements.get_requirement("reqz").value, "req1_value")


    def test_requirement(self):
        requirement = Requirement("name", "unset_msg", "set_msg", "value")
        self.assertEqual(requirement.get(), {'name': 'name', 'unset_msg': 'unset_msg', 'set_msg':'set_msg', 'value': 'value', 'auto_prompt': True} )
        self.assertEqual(requirement.name,"name")
        self.assertEqual(requirement.unset_msg, "unset_msg")
        self.assertEqual(requirement.set_msg, "set_msg")
        self.assertEqual(requirement.value, "value")

    def test_requirements_get(self):
        set_requirement={}
        set_requirement["cancel"] = Requirement("cancel", "Would you like to cancel?", "Order cancelled", False, auto_prompt=False)
        set_requirement["is_cancel"] = Requirement("cancel", "Would you like to cancel?", "Order cancelled", False, auto_prompt=False)

        self.assertEqual(set_requirement["cancel"](), False)
        set_requirement["is_cancel"].value = True

        self.assertEqual(set_requirement["is_cancel"](), True)