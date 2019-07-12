from matplotlib import pyplot as plt
from modules.utils import writeInFile, savePlot, tolist, createTimeLine
from modules.api import mathcadApi
from config import path
import numpy as np

class digitalTransmission(object):
    def __init__(self, sigma, q, tau, matrix):
        self.sigma = sigma
        self.q = q # Количество семплов
        self.tau = tau # Единичное время
        self.matrix = matrix
        self.period = self.tau  # Период несущего колебания
        self.Ts = self.period / self.q  # Период дескритизации

    def coder(self, t):
        t.insert(4, t[0] ^ t[1] ^ t[3])
        t.insert(5, t[0] ^ t[2] ^ t[3])
        t.insert(6, t[1] ^ t[2] ^ t[3])
        return t

    def decoder(self, R):
        api = mathcadApi()

        b = list()
        b.insert(0, R[0] ^ R[1] ^ R[3] ^ R[4])
        b.insert(1, R[0] ^ R[2] ^ R[3] ^ R[5])
        b.insert(2, R[1] ^ R[2] ^ R[3] ^ R[6])
        _sum = sum([x for x in range(3)])
        if _sum != 0:
            for i in range(3):
                if sum(R[i] ^ b) == 0:
                    R[i] = R[i] ^ 1
            api.submatrix(R, 0, 3, 0, 0)


    # Модель BPSK модулятора
    def BPSK(self, time, matrix):
        cSignals = list()

        print('Пожалуйста, подождите. Записываем массив отсчётов сигнала')
        for descrPeriod in time:  # Период дескритизации
            i = int(np.floor(descrPeriod/self.tau))
            if matrix[i] < 0.1:
                phi = 0
            else:
                phi = np.pi

            cSignals.append(np.sin(2 * np.pi * descrPeriod / self.period + phi))
            # if self.debug: print('[PHI: {}]'.format(phi))

        return cSignals

    def detect(self, M_noise):
        M_noise = tolist(M_noise)
        length = int(np.round(len(M_noise) / self.q))
        for i in range(length):
            a = 0
            b = 0
            for k in range(i * self.q, self.q * (i + 1)-1):
                a += M_noise[k] * np.sin(2 * np.pi * k * self.Ts / self.period)
                b += M_noise[k] * np.sin(np.pi  + 2 * np.pi * k * self.Ts / self.period)

            if a < b:
                M_noise[i] = 1
            else:
                M_noise[i] = 0

        return M_noise[:length:]

    def errorChances(self, M, D):
        api = mathcadApi()
        P = list()
        for i in range(25):
            sigma = 0.1 + 0.1 * i
            N = api.rnorm(len(M), 0, sigma)
            H = M + N
            R = self.detect(H)
            P.insert(i, api.getErrorChance(D, R))
        return P