from libmarvin import Plugin
import libmarvin
import logging

from libmarvin.util import get_key_from_kwargs


@libmarvin.plugin_registry.register
class NullPlugin(Plugin):
    plugin_name = "NullPlugin"
    args = None
    kwargs = None

    def __init__(self, *args, **kwargs):
        logging.info("Instantiating %s" % self)
        self.somekey = get_key_from_kwargs('somekey', kwargs)
        kwargs.pop('api')
        self.args = args
        self.kwargs = kwargs

    def some_method(self, *args, **kwargs):
        return self, args, kwargs

    @staticmethod
    def some_static_method(*args, **kwargs):
        return args, kwargs

    @staticmethod
    def help():
        return "NullPlugin Help Stub"