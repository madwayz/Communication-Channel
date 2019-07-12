from scipy.stats import binom
from matplotlib.pyplot import *


class mathcadApi:
    def rbinom(self, size, maxNum, p):
        return [dig for dig in binom.rvs(n=maxNum,p=p,size=size)]

    def rnorm(self, m, mew, sigma):
        return np.random.normal(mew, sigma, m)

    def stack(self, a, b):
        return np.stack((a, b))

    def submatrix(self, matrix, line1, line2, column1, column2):
        if line1 > line2:
            raise Exception('2 аргумент должен быть меньше 3 аргумента')

        if column1 > column2:
            raise Exception('4 аргумент должен быть меньше 5 аргумента')

        if line1 == line2 == column1 == column2 == 0:
            raise Exception('Один из аргументов должен быть положительным')

        # Проверка на вектор
        lines = 0 # Если останется 0, то это вектор
        for i in matrix:
            if type(i) == list:
                lines += 1

        if line1 > lines or line2 > lines:
            raise Exception('Один из аргументов больше высоты матрицы. Возможно, была передан вектор')

        if not lines: #  То это вектор
            if line1 == line2 == 0:
                return matrix[column1:column2 + 1]

        return [matrix[line][column1:column2+1] for line in range(line1, line2+1)]

    def last(self, matrix):
        #Подсчитываем кол-во списков внутри главного списка
        count = 0
        for i in matrix:
            if type(i) == list:
                count += 1

            if count > 1:
                raise Exception('Длину последнего элементам узнать можно только в векторе')

        return len(matrix) - 1


    def getErrors(self, m1, m2):
        return sum([m1[i] ^ m2[i] for i in range(len(m1)) if len(m1) == len(m2)])

    def getErrorChance(self, m1, m2):
        return sum([m1[i] ^ m2[i] for i in range(len(m1)) if len(m1) == len(m2)]) / len(m1)