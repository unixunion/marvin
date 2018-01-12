import requests

from libmarvin import util
import logging

class Session:

    # plugins this session instantiated, this is because plugins could have
    # session based state, like sudo, or contextual converses.
    plugin_instances = None

    def __init__(self):
        self.plugin_instances = {}

    # return the method which should handle the intent
    def get_intent_plugin(self, intent, *args, **kwargs):
        if not intent in self.plugin_instances:
            self.plugin_instances[intent] = util.plugin(intent, *args, **kwargs)
            # return util.plugin(intent, *args, **kwargs)
        return self.plugin_instances[intent]

    @staticmethod
    def get_intent_plugin_method(plugin, method, *args, **kwargs):
        return plugin.get_method_by_name(method, *args, **kwargs)

    def query(self, line=None, author=None):
        r = requests.post("http://localhost:5000/parse", data='{"q": "%s"}' % line)
        print (r.json())

        intent_name = r.json()['intent']['name']

        if "__" in intent_name:
            try:
                plugin_name = r.json()['intent']['name'].split("__")[0]
                plugin_method_name = r.json()['intent']['name'].split("__")[1]

                plugin = self.get_intent_plugin(plugin_name)
                plugin_method = self.get_intent_plugin_method(plugin, plugin_method_name)
                return plugin_method(author=author, line=line)
            except Exception as e:
                return "exception %s" % e
        else:
            try:
                logging.info("getting intent plugin: %s" % intent_name)
                plugin = self.get_intent_plugin(intent_name)
                plugin_method = self.get_intent_plugin_method(plugin, 'default')
                return plugin_method(author=author, line=line)
            except Exception as e:
                logging.error( "unable to reach plugin: %s, %s" % (intent_name, e))
                return "unable to reach plugin: %s" % intent_name