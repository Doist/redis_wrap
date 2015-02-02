from .redis_systems import *

class SetFu (redis_obj):

    def add(self, item):
        self.conn.sadd(self.name, item)

    def discard(self, item):
        self.conn.srem(self.name, item)

    def remove(self, item):
        r = self.conn.srem(self.name, item)
        if r < 1:
            raise KeyError

    def pop(self):
        r = self.conn.spop(self.name)
        if r == None:
            raise KeyError
        return r

    def update(self, other):
        if isinstance(other, SetFu):
            self.conn.sunionstore(self.name, self.name, other.name)
        else:
            for item in other:
                self.add(item)

    def intersection_update(self, other):
        if isinstance(other, SetFu):
            self.conn.sinterstore(self.name, self.name, other.name)
        else:
            for item in self:
                if item not in other:
                    self.discard(item)

    def difference_update(self, other):
        if isinstance(other, SetFu):
            self.conn.sdiffstore(self.name, self.name, other.name)
        else:
            for item in other:
                self.discard(item)

    def symmetric_difference_update(self, other):
        if isinstance(other, SetFu):
            with self.conn.pipeline(transaction=True) as trans:
                trans.sunionstore('__transientkey-1__', self.name, other.name)
                trans.sinterstore('__transientkey-2__', self.name, other.name)
                trans.sdiffstore(self.name, '__transientkey-1__', '__transientkey-2__')
                trans.delete('__transientkey-1__', '__transientkey-2__')
                trans.execute()
        else:
            for item in other:
                if item in self:
                    self.remove(item)
                else:
                    self.add(item)

    def __iter__(self):
        for item in self.conn.smembers(self.name):
            yield item

    def __len__(self):
        return self.conn.scard(self.name)

    def __contains__(self, item):
        return self.conn.sismember(self.name, item)

    def __isub__(self, other):
        self.difference_update(other)
        return self

    def __iand__(self, other):
        self.intersection_update(other)
        return self

    def __ixor__(self, other):
        self.symmetric_difference_update(other)
        return self

    def __ior__(self, other):
        self.update(other)
        return self
