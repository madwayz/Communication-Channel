from matplotlib.pyplot import *
from config import img_path

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