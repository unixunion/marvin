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

    def get(self):
        return {"id": self._id, "user": self._user, "plugin": self._plugin, "data": self._data}

    def id(self):
        return self._id

    def set_user(self, user: object):
        logging.info("user set to %s" % self._user)
        self._user = user

    def get_user(self):
        return self._user

    def set_plugin(self, plugin: object):
        logging.info("plugin set to %s" % self._plugin)
        self._plugin = plugin

    def get_plugin(self):
        return self._plugin

    def set_data(self, data: object):
        logging.info("data set to %s" % self._data)
        self._data = data

    def get_data(self):
        return self._data
