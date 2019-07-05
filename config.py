from matplotlib.pyplot import *
import os

path = os.getcwd()
img_path = os.getcwd() + '\data\plots\\'

class GraphicSettings(object):
    def __init__(self, b_grid=False):
        grid(b_grid) # Сетка для графика
        show()
        # legend(['Модуляция', 'Тест'])