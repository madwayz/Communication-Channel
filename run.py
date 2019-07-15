from matplotlib import pyplot as plt
from components.DTS import digitalTransmission
from components.encryption import SimpleDEncryptor
from modules.utils import writeInFile, savePlot, createTimeLine, parseErrorChances
from modules.api import mathcadApi
from config import path
import numpy as np
import ast

if __name__ == '__main__':
    api = mathcadApi()
    np.seterr(divide='ignore')

    # Генерируем массив
    D = api.rbinom(500, 1, 0.5)

    # Создаём экземпляр класса
    dt = digitalTransmission(sigma=0.5, q=20, tau=0.1, matrix=D)

    # Создаём таймлайн модели для отрисовки на графике
    timeline = createTimeLine(0, len(D) * dt.tau - dt.Ts, dt.Ts)
    print("TIMELINE", timeline)

    """
    Получаем массив отсчетов сигнала с выхода модулятора M,
    соответствующих модельному времени.
    При подаче на вход массива
    """
    M = dt.BPSK(timeline, D)
    writeInFile(str(M), path + '\data\\bpsk.txt', 'Фазовая модуляция')
    savePlot(plt, 'p1.png', xCoords=np.array(timeline), yCoords=M, xlabel=r'$len(D) * \tau - Ts$', ylabel='BPSK(D)') # Отрисовываем график

    """
    Добавляем шум
    """
    noise = api.rnorm(len(M), 0, dt.sigma)
    M_noise = M + noise
    W = createTimeLine(len(M_noise))
    savePlot(plt, 'p2.png', xCoords=W, yCoords=M_noise, xlabel=r'len(M_noise)', ylabel='M_noise')

    """
    Детектим массив
    Выявляем ошибки
    Получаем вероятность ошибок
    """
    Y = dt.detect(M_noise)
    o = dt.getErrorChances(M, D)

    a = [1, 0, 0, 0]
    N = [
        [1, 1, 0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1]
    ]
    E = [0, 1, 1, 0, 0, 0, 0]

    T = dt.channel_encoder(a)
    R = [T[i] ^ E[i] for i in range(len(E)) if len(E) == len(T)]
    X = dt.channel_decoder(R, N)
    I = dt.coding(D)
    S = dt.decoding(D, N)

    print('Coded T:', T)
    print('R(T ^ E):', R)
    print('Decoded R:', X)
    print('T ^ X: ', sum(np.bitwise_xor(T, X)))
    print('I:', I)
    print('S:', S)

    Q1 = dt.getErrorChances(M, D, N=N, decoding=True)
    timeline = [(i + 1) / 10 for i in range(len(Q1))]
    savePlot(plt, 'p3.png', xCoords=timeline, yCoords=np.log(o), xlabel=r'$\frac{i+10}{10}$', ylabel='Вероятность ошибок')
    writeInFile(str(o), path + '\data\error_chance_q={}.txt'.format(dt.q), 'Вероятность ошибок O')
    parseErrorChances(plt, timeline)

    savePlot(plt, 'p5.png', timeline, np.log(Q1), xlabel=r'$\frac{i+10}{10}$', ylabel='Вероятность ошибок Q1')
    plt.grid()



    plaintext = np.fromfile('data\plaintext.txt', dtype='uint16')
    key = api.rbinom(8, 1, 0.5)

    den = SimpleDEncryptor()
    den.encrypt(plaintext, key)
    with open('data\cyphertext.txt', 'r+') as f:
        cypher = ast.literal_eval(f.read())
        den.decrypt(cypher, 16)