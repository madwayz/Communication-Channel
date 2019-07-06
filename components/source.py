from matplotlib import pyplot as plt
import numpy as np
from modules.utils import writeInFile, savePlot, parseErrorChances
from modules.api import mathcadApi
from config import path


class digitalTransmission(object):
    def __init__(self, sigma, q, tau, matrix):
        self.sigma = sigma
        self.q = q
        self.tau = tau
        self.matrix = matrix
        self.cSignals = list()
        self.period = self.tau  # Период несущего колебания
        self.Ts = self.period / self.q  # Период дескритизации
        self.time = [dig for dig in np.arange(0, len(self.matrix) * self.tau - self.Ts, self.Ts)]  # Модельное время

    # Модель BPSK модулятора
    def BPSK(self):
        cSignals = list()
        print('Пожалуйста, подождите. Записываем массив отсчётов сигнала')
        for descrPeriod in self.time:  # Период дескритизации
            i = int(np.floor(descrPeriod / self.tau))
            if self.matrix[i] == 0:
                phi = 0
            else:
                phi = np.pi

            cSignals.append(np.sin(2 * np.pi * descrPeriod / self.period + phi))
            # if self.debug: print('[PHI: {}]'.format(phi))

        writeInFile(str(cSignals), path + '\data\count_signals.txt', 'Отсчёты сигналов')

        return cSignals

    def detect(self, signalsWithNoise, write=True):
        signalsWithNoise = np.ndarray.tolist(signalsWithNoise)
        length = int(np.floor(len(signalsWithNoise) / self.q)) + 1
        for i in range(length):
            a = 0
            b = 0
            for k in range(i * self.q, self.q * (i + 1)-1):
                a += signalsWithNoise[k] * np.sin(2 * np.pi * (k * self.Ts / self.period))
                b += signalsWithNoise[k] * np.sin(np.pi  + 2 * np.pi * (k * self.Ts) / self.period)
                if a < b:
                    signalsWithNoise[i] = 1
                else:
                    signalsWithNoise[i] = 0

        if write:
            writeInFile(str(signalsWithNoise[:length:]), path + '\data\detected_signals.txt', 'Проверенные детектором сигналы')

        return signalsWithNoise[:length:]

    def errorChances(self, cSignals):
        api = mathcadApi()
        P = list()
        for i in range(1, 25):
            sigma = (i + 1) / 10
            N = api.rnorm(len(cSignals), 0, sigma)
            H = cSignals + N
            R = self.detect(H, write=False)
            P.insert(i, api.getErrorChance(R, self.matrix))
        return P

    def start(self):
        print(''
            '[Период дискретизации: {}]\n' \
            '[Период несущего колебания {}]'.format(self.Ts, self.period))

        writeInFile(str(self.time), path + '\data\model_text.dat', 'Модельное время')

        """
        Получаем массив отсчетов сигнала с выхода модулятора M, 
        соответствующих модельному времени.
        При подаче на вход массива
        """
        cSignals = self.BPSK()
        savePlot(plt, 'p1.png', np.array(self.time), cSignals)

        """
        Добавляем шум
        """
        api = mathcadApi()
        noise = api.rnorm(len(cSignals), 0, self.sigma)
        signalsWithNoise = cSignals + noise
        W = [i for i in range(len(signalsWithNoise))]
        savePlot(plt, 'p2.png', W, signalsWithNoise)

        """
        Детектим массив
        Выявляем ошибки
        Получаем вероятность ошибок
        """
        matrix2 = self.detect(signalsWithNoise)
        print('[Кол-во ошибок: {}]'.format(api.getErrors(self.matrix, matrix2)))
        print('[Вероятность ошибок: {}]'.format(api.getErrorChance(self.matrix, matrix2)))

        o = self.errorChances(cSignals)

        timeline = [(i + 1) / 10 for i in range(len(o))]
        savePlot(plt, 'p3.png', timeline, o)
        writeInFile(str(o), path + '\data\error_chance_q={}.txt'.format(self.q), 'Шансы ошибок')

        parseErrorChances(plt, timeline)
