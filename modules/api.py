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
        if type(a[0]) == list and type(b[0]) == list:
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
        if len(m1) < len(m2):
            return sum([m1[i] ^ m2[i] for i in range(len(m1))])
        else:
            return sum([m1[i] ^ m2[i] for i in range(len(m2))])

    def getErrorChance(self, m1, m2):
        if len(m1) < len(m2):
            return sum([m1[i] ^ m2[i] for i in range(len(m1))]) / len(m1)
        else:
            return sum([m1[i] ^ m2[i] for i in range(len(m2))]) / len(m1)