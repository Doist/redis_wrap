# -*- coding: utf-8 -*-
"""
redis_wrap
~~~~~~~~

Implements a wrapper for Redis datatypes so they mimic the datatypes found in Python.

Requires Redis 2.0+ and newest version of redis-py.

For best performance the wrappers are lazy and use direct Redis calls.
E.g. __len__ of list wrapper is implemented by calling llen.

redis-py can be downloaded from here:
* http://github.com/andymccurdy/redis-py

Examples
========

Example of list wrapper::

    bears = get_list('bears')
    bears.append('grizzly')
    assert len(bears) == 1
    assert 'grizzly' in bears

Example of hash wrapper::

    villains = get_hash('villains')
    assert 'riddler' not in villains

    villains['riddler'] = 'Edward Nigma'
    assert 'riddler' in villains

    assert len(villains.keys()) == 1

    del villains['riddler']
    assert len(villains) == 0

Example of set wrapper::

    fishes = get_set('fishes')
    assert 'nemo' not in fishes

    fishes.add('nemo')
    assert 'nemo' in fishes

    for item in fishes:
        assert item == 'nemo'

Example of other redis connection::

    setup_system('other', host='127.0.0.1', port=6379)
    bears = get_list('bears', 'other')

:copyright: 2010 by amix
:license: BSD, see LICENSE for more details.
"""
import redis


#--- System related ----------------------------------------------
SYSTEMS = {
    'default': redis.Redis(host='localhost', port=6379)
}

def setup_system(name, host, port, **kw):
    SYSTEMS[name] = redis.Redis(host=host, port=port, **kw)

def get_redis(system='default'):
    return SYSTEMS[system]


#--- Decorators ----------------------------------------------
def get_list(name, system='default'):
    return ListFu(name, system)

def get_hash(name, system='default'):
    return HashFu(name, system)

def get_set(name, system='default'):
    return SetFu(name, system)


#--- Data impl. ----------------------------------------------
class ListFu:

    def __init__(self, name, system):
        self.name = name
        self.conn = get_redis(system)

    def append(self, item):
        self.conn.rpush(self.name, item)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def remove(self, value):
        self.conn.lrem(self.name, value)

    def pop(self, index=None):
        if index:
            raise ValueError('Not supported')
        return self.conn.rpop(self.name)

    def list_trim(self, start, stop):
        self.conn.ltrim(self.name, start, stop)

    def __len__(self):
        return self.conn.llen(self.name)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.conn.lrange(self.name, key.start, key.stop)

        val = self.conn.lindex(self.name, key)
        if not val:
            raise IndexError
        return val

    def __setitem__(self, key, value):
        try:
            self.conn.lset(self.name, key, value)
        except redis.exceptions.ResponseError:
            raise IndexError

    def __iter__(self):
        i = 0
        while True:
            items = self.conn.lrange(self.name, i, i+30)
            if len(items) == 0:
                raise StopIteration
            for item in items:
                yield item
            i += 30


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


class SetFu:

    def __init__(self, name, system):
        self.name = name
        self.conn = get_redis(system)

    def add(self, item):
        self.conn.sadd(self.name, item)

    def discard(self, item):
        self.conn.srem(self.name, item)

    def remove(self, item):
        r = self.conn.srem(self.name, item)
        if r < 1:
            raise KeyError

    def pop(self, item):
        return self.conn.spop(self.name, item)

    def __iter__(self):
        for item in self.conn.smembers(self.name):
            yield item

    def __len__(self):
        return self.conn.scard(self.name)

    def __contains__(self, item):
        return self.conn.sismember(self.name, item)

