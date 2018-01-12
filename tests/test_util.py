
import os
import unittest

from libmarvin import util
from libmarvin.intents.nullplugin import NullPlugin
from libmarvin.util import MissingProperty


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
        self.assertEqual(o.some_static_method("arg1", "arg2"), ('arg1', 'arg2') )
