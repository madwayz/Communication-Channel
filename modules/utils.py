def genText(n):
    import random
    return ''.join([chr(random.randrange(65, 90)) for _ in range(n)])


def writeInFile(path, text):
    with open(path, 'w+') as f:
        f.write(path)
        print('{} был(-о) записан(-о) в {}'.format(text, path))