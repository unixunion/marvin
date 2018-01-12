class Cache(object):
    cache = {}

    def __init__(self):
        self.cache = {}

    @staticmethod
    def get(id):
        return Cache.cache[id]

    @staticmethod
    def set(id, object):
        Cache.cache[id] = object
