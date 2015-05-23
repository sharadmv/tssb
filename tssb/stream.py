import numpy as np

class RandomStream(object):

    def __init__(self, distribution, ndtype=np.longdouble):
        self.distribution = distribution
        self.ndtype = ndtype
        self.items = []
        self.cur_index = -1

    def __getitem__(self, key):
        if key > self.cur_index:
            size = key - self.cur_index
            next_items = self.distribution.sample(size=size)
            self.items.extend(next_items)
            self.cur_index = key
        return self.items[key]

class TreeRandomStream(object):
    pass
