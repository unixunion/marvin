import inspect
from inspect import FullArgSpec

__author__ = 'keghol'

"""
The plugin system
"""

import functools
import logging
from collections import OrderedDict

from libmarvin.util import get_calling_module, get_key_from_kwargs


class PluginClass(type):
    """This is a metaclass for construction only, see Plugin rather"""

    def __new__(cls, clsname, bases, dct):
        new_object = super(PluginClass, cls).__new__(cls, clsname, bases, dct)
        return new_object


class Plugin(object):
    """This is the plugin core object where all plugins should extend from and register too.
    Plugin Example:
    .. doctest::
        :options: +SKIP
        >>> import pprint
        >>> import libmarvin
        >>> from libmarvin.plugin import Plugin
        >>> @libmarvin.plugin_registry.register
        >>> class Bar(Plugin):
        >>>     plugin_name = "BarPlugin"
        >>>     def __init__(self, *args, **kwargs):
        >>>         pass
        >>>     # Instance methods work!
        >>>     def hello(self, *args, **kwargs):
        >>>         return "Args: %s from %s" % (args, self)
        >>>     # Static methods work too!
        >>>     @staticmethod
        >>>     def static_method(*args, **kwargs):
        >>>         print("args! %s kw: %s" % (args,kwargs))
        >>>
        >>> new_instance = libmarvin.util.plugin("NullPlugin", "arg1", "arg2", kw1="kw1", kw2="kw2")
        >>> print (new_instance.some_method("arg1", "arg2", kw1="kw1", kw2="kw2"))
        >>> libmarvin.plugin_registry('BarPlugin').static_method(None, "dude")
        >>> libmarvin.plugin_registry('BarPlugin').gbye()
        >>> pprint.pprint(dir(libmarvin.plugin_registry('BarPlugin')))
    Plugin Instantiation:
    >>> import libmarvin.settingsloader as settings
    >>> my_plugin = api.manage("NullPlugin")
    >>> type(my_plugin)
    <class 'libsolace.items.NullPlugin.NullPlugin'>
    Direct Instantiation:
    >>> import libmarvin.settingsloader as settings
    >>> import libmarvin
    >>> my_clazz = libmarvin.plugin_registry("NullPlugin", settings=settings)
    >>> my_instance = my_clazz(settings=settings)
    """
    __metaclass__ = PluginClass
    plugins = []
    plugins_dict = OrderedDict()
    plugin_name = "Plugin"

    context_locking = False
    lock_session = False
    lock_session_default_method = None

    """ the plugin's name, override this in the derived class!"""
    exists = False

    def __init__(self, *args, **kwargs):
        logging.debug("Plugin Init: %s, %s" % (args, kwargs))

    # async def create_cls(cls, *args, **kwargs):
    #     foo = Foo(settings)
    #     await foo._init()
    #     return foo

    def register(self, object_class, *args, **kwargs):
        """
        Registers a object with the plugin registry, typically used as a decorator.
        :param object_class: the class to register as a plugin
        Example:
            .. doctest::
                :options: +SKIP
                >>> @libmarvin.plugin_registry.register
                >>> class Foo(Plugin)
                >>> ...
        """
        logging.info("Registering Plugin id: %s from class: %s " % (object_class.plugin_name, object_class))
        o = object_class

        # TODO FIXME
        # plugin_members = inspect.getmembers(o)
        # for pm in plugin_members:
        #     print ("%s: %s" % (o.plugin_name, pm))

        # print (inspect.getfullargspec(o.__init__))
        # plugin_init_parameters = inspect.getfullargspec(o.__init__) # type:FullArgSpec

        self.plugins.append(o)
        self.plugins_dict[object_class.plugin_name] = o

        def _d(fn):
            logging.info("CALL CALL CALL CALL CALL CALL")
            return functools.update_wrapper(object_class(fn), fn)

        functools.update_wrapper(_d, object_class)
        return _d

    # return a method
    def get_method_by_name(self, method):
        return getattr(self, method)

    def __call__(self, *args, **kwargs):
        """
        When you call the registry with the name of a plugin eg: 'NullPlugin', as the first arg, this returns the class
        from the plugin_registry. You can then instantiate the class in any way you need to.
        Example
        >>> import libmarvin
        >>> from libmarvin.plugin import Plugin
        >>> a = libmarvin.plugin_registry("NullPlugin")
        >>> type(a)
        ""
        :param args: name of Plugin to return
        :param kwargs:
        :return: class
        """

        try:
            module = get_calling_module(point=2)
        except:
            module = "Unknown"

        try:
            module_parent = get_calling_module(point=3)
        except:
            module_parent = "Unknown"

        logging.debug(self.plugins_dict)
        logging.info("Module %s->%s->%s" % (module_parent, module, args[0]))

        logging.debug("Plugin Request: args: %s, kwargs: %s" % (args, kwargs))
        try:
            logging.debug("Class: %s" % self.plugins_dict[args[0]])
            return self.plugins_dict[args[0]]
        except:
            logging.warning("No plugin named: %s found, available plugins are: %s" % (args[0], self.plugins_dict))
            logging.warning(
                "Please check the plugin is listed in the yaml config and that you have @libsolace.plugin_registry.register in the class")
            raise

    # is the plugin a context locking one?
    def is_context_locking(self) -> bool:
        return self.context_locking

    # set the session locking to value
    def set_locking_session(self, value: bool):
        self.lock_session = value

    # is the plugin currently locking a session
    def is_locking_session(self):
        return self.lock_session

    # returns the data from the session
    def get_data(self, *args, **kwargs):
        return self.begin_session(*args, **kwargs).get_data()

    def destroy_session(self, *args, **kwargs):
        message_object = get_key_from_kwargs('message_object', kwargs)  # type: discord.Message
        user = message_object.author.id  # type: discord.User
        self.dialog_sessions[user] = None
        self.dialog_sessions.pop(user)

# class PluginResponse(object):
#     """
#     Encapsulating class for holding SEMP requests and their accompanying kwargs.
#     Example:
#     >>> request = PluginResponse('<rpc semp-version="soltr/7_1_1"><show><memory/></show></rpc>', primaryOnly=True)
#     >>> request.xml
#     '<rpc semp-version="soltr/7_1_1"><show><memory/></show></rpc>'
#     """
#     def __init__(self, xml, **kwargs):
#         self.xml = xml
#         """ the XML """
#         self.kwargs = kwargs
#         """ the kwargs """
