#!/usr/bin/env python2
# encoding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys

from redis_wrap import get_bitset, get_hash, get_list, get_redis, get_set


def raises(f, excpt):
    try:
        f()
        return False
    except excpt:
        return True


def setup_module(module=None):
    get_redis().delete('bears')
    get_redis().delete('deers')
    get_redis().delete('villains')
    get_redis().delete('fishes')

    print(sys._getframe(0).f_code.co_name, 'ok.')


def test_list():
    bears = get_list('bears')
    assert len(bears) == 0

    bears.append('grizzly')
    assert len(bears) == 1
    assert bears[0] == 'grizzly'
    assert bears[-1] == 'grizzly'

    for bear in bears:
        assert bear == 'grizzly'

    assert 'grizzly' in bears

    bears.extend(['white bear', 'pedo bear'])
    assert len(bears) == 3

    bears[2] = 'nice bear'
    assert bears[2] == 'nice bear'

    assert 5 > len(bears)
    try:
        bears[5] = 'dizzy bear'
    except IndexError:
        pass

    bears.extend(['polar bear', 'gummy bear'])
    assert list(bears) == ['grizzly', 'white bear', 'nice bear', 'polar bear', 'gummy bear']

    assert bears[1:2] == ['white bear']
    assert bears[2:4] == ['nice bear', 'polar bear']
    assert bears[:2] == ['grizzly', 'white bear']
    assert bears[-2:] == ['polar bear', 'gummy bear']
    assert bears[10:20] == []

    bears.remove('grizzly')
    assert 'grizzly' not in bears

    print(sys._getframe(0).f_code.co_name, 'ok.')


def test_list_trim():
    deers = get_list('deers')

    for i in range(0, 100):
        deers.append('rudolf_%s' % i)

    assert len(deers) == 100

    deers.list_trim(0, 5)

    assert len(deers) == 6

    assert deers[0] == 'rudolf_0'
    assert deers[1] == 'rudolf_1'

    print(sys._getframe(0).f_code.co_name, 'ok.')


def test_hash():
    villains = get_hash('villains')
    assert 'riddler' not in villains

    villains['riddler'] = 'Edward Nigma'
    assert 'riddler' in villains
    assert villains.get('riddler') == 'Edward Nigma'

    assert len(villains.keys()) == 1
    assert villains.values() == ['Edward Nigma']

    assert list(villains) == ['riddler']

    assert villains.items() == [('riddler', 'Edward Nigma')]

    del villains['riddler']
    assert len(villains.keys()) == 0
    assert 'riddler' not in villains

    villains['drZero'] = ''
    assert villains['drZero'] == ''

    assert villains.pop('drZero') == ''
    assert 'drZero' not in villains

    assert raises(lambda: villains.pop('Mysterio'), KeyError)
    assert villains.pop('Mysterio', 'Quentin Beck') == 'Quentin Beck'

    villains.update({'drEvil':'Douglas Powers'})
    villains.update([('joker','Jack'),('penguin','Oswald Chesterfield Cobblepot')])
    assert set(villains.items()) == set([
        ('drEvil','Douglas Powers'),
        ('joker','Jack'),
        ('penguin','Oswald Chesterfield Cobblepot')])

    other_villains = get_hash('minions')
    other_villains.update(lizard='Curt Connors', rhino='Aleksei Sytsevich')
    villains.update(other_villains)
    assert set(villains.items()) == set([
        ('drEvil','Douglas Powers'),
        ('joker','Jack'),
        ('penguin','Oswald Chesterfield Cobblepot'),
        ('lizard','Curt Connors'),
        ('rhino', 'Aleksei Sytsevich')])

    print(sys._getframe(0).f_code.co_name, 'ok.')


def test_set():
    fishes = get_set('fishes')
    assert len(fishes) == 0
    assert 'nemo' not in fishes

    assert raises(lambda: fishes.remove('nemo'), KeyError)

    fishes.discard('nemo')      # it's ok to .discard() nonexistant items

    fishes.add('nemo')
    assert len(fishes) == 1
    assert 'nemo' in fishes

    for item in fishes:
        assert item == 'nemo'

    fishes.remove('nemo')
    assert len(fishes) == 0

    fishes.add('dory')
    assert fishes.pop() == 'dory'
    assert raises(lambda: fishes.pop(), KeyError)

    fishes.add('marlin')
    assert len(fishes) == 1
    fishes.clear()
    assert len(fishes) == 0

    fishes.update(('nemo','marlin'))
    assert set(fishes) == set (['nemo','marlin'])
    fishes |= ('dory','crush')
    assert set(fishes) == set (['nemo','marlin', 'dory', 'crush'])

    other_fishes = get_set('other_fishes')
    other_fishes.update(('gill', 'bloat', 'flo'))
    fishes |= other_fishes
    assert set(fishes) == set(['nemo','marlin', 'dory', 'crush', 'gill', 'bloat', 'flo'])

    fishes.intersection_update(('nemo','marlin', 'dory', 'crush', 'gill', 'deb', 'bloat'))
    assert set(fishes) == set(['nemo','marlin', 'dory', 'crush', 'gill', 'bloat'])
    fishes &= ('nemo','marlin', 'dory', 'gill', 'bloat', 'gurgle')
    assert set(fishes) == set(['nemo','marlin', 'dory', 'gill', 'bloat'])
    fishes &= other_fishes
    assert set(fishes) == set(['gill', 'bloat'])

    fishes.clear()
    fishes.update(('nemo','marlin', 'dory', 'gill', 'bloat'))
    fishes.difference_update(('gill', 'bloat', 'flo'))
    assert set(fishes) == set(['nemo','marlin', 'dory'])

    fishes.clear()
    fishes.update(('nemo','marlin', 'dory', 'gill', 'bloat'))
    fishes -= ('gill', 'bloat', 'flo')
    assert set(fishes) == set(['nemo','marlin', 'dory'])

    fishes.clear()
    fishes.update(('nemo','marlin', 'dory', 'gill', 'bloat'))
    fishes -= other_fishes
    assert set(fishes) == set(['nemo','marlin', 'dory'])

    fishes.clear()
    fishes.update(('nemo','marlin', 'dory', 'gill', 'bloat'))
    fishes.symmetric_difference_update(('gill', 'bloat', 'flo'))
    assert set(fishes) == set(['nemo','marlin', 'dory', 'flo'])

    fishes.clear()
    fishes.update(('nemo','marlin', 'dory', 'gill', 'bloat'))
    fishes ^= ('gill', 'bloat', 'flo')
    assert set(fishes) == set(['nemo','marlin', 'dory', 'flo'])

    fishes.clear()
    fishes.update(('nemo','marlin', 'dory', 'gill', 'bloat'))
    fishes ^= other_fishes
    assert set(fishes) == set(['nemo','marlin', 'dory', 'flo'])

    print(sys._getframe(0).f_code.co_name, 'ok.')


def test_bitset():
    users = get_bitset('users')
    users.clear()
    assert len(users) == 0

    assert 3 not in users
    users.add(3)
    assert len(users) == 1
    assert 3 in users

    assert raises(lambda: users.remove(9), KeyError)
    users.discard(9)
    users.add(7)
    users.remove(7)

    users |= (5,4)
    assert set(users) == set([3,4,5])

    others = get_bitset('others')
    others |= (4,6,8)
    assert set(others) == set([4,6,8])
    users |= others
    assert set(users) == set([3,4,5,6,8])

    users &= (4,5,6,7,8)
    assert set(users) == set([4,5,6,8])

    users.clear()
    assert len(users) == 0

    print(sys._getframe(0).f_code.co_name, 'ok.')


if __name__ == '__main__':
    setup_module()
    test_list()
    test_list_trim()
    test_hash()
    test_set()
    test_bitset()
