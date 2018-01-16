import inspect

import requests

from libmarvin import util
import logging
import pprint


def extract_entities(intent: dict) -> dict:
    """
    Extract the entities into key: value where key is the name of the entity as defined
    in the rasu training material, and the value being the value.

    the response from this should be suitable to be passed as kwargs into any method.

    :param intent: intent response from rasu
    :return: entities as a dictionary
    """
    # {'entity': 'user', 'value': '<@243698565086576641>', 'start': 4, 'end': 25, 'extractor': 'ner_mitie'}

    d = {}

    for e in intent["entities"]:
        logging.info("entity: %s" % e)
        d[e["entity"]] = e["value"]

    logging.info("generate kwargs: %s" % d)

    return d


class Session:
    # plugins this session instantiated, this is because plugins could have
    # session based state, like sudo, or contextual converses.
    plugin_instances = None

    # a plugin to lock the dialog context to for multi faceted discussions
    context_lock = None

    def __init__(self):
        logging.info("new session")
        self.plugin_instances = {}

    def get_plugin_init_parameters(self, pluginname):
        required_parameters = inspect.getfullargspec(util.plugin(pluginname).__init__)

    # return the method which should handle the intent
    def get_intent_plugin(self, intent, *args, **kwargs):

        # put the intent into the session cache if one does not exist
        if not intent in self.plugin_instances:
            logging.info("instantiating %s for the session stack" % intent)
            self.plugin_instances[intent] = util.plugin(intent, *args, **kwargs)
        else:
            logging.info("plugin %s already in cache" % intent)

        # check if context locked plugin is already in session
        if self.context_lock:
            logging.info("a context lock is set")
            plugin = self.context_lock # type: Plugin
            if plugin.is_locking_session():
                logging.info("the plugin: %s is locking session, returning it instead" % plugin)
                return plugin
            else:
                # unlocking context lock
                logging.info("unlocking the locking session")
                self.context_lock = None
                return self.plugin_instances[intent]
        else:
                logging.info("no context lock is in progress")
                plugin = self.plugin_instances[intent]
                if plugin.context_locking:
                    self.context_lock = plugin
                return plugin


    @staticmethod
    def get_intent_plugin_method(plugin, method, *args, **kwargs):
        logging.info("Getting intent plugin: %s, method: %s" % (plugin, method))
        if plugin.is_locking_session():
            return plugin.lock_session_default_method
        else:
            return plugin.get_method_by_name(method, *args, **kwargs)

    async def query(self, line=None, author=None, *args, **kwargs):

        try:
            r = requests.post("http://localhost:5000/parse", data='{"q": "%s"}' % line)
        except Exception as e:
            return "error: linquistic neural network is offline.", 0
        pprint.pprint(r.json())

        intent_name = r.json()['intent']['name']
        entities = r.json()['entities']
        intent_kwargs = extract_entities(r.json())
        intent_kwargs = {**intent_kwargs, **kwargs}
        confidence = r.json()['intent']['confidence']

        logging.info("Intent: %s, entities: %s" % (intent_name, entities))

        if "__" in intent_name:
            try:
                plugin_name = intent_name.split("__")[0]
                plugin_method_name = r.json()['intent']['name'].split("__")[1]
                plugin = self.get_intent_plugin(plugin_name)
                plugin_method = self.get_intent_plugin_method(plugin, plugin_method_name)
                result = await plugin_method(author=author, line=line, **intent_kwargs)
                return "%s" % result, confidence
            except Exception as e:
                return "exception %s" % e, confidence
        else:
            try:
                logging.info("getting intent plugin: %s" % intent_name)
                plugin = self.get_intent_plugin(intent_name)
                plugin_method = self.get_intent_plugin_method(plugin, 'default')
                result = await plugin_method(author=author, line=line, **intent_kwargs)
                return "%s" % result, confidence
            except Exception as e:
                logging.error("unable to reach plugin: %s, %s" % (intent_name, e))
                return "unable to reach plugin: %s" % intent_name, confidence
