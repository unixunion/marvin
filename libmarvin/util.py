import inspect
import logging

import libmarvin

def get_calling_module(point=2):
    """
    Return a module at a different point in the stack.
    :param point: the number of calls backwards in the stack.
    :return:
    """
    frm = inspect.stack()[point]
    function = str(frm[3])
    line = str(frm[2])
    modulepath = str(frm[1]).split('/')
    module = str(modulepath.pop())
    return "%s:%s" % (module, line)

def plugin(plugin_name, *args, **kwargs):
    """
    Gets a plugin, configures it, then allows direct communication with it.
    Plugins are passed the kwargs directly if any are specified.
    Example:
        >>> p1 = util.plugin("NullPlugin")
        >>> p1.some_method("foo", bar="baz")
        (('foo',), {'bar': 'baz'})
        >>> p2 = api.manage("NullPlugin", a="a")
        >>> p2.kwargs['a']
        'a'
    """


    plugin = libmarvin.plugin_registry(plugin_name, *args, **kwargs)
    logging.debug("Setting up the plugin instance with api and kwargs")
    return plugin(api=None, *args, **kwargs)


class MissingProperty(Exception):
    pass


def get_key_from_kwargs(key, kwargs, default=None, optional=False):
    """
    Returns a key from kwargs or raises exception is no key is present
    Example:
    >>> get_key_from_kwargs("vpn_name", kwargs)
    'dev_testvpn'
    >>> get_key_from_kwargs("missing_key", other_dict, default=True, optional=False)
    True
    >>> get_key_from_kwargs("missin_key", kwargs)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/keghol/Development/libsolace/libsolace/util.py", line 303, in get_key_from_kwargs
        raise(MissingProperty(key))
    libsolace.Exceptions.MissingProperty: missing_key
    """
    if key in kwargs:
        return kwargs.get(key)
    elif default is not None:
        return default
    elif optional is True:
        return
    else:
        logging.warning("Required kwarg %s not present" % key)
        raise (MissingProperty("%s is missing from kwargs" % key))
