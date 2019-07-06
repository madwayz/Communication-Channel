from matplotlib import pyplot as plt
import numpy as np
from modules.utils import writeInFile, savePlot, tolist
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

        #return np.array(cSignals)
        return cSignals

    def detect(self, signalsWithNoise):
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


        writeInFile(str(signalsWithNoise[:length:]), path + '\data\detected_signals.txt', 'Проверенные детектором сигналы')
        return signalsWithNoise[:length:]
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
        #         [Период дискретизации] {}
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


        """
        Детектим массив
        """
        matrix2 = self.detect(signalsWithNoise)
        #matrix2 = api.rbinom(1000, 1, 0.2)
        print(matrix2)
        print(self.matrix)
        print('Кол-во ошибок:', api.getErrors(self.matrix, matrix2))
        print('Вероятность ошибок:', api.getErrorChance(self.matrix, matrix2))