from scipy.stats import binom
from matplotlib.pyplot import *


class mathcadApi:
    def rbinom(self, size, maxNum, p):
        return [dig for dig in binom.rvs(n=maxNum,p=p,size=size)]

    def rnorm(self, m, mew, sigma):
        return np.random.normal(mew, sigma, m)

    def getErrors(self, m1, m2):
        return sum([m1[i] ^ m2[i] for i in range(len(m1)) if len(m1) == len(m2)])

    def getErrorChance(self, m1, m2):
        return sum([m1[i] ^ m2[i] for i in range(len(m1)) if len(m1) == len(m2)]) / len(m1)