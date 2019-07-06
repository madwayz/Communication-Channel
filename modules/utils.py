from matplotlib.pyplot import *
from config import img_path, path

def genText(n):
    import random
    return ''.join([chr(random.randrange(65, 90)) for _ in range(n)])


def writeInFile(data, path, text):
    with open(path, 'w+') as f:
        f.write(data)
        print('{} был(-о/и) записан(-о/ы) в {}'.format(text, path))


def savePlot(plt, name, x_coords, y_coords, clear=True):
    if clear:
        plt.cla()

    plt.plot(x_coords, y_coords)
    plt.savefig(img_path + name)
    print('Сохраняю график в {}'.format(img_path + name))


def tolist(array):
    return np.ndarray.tolist(array)


def parseErrorChances(plt, timeline):
    import os
    import re
    import ast

    file_names = list(file_name for file_name in os.listdir(path + '\data') if re.findall(r'error_chance_q=\d+.txt', file_name))
    for i in range(4, 4 + len(file_names)):
        for file in file_names:
            with open(path + '\data\\' + file, 'r+') as f:
                file_out = ast.literal_eval(f.read())
                savePlot(plt, 'p{}.png'.format(i), timeline, np.array(file_out), clear=False)