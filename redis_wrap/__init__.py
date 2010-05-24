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
        self.system = system

    def append(self, item):
        get_redis(self.system).lpush(self.name, item)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def remove(self, value):
        get_redis(self.system).lrem(self.name, value)

    def __len__(self):
        return get_redis(self.system).llen(self.name)

    def __iter__(self):
        client = get_redis(self.system)
        i = 0
        while True:
            items = client.lrange(self.name, i, i+30)
            if len(items) == 0:
                raise StopIteration
            for item in items:
                yield item
            i += 30


class HashFu:

    def __init__(self, name, system):
        self.name = name
        self.system = system

    def get(self, key, default=None):
        return get_redis(self.system).hget(self.name, key) or default

    def keys(self):
        return get_redis(self.system).hkeys(self.name) or []

    def values(self):
        return get_redis(self.system).hvals(self.name) or []

    def __len__(self):
        return get_redis(self.system).hlen(self.name) or 0

    def __getitem__(self, key):
        val = self.get(key)
        if not val:
            raise KeyError
        return val

    def __setitem__(self, key, value):
        get_redis(self.system).hset(self.name, key, value)

    def __delitem__(self, key):
        get_redis(self.system).hdel(self.name, key)

    def __contains__(self, key):
        return get_redis(self.system).hexists(self.name, key)


class SetFu:

    def __init__(self, name, system):
        self.name = name
        self.system = system

    def add(self, item):
        get_redis(self.system).sadd(self.name, item)

    def remove(self, item):
        get_redis(self.system).srem(self.name, item)

    def pop(self, item):
        return get_redis(self.system).spop(self.name, item)

    def __iter__(self):
        client = get_redis(self.system)
        for item in client.smembers(self.name):
            yield item

    def __contains__(self, item):
        return get_redis(self.system).sismember(self.name, item)
