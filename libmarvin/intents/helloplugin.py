from libmarvin import Plugin
import libmarvin
import logging

from libmarvin.util import get_key_from_kwargs


@libmarvin.plugin_registry.register
class HelloPlugin(Plugin):
    plugin_name = "HelloPlugin"
    args = None
    kwargs = None

    def __init__(self, *args, **kwargs):
        logging.info("Instantiating %s" % self)
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def hello(user):
        return "hello %s" % user