from redis_wrap import get_redis, get_list, get_hash, get_set


def setup_module(module=None):
    get_redis().delete('bears')
    get_redis().delete('villains')
    get_redis().delete('fishes')


def test_list():
    bears = get_list('bears')

    bears.append('grizzly')
    assert len(bears) == 1

    for bear in bears:
        assert bear == 'grizzly'

    assert 'grizzly' in bears

    bears.extend(['white bear', 'pedo bear'])
    assert len(bears) == 3

    bears.remove('grizzly')
    assert 'grizzly' not in bears


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


def test_set():
    fishes = get_set('fishes')
    assert 'nemo' not in fishes

    fishes.add('nemo')
    assert 'nemo' in fishes

    for item in fishes:
        assert item == 'nemo'


if __name__ == '__main__':
    setup_module()
    test_list()
    test_hash()
    test_set()
