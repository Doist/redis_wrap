from redis_systems import *

class HashFu:

    def __init__(self, name, system):
        self.name = name
        self.conn = get_redis(system)

    def get(self, key, default=None):
        return self.conn.hget(self.name, key) or default

    def keys(self):
        return self.conn.hkeys(self.name) or []

    def values(self):
        return self.conn.hvals(self.name) or []

    def __len__(self):
        return self.conn.hlen(self.name) or 0

    def __iter__(self):
        for k in self.keys():
            yield k

    def __getitem__(self, key):
        val = self.get(key)
        if not val:
            raise KeyError
        return val

    def __setitem__(self, key, value):
        self.conn.hset(self.name, key, value)

    def __delitem__(self, key):
        self.conn.hdel(self.name, key)

    def __contains__(self, key):
        return self.conn.hexists(self.name, key)

