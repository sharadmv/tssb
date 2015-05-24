import numpy as np
import scipy.stats as stats

from dist import Distribution
from process import IndependentRandomProcess, MarkovTreeRandomProcess
from tssb import TSSB, depth_weight

class RandomMeasure(Distribution):

    def sample_one(self):
        raise NotImplementedError

class RandomCountingMeasure(RandomMeasure):

    def __init__(self, weights, base_measure):
        self.weights = weights
        self.base_measure = base_measure
        self.objects = IndependentRandomProcess(self.base_measure)

    def uniform_index(self, u):
        return self.weights.uniform_index(u)

    def sample_one(self):
        index = self.weights.sample_one()
        return (index, self.objects[index])

    def __getitem__(self, key):
        return self.objects[key]

class TreeRandomMeasure(RandomCountingMeasure):

    def __init__(self, weights, base_measure, transition_measure):
        self.weights = weights
        self.base_measure = base_measure
        self.transition_measure = transition_measure
        self.objects = MarkovTreeRandomProcess(self.base_measure, self.transition_measure)

def create_gaussian_trm(eta, cov, prior):

    def initial():
        return (prior.sample(), cov)

    def next(prev):
        mean, cov = prev
        return (stats.multivariate_normal(mean=mean, cov=cov).rvs(), cov)

    tssb = TSSB(alpha=depth_weight(25, 1), gamma=1)
    return TreeRandomMeasure(tssb, next, initial)

if __name__ == "__main__":
    from util import ScipySampler
    t = create_gaussian_trm(1, np.eye(2)/1000.0, ScipySampler(stats.multivariate_normal([0, 0], np.eye(2))))
