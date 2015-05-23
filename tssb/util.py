import numpy as np

from dist import Distribution

class ScipySampler(Distribution):

    def __init__(self, rv, ndtype=np.longdouble):
        self.rv = rv
        self.ndtype = ndtype

    def sample(self, size=1):
        return self.rv.rvs(size=size).astype(self.ndtype)

    def sample_one(self):
        return self.rv.rvs().astype(self.ndtype)
