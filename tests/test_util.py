
import os
import unittest

from libmarvin import util, Plugin
from libmarvin.intents.nullplugin import NullPlugin
from libmarvin.util import MissingProperty, get_key_from_kwargs


class UtilTest(unittest.TestCase):
    def test_plugin(self):
        import libmarvin
        import libmarvin.settingsloader as settings

        # bad config keys
        with self.assertRaises(MissingProperty):
            util.plugin("NullPlugin")

        # instantiate correctly
        o = util.plugin("NullPlugin", somekey="value")

        # invoke a method
        method_instance_output = o.some_method("arg1", "arg2", kw1="kw1", kw2="kw2")

        # strip first element cause its the instance
        self.assertEqual(method_instance_output[1:], (('arg1', 'arg2'), {'kw1': 'kw1', 'kw2': 'kw2'}) )

        # check static method has all its marbels
        self.assertEqual(o.some_static_method("arg1", "arg2"), (('arg1', 'arg2'), {}) )

        # call a method by string name
        some_method=o.get_method_by_name('some_static_method')
        self.assertEqual(some_method("arg1", "arg2", kw1="kw1", kw2="kw2"), (('arg1', 'arg2'), {'kw1': 'kw1', 'kw2': 'kw2'}) )

        # call non-static method by name
        some_method=o.get_method_by_name('some_method')
        self.assertEqual(some_method("arg1", "arg2", kw1="kw1", kw2="kw2")[1:], (('arg1', 'arg2'), {'kw1': 'kw1', 'kw2': 'kw2'}))
        self.assertIsInstance(some_method()[0], Plugin)

    def test_get_key_from_kwargs(self):
        with self.assertRaises(MissingProperty):
            get_key_from_kwargs("test", {})

        a = get_key_from_kwargs("test", {}, "default")
        self.assertEqual(a, "default")