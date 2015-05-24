import numpy as np
import scipy.stats as stats

from dist import Distribution
from gem import LazyGEM

def depth_weight(a, l):
    def dpw(j):
        return l ** j * a
    return dpw

class TSSB(Distribution):

    def __init__(self, index=(), depth=0, alpha=depth_weight(1.0, 0.5), gamma=0.2):
        self.index = index
        self.depth = depth
        self.alpha = alpha
        self.gamma = gamma
        self.nu = stats.beta(1, self.alpha(self.depth)).rvs()
        self.psi = LazyGEM(self.gamma)
        self.children = []
        self.cur_index = -1

    def get_child(self, key):
        if self.cur_index < key:
            while self.cur_index < key:
                self.cur_index += 1
                self.children.append(TSSB(
                    index=self.index + (self.cur_index,),
                    depth=self.depth + 1,
                    alpha=self.alpha,
                    gamma=self.gamma
                ))
        return self.children[key]

    def uniform_index(self, u):
        if u < self.nu:
            return self.index
        u = (u - self.nu) / (1.0 - self.nu)
        i, right_weight = self.psi.uniform_index(u)
        child, weight = self.get_child(i), self.psi[i]
        left_weight = right_weight - weight
        u = (u - left_weight) / (weight)
        return child.uniform_index(u)

    def sample_one(self):
        return self.uniform_index(np.random.random())

    def __repr__(self):
        if self.index:
            return '-'.join(map(str, self.index))
        return '-'

if __name__ == "__main__":
    t = TSSB(alpha=depth_weight(1, 1), gamma=1)
