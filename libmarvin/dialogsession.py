import logging
import uuid


class DialogSession:
    _id = None
    _user = None
    _plugin = None
    _data = None

    def __init__(self):
        logging.info("new dialog session")
        self.id = str(uuid.uuid1())

    def id(self):
        return self._id

    def set_user(self, user: object):
        self._user = user

    def get_user(self):
        return self._user

    def set_plugin(self, plugin: object):
        self._plugin = plugin

    def get_plugin(self):
        return self._plugin

    def set_data(self, data: object):
        self._data = data

    def get_data(self):
        return self._data