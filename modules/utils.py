from matplotlib.pyplot import *
from config import img_path, path
import os
import re
import ast


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



def savePlot(plt, name, xCoords=None, yCoords=None, label=None, xlabel=None, ylabel=None):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if xCoords is not None and yCoords is not None:
        if label is not None:
            plt.plot(xCoords, yCoords, label=label)
        else:
            plt.plot(xCoords, yCoords)
    else:
        plt.plot(xCoords, yCoords)

    if label is not None:
        plt.legend(bbox_to_anchor=(1.01, 0.15), loc='right')
    plt.savefig(img_path + name)
    show()

    print('Сохраняю график в {}'.format(img_path + name))


def parseErrorChances(plt, timeline):
    plt.xlabel(r'$\frac{i+10}{10}$')
    plt.ylabel('Вероятность ошибок O')

    file_names = list(file_name for file_name in os.listdir(path + '\data') if re.findall(r'error_chance_q=\d+.txt', file_name))
    for file in file_names:
        with open(path + '\data\\' + file, 'r+') as f:
            file_out = ast.literal_eval(f.read())
            plt.plot(timeline, np.log(file_out), label='q={}'.format(*re.findall(r'\d+', file)))

    plt.legend(bbox_to_anchor=(1.01, 0.14), loc='right')
    plt.savefig(img_path + 'p4.png')

    show()
    print('Сохраняю график в {}'.format(img_path + 'p4.png'))