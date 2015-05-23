class Distribution(object):

    def sample(self, size=None):
        if not size:
            return self.sample_one()
        else:
            samples = [0] * size
            for i in xrange(size):
                samples[i] = self.sample_one()
            return  samples

    def sample_one(self):
        raise NotImplementedError
