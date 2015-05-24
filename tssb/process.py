import scipy.stats as stats
import numpy as np

class RandomProcess(object):

    def __init__(self, next, ndtype=np.longdouble):
        self.next = next
        self.ndtype = ndtype
        self.items = []
        self.cur_index = -1

class IndependentRandomProcess(RandomProcess):

    def __getitem__(self, key):
        if key > self.cur_index:
            size = key - self.cur_index
            next_items = self.next(size=size)
            self.items.extend(next_items)
            self.cur_index = key
        return self.items[key]

class MarkovRandomProcess(RandomProcess):

    def __init__(self, next, initial, ndtype=np.longdouble):
        super(MarkovRandomProcess, self).__init__(next, ndtype=ndtype)
        self.initial = initial

    def __getitem__(self, key):
        if key > self.cur_index:
            while self.cur_index < key:
                self.cur_index += 1
                if self.cur_index == 0:
                    self.items.append(self.initial())
                else:
                    self.items.append(self.next(self.items[-1]))
        return self.items[key]

class MarkovTreeRandomProcess(MarkovRandomProcess):

    def __init__(self, next, initial, ndtype=np.longdouble):
        super(MarkovTreeRandomProcess, self).__init__(next, initial, ndtype=ndtype)
        self.items = {}

    def __getitem__(self, key):
        if key not in self.items:
            if len(key) == 0:
                self.items[key] = self.initial()
            parent = self[key[:-1]]
            self.items[key] = self.next(parent)
        return self.items[key]

def create_gaussian_markov_process(eta, cov, prior):

    def initial():
        return (prior.sample(), cov)

    def next(prev):
        mean, cov = prev
        return (stats.multivariate_normal(mean=mean, cov=cov).rvs(), cov)

    return MarkovTreeRandomProcess(next, initial, ndtype=np.longdouble)
