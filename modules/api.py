from scipy.stats import binom
from matplotlib.pyplot import *
class mathcadApi:
    def rbinom(self, size, maxNum, p):
        return [dig for dig in binom.rvs(n=maxNum,p=p,size=size)]

    def rnorm(self, m, mew, sigma):
        return np.random.normal(mew, sigma, m)

