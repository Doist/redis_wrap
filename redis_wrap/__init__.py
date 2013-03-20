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

from redis_systems import *
from redis_list import ListFu
from redis_hash import HashFu
from redis_set import SetFu

#--- Decorators ----------------------------------------------
def get_list(name, system='default'):
    return ListFu(name, system)

def get_hash(name, system='default'):
    return HashFu(name, system)

def get_set(name, system='default'):
    return SetFu(name, system)


