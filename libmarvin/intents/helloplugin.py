from libmarvin import Plugin
import libmarvin
import logging

from libmarvin.util import get_key_from_kwargs


@libmarvin.plugin_registry.register
class HelloPlugin(Plugin):
    plugin_name = "helloplugin"
    args = None
    kwargs = None

    def __init__(self, *args, **kwargs):
        logging.info("instantiating %s" % self)
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    async def hello(*args, author=None, line=None, **kwargs):
        return "hello %s!" % (author)

    @staticmethod
    async def gbye(*args, author=None, line=None, **kwargs):
        return "goodbye human!"

    # default method to call if no double underscored method mentioned in intent name
    def default(self, *args, **kwargs):
        return "Default: args: %s, kwargs %s" % (args, kwargs)