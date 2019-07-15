from modules.utils import tolist
from modules.api import mathcadApi
import numpy as np

class digitalTransmission(object):
    def __init__(self, sigma, q, tau, matrix):
        self.sigma = sigma  # Среднеквадратическое отклонение для шума
        self.q = q  # Количество семплов
        self.tau = tau  # Единичное время
        self.matrix = matrix  # Входная матрица
        self.period = self.tau  # Период несущего колебания
        self.Ts = self.period / self.q  # Период семплирования
        self.k = 4
        self.n = 7

    def channel_encoder(self, t):
        t.insert(4, t[0] ^ t[1] ^ t[3])
        t.insert(5, t[0] ^ t[2] ^ t[3])
        t.insert(6, t[1] ^ t[2] ^ t[3])
        #print(t)
        return t

    def channel_decoder(self, T, N):
        api = mathcadApi()
        #print('T', T)
        b = list()
        b.insert(0, T[0] ^ T[1] ^ T[3] ^ T[4])
        b.insert(1, T[0] ^ T[2] ^ T[3] ^ T[5])
        b.insert(2, T[1] ^ T[2] ^ T[3] ^ T[6])
        if sum(b[:3]) != 0:
            for j in range(7):
                column = api.subcolumn(N, j)
                if sum(np.logical_xor(column, b)) == 0:
                    T[j] ^= 1
        return T

    def coding(self, matrix):
        api = mathcadApi()
        c = self.channel_encoder(api.submatrix(matrix, 0, 3, 0, 0))
        for j in range(1, int(np.floor(len(matrix)/self.k))-1):
            b = self.channel_encoder(api.submatrix(matrix, self.k * j, self.k * j + (self.k - 1), 0, 0))
            c = api.stack(c, b)
        return c

    def decoding(self, matrix, N):
        api = mathcadApi()
        c = self.channel_decoder(api.submatrix(matrix, 0, 6, 0, 0), N)
        for p in range(1, int(np.floor(len(matrix)/self.n))-1):
            a = self.channel_decoder(api.submatrix(matrix, p * self.n, (p + 1) * self.n - 1, 0, 0), N)
            c = api.stack(c, a)
        return c

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

    def getErrorChances(self, M, D, decoding=False, **kwargs):
        api = mathcadApi()
        P = list()
        for i in range(25):
            sigma = (i + 1) / 10
            N = api.rnorm(len(M), 0, sigma)
            H = M + N
            R = self.detect(H)
            if decoding:
                F = self.decoding(R, kwargs['N'])
                P.insert(i, api.getErrorChance(D, F))
            else:
                P.insert(i, api.getErrorChance(D, R))
        return P