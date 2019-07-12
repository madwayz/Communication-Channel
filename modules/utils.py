from matplotlib.pyplot import *
from config import img_path, path


def genText(n):
    import random
    return ''.join([chr(random.randrange(65, 90)) for _ in range(n)])


"""
На вход подаются данные для создания цикла, обёрнутые в np.arrange()
@arg1:  
"""
def createTimeLine(*args):
    return [dig for dig in np.arange(*args)]


def tolist(array):
    return np.ndarray.tolist(array)


def writeInFile(data, path, text):
    with open(path, 'w+') as f:
        f.write(data)

        print('{} был(-о/и) записан(-о/ы) в {}'.format(text, path))



def savePlot(plt, name, xCoords=None, yCoords=None, label=False):
    # if 'xLabel' in kwargs and 'yLabel' in kwargs:
    #     if kwargs['xLabel'] and kwargs['yLabel']:
    #

    if xCoords is not None and yCoords is not None:
        if label:
            plt.plot(xCoords, yCoords, label='label')
        else:
            plt.plot(xCoords, yCoords)
    else:
        plt.plot(xCoords, yCoords)

    plt.savefig(img_path + name)
    show()

    print('Сохраняю график в {}'.format(img_path + name))




def parseErrorChances(plt, timeline):
    import os
    import re
    import ast

    plt.xlabel(r'$\frac{i+10}{10}$')
    plt.ylabel('Вероятность ошибки')

    file_names = list(file_name for file_name in os.listdir(path + '\data') if re.findall(r'error_chance_q=\d+.txt', file_name))
    for file in file_names:
        with open(path + '\data\\' + file, 'r+') as f:
            file_out = ast.literal_eval(f.read())
            plt.plot(timeline, file_out, label='q={}'.format(*re.findall(r'\d+', file)))

    plt.savefig(img_path + 'p4.png')
    plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left')
    show()

    print('Сохраняю график в {}'.format(img_path + 'p4.png'))




#TODO Сделать больше информативности на графиках
