from matplotlib.pyplot import *

def genText(n):
    import random
    return ''.join([chr(random.randrange(65, 90)) for _ in range(n)])


def writeInFile(data, path, text):
    with open(path, 'w+') as f:
        f.write(data)
        print('{} был(-о/и) записан(-о/ы) в {}'.format(text, path))


