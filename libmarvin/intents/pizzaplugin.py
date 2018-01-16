import difflib

from libmarvin import Plugin
import libmarvin
import logging

from libmarvin.requirements import Requirements, Requirement
from libmarvin.util import get_key_from_kwargs


@libmarvin.plugin_registry.register
class PizzaPlugin(Plugin):
    plugin_name = "pizzaplugin"
    args = None
    kwargs = None
    requirements = None


    def __init__(self, *args, **kwargs):
        logging.info("Instantiating %s" % self)
        self.args = args
        self.kwargs = kwargs
        self.requirements = Requirements() # type:Requirements

        # first we set all the requirements to with thier value to None
        self.requirements.new_requirement("menu", "The options are: {options}",
                                          "You have selected pizza: {value}",
                                          None, auto_prompt=False,
                                          options=["Cacciatore", "Mexican", "Taco", "Fish"])
        self.requirements.new_requirement("pizza_name", "Which pizza would you like to order?", "You have selected {value}", None)
        self.requirements.new_requirement("address", "What is the address?", "Address set to: {value}", None)
        self.requirements.new_requirement("payment_method", "How would you like to pay",
                                          "Payment method: {value}",
                                          None,
                                          options=["Cash", "Card"])
        self.requirements.new_requirement("confirm", "Please confirm your order.", "Order confirmed", None)
        self.requirements.new_requirement("cancel", "Would you like to cancel?", "Order cancelled", None, auto_prompt=False)

        # this plugin locks a user into a dialog session, so lets set that.
        self.context_locking = True
        self.lock_session_default_method = self.order_pizza

        logging.info("Completed Instantiation")

    # async def begin_session(self, *args, **kwargs):
        

    async def order_pizza(self, *args, **kwargs):
        # message_object = get_key_from_kwargs('message_object', kwargs)  # type: discord.Message

        if self.is_context_locking() and not self.is_locking_session():
            self.set_locking_session(True)
            return "Welcome to penuci's pizza!, I am pizzabot!"

        response = ""

        # check if this is a help request
        if get_key_from_kwargs("help", kwargs, default=False, is_optional=True):
            return self.help()

        # check if this is a cancelation
        if get_key_from_kwargs("cancel", kwargs, default=False, is_optional=True):
            # self.requirements.requirements["cancel"].set(True)
            self.requirements.get_requirement("cancel").set(True)

        # if cancelling, we cancel and return the cancellation set response
        if self.requirements.get_requirement("cancel").value:
            self.set_locking_session(False)
            return self.requirements.get_requirement("cancel").set_msg

        # iterate over requirements
        for requirement in self.requirements.requirements:  # type: Requirement

            # if the requirement has no value, we check for if kwargs set it
            if not requirement.value:

                logging.info("examing unmet requirement: %s" % requirement.name)
                if requirement.name in kwargs:
                    logging.info("requirement kwarg: %s is passed" % requirement.name)
                    if requirement.options:
                        logging.info("Searching for close_match in options: %s" % requirement.options)

                        closest_match = difflib.get_close_matches(kwargs[requirement.name], requirement.options)
                        if closest_match:
                            requirement.set(closest_match[0])
                        else:
                            response = "Invalid selection: %s is not in %s" % (kwargs[requirement.name], requirement.options)
                            return response
                    else:
                        requirement.set(kwargs[requirement.name])
                    response = requirement.set_msg.format(**requirement.get())
                else:
                    logging.info("%s not in kw: %s" % (requirement.name, kwargs))
            else:
                response = requirement.set_msg.format(**requirement.get())

        for requirement in self.requirements.requirements:  # type: Requirement
            logging.info("Checking requirement: %s" % requirement.name)
            # if the requirement has no value, we check for if kwargs set it
            if not requirement.value and requirement.auto_prompt:
                logging.info("Requirement not met: %s" % requirement.name)
                return "%s, %s" % (response, requirement.unset_msg)

        logging.info("No unmet requirements")
        return "Your order is complete"

    def help(self):
        response = "I am Penucci"
        for r in self.requirements.requirements:
            if r.value:
                response = "%s\n%s" % (response, r.set_msg.format(**r.get()))
            if not r.value:
                response = "%s\n%s" % (response, r.unset_msg.format(**r.get()))

        return response