Python wrapper for Redis datatypes
===========================================

Implements a wrapper for Redis datatypes so they mimic the datatypes found in Python.

Requires Redis 2.0+ and newest version of redis-py.

For best performance the wrappers are lazy and use direct Redis calls, for example:
    
    len(get_list("bears")) # will call redis_client.llen("bears")

    'grizzly' in get_hash('bears') # will call redis_client.hexists('bears', 'grizzly')

redis-py can be downloaded from here:

* [redis-py on github](http://github.com/andymccurdy/redis-py)

You can also quick install it from [PyPi](http://pypi.python.org/pypi/redis_wrap):
    
* $ sudo easy_install redis_wrap

Related:

* [Blog post about redis_wrap](http://amix.dk/blog/post/19508#redis-wrap-Python-wrapper-for-Redis-datatypes)

Examples
========

Example of list wrapper:

    bears = get_list('bears')
    bears.append('grizzly')
    assert len(bears) == 1
    assert 'grizzly' in bears


Example of hash wrapper:

    villains = get_hash('villains')
    assert 'riddler' not in villains

    villains['riddler'] = 'Edward Nigma'
    assert 'riddler' in villains

    assert len(villains.keys()) == 1

    del villains['riddler']
    assert len(villains) == 0


Example of set wrapper:

    fishes = get_set('fishes')
    assert 'nemo' not in fishes

    fishes.add('nemo')
    assert 'nemo' in fishes

    for item in fishes:
        assert item == 'nemo'
