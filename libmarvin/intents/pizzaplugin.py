import difflib

from libmarvin import Plugin
import libmarvin
import logging

from libmarvin.dialogsession import DialogSession
from libmarvin.requirements import Requirements, Requirement
from libmarvin.util import get_key_from_kwargs


@libmarvin.plugin_registry.register
class PizzaPlugin(Plugin):
    plugin_name = "pizzaplugin"
    args = None
    kwargs = None
    dialog_sessions = None

    def __init__(self, *args, **kwargs):
        logging.info("Instantiating %s" % self)
        self.args = args
        self.kwargs = kwargs

        # this plugin locks a user into a dialog session, so lets set that.
        self.context_locking = True
        self.lock_session_default_method = self.order_pizza

        self.dialog_sessions = {}

        logging.info("Completed Instantiation")

    # creates a new session if one does not exist, else returns the existing one
    def begin_session(self, *args, **kwargs):
        logging.info("begin_session")

        message_object = get_key_from_kwargs('message_object', kwargs)  # type: discord.Message
        user = message_object.author.id  # type: discord.User

        if not user in self.dialog_sessions:
            logging.info("new dialog session starting for user: %s" % user)

            dialog_session = DialogSession()
            dialog_session.set_user(user)
            dialog_session.set_plugin(self)

            # requirements holders
            requirements = Requirements()  # type:Requirements

            # first we set all the requirements to with thier value to None
            requirements.new_requirement("menu", "The available pizza's are: {options}",
                                         "You have selected pizza: {value}",
                                         None, auto_prompt=False,
                                         options=["Cacciatore", "Mexican", "Taco", "Fish"])
            requirements.new_requirement("pizza_name", "Which pizza would you like to order?",
                                         "You have selected {value}", None)
            requirements.new_requirement("address", "What is the address?", "Address set to: {value}", None)
            requirements.new_requirement("payment_method", "How would you like to pay",
                                         "Payment method: {value}",
                                         None,
                                         options=["Cash", "Card"])
            requirements.new_requirement("confirm", "Please confirm your order.", "Order confirmed", None)
            requirements.new_requirement("cancel", "Would you like to cancel?", "Order cancelled", None,
                                         auto_prompt=False)

            # put requirements into the session
            dialog_session.set_data(requirements)
            self.dialog_sessions[user] = dialog_session
            return self.dialog_sessions[user]

        else:
            logging.info("continuing session for user: %s" % user)
            return self.dialog_sessions[user]



    # order pizza start / resume session, and continue to real methods
    async def order_pizza(self, *args, **kwargs):
        logging.info("order_pizza called %s %s" % (args, kwargs))
        user_session = self.begin_session(*args, **kwargs)  # type: DialogSession
        return await user_session.get_plugin().order_pizza_real(*args, **kwargs)

    # real method behind the scenes
    async def order_pizza_real(self, *args, **kwargs):

        if self.is_context_locking() and not self.is_locking_session():
            self.set_locking_session(True)
            return "%s, I am pizzabot, may I take your order?" % self.get_header()

        data = self.get_data(*args, **kwargs)
        logging.info("data: %s" % data)

        response = ""

        # check if this is a help request
        if get_key_from_kwargs("help", kwargs, default=False, is_optional=True):
            return self.help(*args, **kwargs)

        # check if this is a cancelation
        if get_key_from_kwargs("cancel", kwargs, default=False, is_optional=True):
            logging.info("cancelling order per user's requrest")
            data.get_requirement("cancel").set(True)

        # if cancelling, we cancel and return the cancellation set response
        if data.get_requirement("cancel").value:
            logging.info("cancelling order")
            self.set_locking_session(False)
            response = self.build_response(data.get_requirement("cancel").set_msg)
            data = None
            self.destroy_session(*args, **kwargs)
            return response

        # call on the data to handle the request
        return data.process_request(*args, **kwargs)


    def help(self, *args, **kwargs):
        response = "%s: I am Pizzabot!\n" % self.get_header()
        for r in self.get_data(*args, **kwargs).requirements:
            if r.value:
                response = "%s\n%s" % (response, r.set_msg.format(**r.get()))
            if not r.value:
                response = "%s\n%s" % (response, r.unset_msg.format(**r.get()))

        return response

    def get_header(self):
        return "%s" % self.plugin_name

    def build_response(self, message):
        return "%s: %s" % (self.plugin_name, message)