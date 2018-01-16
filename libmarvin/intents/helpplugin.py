from libmarvin import Plugin
import libmarvin
import logging

from libmarvin.util import get_key_from_kwargs


@libmarvin.plugin_registry.register
class HelpPlugin(Plugin):
    plugin_name = "helpplugin"
    args = None
    kwargs = None

    def __init__(self, *args, **kwargs):
        logging.info("instantiating %s" % self)
        self.args = args
        self.kwargs = kwargs

    # default method to call if no double underscored method mentioned in intent name
    async def default(self, *args, **kwargs):
        logging.info("help: %s, %s" % (args, kwargs))
        return "I'm marvin, I'm a Natural Language Processing chat-bot! check my source: https://github.com/unixunion/marvin"