import sys
from redis_wrap import get_redis, get_list, get_hash, get_set

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

    try:
        bears[5] = 'dizzy bear'
        assert 5 < len(bears)
    except IndexError:
        pass

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

    assert deers[0] == 'rudolf_99'
    assert deers[1] == 'rudolf_98'

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

    fishes.add('nemo')
    assert len(fishes) == 1
    assert 'nemo' in fishes

    for item in fishes:
        assert item == 'nemo'

    print sys._getframe(0).f_code.co_name, 'ok.'

if __name__ == '__main__':
    setup_module()
    test_list()
    test_list_trim()
    test_hash()
    test_set()
