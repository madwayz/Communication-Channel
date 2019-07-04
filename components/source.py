from matplotlib.pyplot import *
from modules.utils import writeInFile
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
        self.fig = Figure()

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
        for i in range(int(np.floor(len(self.matrix) / self.q)) - 1):
            _min = self.q * i
            _max = (self.q * i) + (self.q - 1)
            for j in range(_min, _max):
                a = signalsWithNoise[j] * np.sin(2 * np.pi / self.period * (j * self.Ts) + np.pi)
                b = signalsWithNoise[j] * np.sin(2 * np.pi / self.period * (j * self.Ts))
                if a > b:
                    signalsWithNoise[i] = 1
                else:
                    signalsWithNoise[i] = 0
        print(signalsWithNoise)
        return signalsWithNoise

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
        plot(cSignals, np.array(self.time)) # Отрисовываем график
        savefig(path + '/data/plots/p1.png')
        print('Сохраняю график в {}/data/plots/'.format(path))



        """
        Добавляем шум
        """
        api = mathcadApi()
        noise = api.rnorm(len(cSignals), 0, self.sigma)
        signalsWithNoise = np.ndarray.tolist(cSignals + noise)
        W = [i for i in range(len(list(signalsWithNoise)))]
        cla()
        plot(W, signalsWithNoise)
        savefig(path + '/data/plots/p2.png')
        print('Сохраняю график в {}/data/plots/'.format(path))
        #self.detect(signalsWithNoise)