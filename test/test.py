import sys
from redis_wrap import get_redis, get_list, get_hash, get_set

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

    print sys._getframe(0).f_code.co_name, 'ok.'

def test_list():
    bears = get_list('bears')

    bears.append('grizzly')
    assert len(bears) == 1

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
    assert bears[1:2] == ['white bear', 'nice bear']
    assert bears[2:4] == ['nice bear', 'polar bear', 'gummy bear']

    bears.remove('grizzly')
    assert 'grizzly' not in bears

    print sys._getframe(0).f_code.co_name, 'ok.'

def test_list_trim():
    deers = get_list('deers')

    for i in range(0, 100):
        deers.append('rudolf_%s' % i)

    assert len(deers) == 100

    deers.list_trim(0, 5)

    assert len(deers) == 6

    assert deers[0] == 'rudolf_0'
    assert deers[1] == 'rudolf_1'

    print sys._getframe(0).f_code.co_name, 'ok.'

def test_hash():
    villains = get_hash('villains')
    assert 'riddler' not in villains

    villains['riddler'] = 'Edward Nigma'
    assert 'riddler' in villains
    assert villains.get('riddler') == 'Edward Nigma'

    assert len(villains.keys()) == 1
    assert villains.values() == ['Edward Nigma']

    del villains['riddler']
    assert len(villains.keys()) == 0
    assert 'riddler' not in villains
    print sys._getframe(0).f_code.co_name, 'ok.'

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

    fishes.add('dori')
    assert fishes.pop() == 'dori'
    assert raises(lambda: fishes.pop(), KeyError)

    fishes.add('martin')
    assert len(fishes) == 1
    fishes.clear()
    assert len(fishes) == 0

    numbers = get_set('numbers')
    fishes.update(('one','two'))
    assert set(fishes) == set (['one','two'])
    fishes |= ('three','four')
    assert set(fishes) == set (['one','two', 'three','four'])

    print sys._getframe(0).f_code.co_name, 'ok.'

if __name__ == '__main__':
    setup_module()
    test_list()
    test_list_trim()
    test_hash()
    test_set()
