from scipy.stats import binom
from modules.utils import tolist
from matplotlib.pyplot import *


class mathcadApi:
    def rbinom(self, size, maxNum, p):
        return [dig for dig in binom.rvs(n=maxNum,p=p,size=size)]

    def rnorm(self, m, mew, sigma):
        return np.random.normal(mew, sigma, m)

    def stack(self, a, b):
        vector_count = 0
        array_count = 0

        if list in a and list in b:
            array_count += 1
        else:
            vector_count += 1

        if array_count:
            return tolist(np.stack((a, b)))
        elif vector_count:
            return tolist(np.concatenate((a, b), axis=None))

    def submatrix(self, matrix, column1, column2, line1, line2):
        if line1 > line2:
            raise Exception('2 аргумент должен быть меньше 3 аргумента')

        if column1 > column2:
            raise Exception('4 аргумент должен быть меньше 5 аргумента')

        # Проверка на вектор
        lines = 0 # Если останется 0, то это вектор
        for i in matrix:
            if type(i) == list:
                lines += 1


        if not lines: #  То это вектор
            if line1 == line2 == 0:
                return matrix[column1:column2 + 1]

        return [matrix[line][column1:column2+1] for line in range(line1, line2+1)]

    def subcolumn(self, matrix, column):
        matrix_tmp = list()
        for x in self.submatrix(matrix, column, column, 0, len(matrix) - 1):
            matrix_tmp.append(*x)

        return matrix_tmp

    def last(self, matrix):
        #Подсчитываем кол-во списков внутри главного списка
        count = 0
        for i in matrix:
            if type(i) == list:
                count += 1

            if count > 1:
                raise Exception('Длину последнего элемента узнать можно только в векторе')

        return len(matrix) - 1

    def getErrors(self, m1, m2):
        length = len(m1) if len(m1) < len(m2) else len(m2)
        return sum([m1[i] ^ m2[i] for i in range(length)])

    def getErrorChance(self, m1, m2):
        length = len(m1) if len(m1) < len(m2) else len(m2)
        return sum([m1[i] ^ m2[i] for i in range(length)]) / len(m1)

    def dec2bin(self, x, n):
        N = list()
        for i in range(n - 1):
            if x >= pow(2, n - 1 - i):
                N.insert(i, 1)
                x += pow(-2, n - 1 - i)
            N.insert(i, 0)
        return N

    def dec2binM(self, x, n):
        api = mathcadApi()
        k = list()
        for i in range(1, api.last(x)):
            k = api.stack(k, self.dec2bin(x[i], n))
        return api.submatrix(k, 1, api.last(k), 0, 0)

    def bin2dec(self, t, j):
        api = mathcadApi()
        B = list()
        for i in range(int(len(t) / j - 1)):
            B.insert(i, self.bin2decM(api.submatrix(t, j * i, j * (i + 1) - 1, 0, 0)))
        return B

    def bin2decM(self, x):
        s = 0
        for i in range(len(x) - 1):
            s += x[i] * pow(2, len(x) - i - 1)
        return s