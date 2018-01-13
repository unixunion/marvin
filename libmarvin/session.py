import requests

from libmarvin import util
import logging
import pprint

def extract_entities(intent):
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

    def __init__(self):
        self.plugin_instances = {}

    # return the method which should handle the intent
    def get_intent_plugin(self, intent, *args, **kwargs):
        if not intent in self.plugin_instances:
            self.plugin_instances[intent] = util.plugin(intent, *args, **kwargs)
        return self.plugin_instances[intent]

    @staticmethod
    def get_intent_plugin_method(plugin, method, *args, **kwargs):
        return plugin.get_method_by_name(method, *args, **kwargs)

    async def query(self, line=None, author=None, *args, **kwargs):

        try:
            r = requests.post("http://localhost:5000/parse", data='{"q": "%s"}' % line)
        except Exception as e:
            return "error: linquistic neural network is offline.", 0
        pprint.pprint (r.json())

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
                # return plugin_method(author=author, line=line, **kwargs)
                result = await plugin_method(author=author, line=line, **intent_kwargs)
                return "%s" % result, confidence
            except Exception as e:
                return "exception %s" % e, confidence
        else:
            try:
                logging.info("getting intent plugin: %s" % intent_name)
                plugin = self.get_intent_plugin(intent_name)
                plugin_method = self.get_intent_plugin_method(plugin, 'default')
                # return plugin_method(author=author, line=line, **kwargs)
                result = await plugin_method(author=author, line=line, **intent_kwargs)
                return "%s" % result, confidence
            except Exception as e:
                logging.error( "unable to reach plugin: %s, %s" % (intent_name, e))
                return "unable to reach plugin: %s" % intent_name, confidence