from .redis_systems import *

class BitsetFu (redis_obj):

    def add(self, item):
        self.conn.setbit(self.name, item, True)

    def remove(self, item):
        r = self.conn.setbit(self.name, item, False)
        if not r:
            raise KeyError

    def discard(self, item):
        self.conn.setbit(self.name, item, False)

    def update(self, other):
        if isinstance(other, BitsetFu):
            self.conn.bitop('OR', self.name, self.name, other.name)
        else:
            for itm in other:
                self.add(itm)

    def intersection_update(self, other):
        if isinstance(other, BitsetFu):
            self.conn.bitop('AND', self.name, self.name, other.name)
        else:
            for item in self:
                if item not in other:
                    self.discard(item)

    def symmetric_difference_update(self, other):
        if isinstance(other, BitsetFu):
            self.conn.bitop('XOR', self.name, self.name, other.name)
        else:
            for item in other:
                if item in self:
                    self.remove(item)
                else:
                    self.add(item)

    def __len__(self):
        return self.conn.bitcount(self.name)

    def __iter__(self):
        for i in range(self.conn.strlen(self.name)*8):
            if self.conn.getbit(self.name, i):
                yield i

    def __contains__(self, item):
        return self.conn.getbit(self.name, item)

    def __iand__(self, other):
        self.intersection_update(other)
        return self

    def __ixor__(self, other):
        self.symmetric_difference_update(other)
        return self

    def __ior__(self, other):
        self.update(other)
        return self
