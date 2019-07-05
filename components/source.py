from matplotlib import pyplot as plt
import numpy as np
from modules.utils import writeInFile, savePlot
from modules.api import mathcadApi
from config import path


class digitalTransmission(object):
    def __init__(self, sigma, q, tau, matrix):
        self.sigma = sigma
        self.q = q
        self.tau = tau
        self.matrix = matrix
        self.period = self.tau  # Период несущего колебания
        self.Ts = self.period / self.q  # Период дескритизации
        self.time = [dig for dig in np.arange(0, len(self.matrix) * self.tau - self.Ts, self.Ts)]  # Модельное время

    # Модель BPSK модулятора
    def BPSK(self):
        count = 0
        cSignals = list()
        print('Пожалуйста, подождите. Записываем массив отсчётов сигнала')
        for descrPeriod in self.time:  # Период дескритизации
            i = int(np.floor(descrPeriod / self.tau))
            if self.matrix[i] == 0:
                phi = 0
            else:
                phi = np.pi

            cSignals.append(np.sin(2 * np.pi * descrPeriod / self.period + phi))
            count += 1
            # if self.debug: print('[PHI: {}]'.format(phi))

        writeInFile(str(cSignals), path + '\data\count_signals.txt', 'Отсчёты сигналов')

        # for k, v in M:
        #     print('''
        #     [Отсчёты сигналов]
        #     {} - {}
        #     '''.format(k, v))

        return np.array(cSignals)

    def detect(self, signalsWithNoise):
        #signalsWithNoise = np.ndarray.tolist(signalsWithNoise)
        print(np.floor(len(signalsWithNoise)))
        #length = int(np.floor(len(signalsWithNoise) / self.q)) - 1
        a = 0
        b = 0
        for i in range(int(len(signalsWithNoise) / self.q) - 1):
            _min = self.q * i
            _max = (self.q * i) + (self.q - 1)
            for j in range(_min, _max):
                j = _min
                a += signalsWithNoise[j] * np.sin(2 * np.pi / self.period * (j * self.Ts) + np.pi)
                b += signalsWithNoise[j] * np.sin(2 * np.pi / self.period * (j * self.Ts))
                if a > b:
                    signalsWithNoise[i] = 1
                else:
                    signalsWithNoise[i] = 0

        writeInFile(str(signalsWithNoise), path + '\data\detected_signals.txt', 'Проверенные детектором сигналы')
        print(signalsWithNoise[:int(len(signalsWithNoise))-1:])
        return signalsWithNoise[:int(len(signalsWithNoise))-1:]
    #TODO: Пофиксить сумму
    #TODO: Доделать чекер

    # def errorChecker(self):
    #     api = mathcadApi()
    #
    #     for i in range(1, 25):
    #         sigma = i+1/10
    #         N = api.rnorm(len(self.matrix), 0, sigma)
    #         H =

    def start(self):
        # title('Модель цифровой системы передачи')
        # xlabel('Модельное время')
        # ylabel('Амлитуда модуляции')

        # if self.debug:
        #     print('''
        #         [Период дескритизации] {}
        #         [Период несущего колебания] {}
        #     '''.format(Ts, T))

        writeInFile(str(self.time), path + '\data\model_text.dat', 'Модельное время')

        """
        Получить массив отсчетов сигнала с выхода модулятора M, 
        соответствующих модельному времени. 
        При подаче на вход массива
        """
        cSignals = self.BPSK()
        savePlot(plt, 'p1.png', cSignals, np.array(self.time))


        """
        Добавляем шум
        """
        api = mathcadApi()
        noise = api.rnorm(len(cSignals), 0, self.sigma)
        signalsWithNoise = cSignals + noise

        W = [i for i in range(len(signalsWithNoise))]
        savePlot(plt, 'p2.png', W, signalsWithNoise)
        self.detect(signalsWithNoise)