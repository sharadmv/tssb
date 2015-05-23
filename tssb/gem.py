import numpy as np
import scipy.stats as stats

from util import ScipySampler
from dist import Distribution
from stream import RandomStream

class GEM(Distribution):

    def __init__(self, a, ndtype=np.longdouble):
        self.a = a
        self.ndtype = ndtype

    def __getitem__(self, key):
        return self.get_weight(key)

    def sample_one(self):
        return self.index(np.random.random())

    def uniform_index(self, u):
        location = 0
        i = -1
        while location < u:
            i += 1
            weight = self.get_weight(i)
            location += weight
        return i, location

    def get_weight(self, index):
        raise NotImplementedError

class TruncatedGEM(GEM):

    def __init__(self, a, max_length):
        super(TruncatedGEM, self).__init__(a)
        self.max_length = max_length

        self.initialize()

    def initialize(self):
        self.betas = np.random.beta(1, self.a, size=self.max_length).astype(self.ndtype)
        self.weights = np.zeros(self.max_length).astype(self.ndtype)

        prev = 1
        for i in xrange(self.max_length - 1):
            self.weights[i] = self.betas[i] * prev
            prev *= (1 - self.betas[i])
        self.weights[self.max_length - 1] = 1 - np.sum(self.weights)
        np.testing.assert_equal(1, np.sum(self.weights))

    def get_weight(self, index):
        if index >= self.max_length:
            raise Exception("index desired greater than max_length, %u" % self.max_length)
        return self.weights[index]

class LazyGEM(GEM):

    def __init__(self, a):
        super(LazyGEM, self).__init__(a)

        self.initialize()

    def initialize(self):
        self.betas = RandomStream(ScipySampler(stats.beta(1, self.a), ndtype=self.ndtype))
        self.weights = np.zeros(0).astype(self.ndtype)
        self.index = -1
        self.prev = self.ndtype(1)


    def get_weight(self, index):
        if index > self.index:
            diff = index - self.index
            weights = np.random.beta(1, self.a, size=diff).astype(self.ndtype)
            self.weights = np.concatenate([self.weights, weights])
            for i in xrange(self.index + 1, index + 1):
                self.weights[i] = self.betas[i] * self.prev
                self.prev *= (1 - self.betas[i])
                self.index += 1
        return self.weights[index]
