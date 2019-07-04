from matplotlib.pyplot import *
from scipy.stats import binom
from modules.utils import writeInFile
import os

class mathcadApi:
    def rbinom(self, size, maxNum, p):
        return [dig for dig in binom.rvs(n=maxNum,p=p,size=size)]

class Source:
    def __init__(self, debug=False):
        self.debug = debug

    # Модель BPSK модулятора
    def BPSK(self, q, tau, matrix):
        title('BPSK модулятор')
        xlabel('Модельное время')
        ylabel('Амлитуда модуляции')

        T = tau # Период несущего колебания
        Ts = T / q # Период дескритизации
        t = [dig for dig in np.arange(0, len(matrix) * tau - Ts, Ts)] # Модельное время
        if self.debug:
            print('''
                [Период дескритизации] {}
                [Период несущего колебания] {}
            '''.format(Ts, T))

        path = os.getcwd()
        writeInFile(str(t), path + '\data\model_text.dat', 'Модельное время')

        """
        Получить массив отсчетов сигнала с выхода модулятора M, 
        соответствующих модельному времени. 
        При подаче на вход массива
        """
        M = list()
        count = 0
        print('Пожалуйста, подождите. Записываем массив отсчётов сигнала')
        for descrPeriod in t: # Период дескритизации
            i = int(np.floor(descrPeriod/tau))
            if matrix[i] == 0: phi = 0
            else: phi = np.pi

            M.append([np.sin(2*np.pi * descrPeriod/T + phi)])
            count += 1
            #if self.debug: print('[PHI: {}]'.format(phi))

        writeInFile(str(M), path + '\data\count_signals.txt', 'Отсчёты сигналов')

        if self.debug:
            for k, v in M:
                print('{} - {}'.format(k, v))

        plot(np.array(M), np.array(t))


class GraphicSettings(object):
    def __init__(self, b_grid=False):
        grid(b_grid) # Сетка для графика
        show()
        # legend(['Модуляция', 'Тест'])