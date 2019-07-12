from matplotlib import pyplot as plt
from components.source import digitalTransmission
from modules.utils import writeInFile, savePlot, createTimeLine, parseErrorChances
from modules.api import mathcadApi
from config import path
import numpy as np

if __name__ == '__main__':
    api = mathcadApi()

    # Генерируем массив
    D = api.rbinom(1000, 1, 0.5)

    # Запускаем источник

    dt = digitalTransmission(sigma=0.5, q=20, tau=0.1, matrix=D)

    # Создаём таймлайн для отрисовки на графике
    timeline = createTimeLine(0, len(D) * dt.tau - dt.Ts, dt.Ts)  # Модельное время
    print("TIMELINE", timeline)

    """
    Получаем массив отсчетов сигнала с выхода модулятора M, 
    соответствующих модельному времени.
    При подаче на вход массива
    """
    M = dt.BPSK(timeline, D)
    writeInFile(str(M), path + '\data\\bpsk.txt', 'Фазовая модуляция')
    savePlot(plt, 'p1.png', xCoords=np.array(timeline), yCoords=M) # Отрисовываем график

    """
    Добавляем шум
    """
    noise = api.rnorm(len(M), 0, dt.sigma)
    M_noise = M + noise
    W = createTimeLine(len(M_noise))
    savePlot(plt, 'p2.png', xCoords=W, yCoords=M_noise)

    """
    Детектим массив
    Выявляем ошибки
    Получаем вероятность ошибок
    """
    Y = dt.detect(M_noise)
    o = dt.errorChances(M, D)

    timeline = [(i + 1) / 10 for i in range(len(o))]
    savePlot(plt, 'p3.png', xCoords=timeline, yCoords=o)
    writeInFile(str(o), path + '\data\error_chance_q={}.txt'.format(dt.q), 'Вероятность ошибок')
    parseErrorChances(plt, timeline)

    a = [1, 0, 0, 0]
    T = dt.coder(a)
    print(T)

    plt.grid()
