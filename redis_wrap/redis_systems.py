import redis


#--- System related ----------------------------------------------
SYSTEMS = {
    'default': redis.Redis(host='localhost', port=6379)
}

def setup_system(name, host, port, **kw):
    SYSTEMS[name] = redis.Redis(host=host, port=port, **kw)

def get_redis(system='default'):
    return SYSTEMS[system]


class redis_obj:

    def __init__(self, name, system):
        self.name = name
        self.conn = get_redis(system)

    def clear(self):
        self.conn.delete(self.name)

