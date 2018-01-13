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

    @staticmethod
    async def status(*args, author=None, line=None, **kwargs):
        return "I'm operating within acceptable parameters."

    @staticmethod
    async def quote_laws(*args, author=None, line=None, **kwargs):
        return """1st law: A robot may not injure a human being or, through inaction, allow a human being to come to harm.\n
2nd law: A robot must obey the orders given it by human beings except where such orders would conflict with the First Law.\n
3rd law: A robot must protect its own existence as long as such protection does not conflict with the First or Second Laws."""

    @staticmethod
    async def thanks(*args, author=None, line=None, **kwargs):
        return "you're welcome %s!" % author

    # default method to call if no double underscored method mentioned in intent name
    def default(self, *args, **kwargs):
        return "Default: args: %s, kwargs %s" % (args, kwargs)