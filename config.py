from matplotlib.pyplot import *
import os

path = os.getcwd()

class GraphicSettings(object):
    def __init__(self, b_grid=False):
        grid(b_grid) # Сетка для графика
        show()
        # legend(['Модуляция', 'Тест'])