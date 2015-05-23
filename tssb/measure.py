from dist import Distribution
from stream import RandomStream

class RandomMeasure(Distribution):

    def sample_one(self):
        raise NotImplementedError

class RandomCountingMeasure(RandomMeasure):

    def __init__(self, weights, base_measure):
        self.weights = weights
        self.base_measure = base_measure
        self.objects = RandomStream(self.base_measure)

    def uniform_index(self, u):
        return self.weights.uniform_index(u)

    def sample_one(self):
        return self[self.weights.sample_one()]

    def __getitem__(self, key):
        return self.objects[key]
