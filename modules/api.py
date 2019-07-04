from matplotlib.pyplot import *
from scipy.stats import binom

class mathcadApi:
    def rbinom(self, size, maxNum, p):
        return [dig for dig in binom.rvs(n=maxNum,p=p,size=size)]

class Source:
    def __init__(self, debug=False):
        self.debug = debug

    # Модель BPSK модулятора
    def BPSK(self, q, tau, matrix):
        # title('Фазовая модуляция')
        # xlabel('Время')
        # ylabel('Амлитуда модуляции')

        phi = None
        T = tau # Период несущего колебания
        Ts = T / q # Период дескритизации
        t = [dig for dig in np.arange(0, len(matrix) * tau - Ts, Ts)] # Модельное время
        if self.debug: print('''
            [Модельное время] {}
            [Период дескритизации] {}
            [Период несущего колебания] {}
        '''.format(t, Ts, T))


        #ReqByTime = [int(dig) for dig in t / Ts]
        for descrPeriod in t: # Период дескритизации
            i = int(np.floor(descrPeriod/tau))
            if matrix[int(np.floor(descrPeriod/T))] == 0: phi = 0
            else: phi = np.pi

        if self.debug: print('[]')
        plot(np.sin(2*np.pi * t/T + phi))

class GraphicSettings(object):
    def __init__(self, b_grid=False):
        grid(b_grid) # Сетка для графика
        show()
        # legend(['Модуляция', 'Тест'])