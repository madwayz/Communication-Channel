from modules.api import mathcadApi
import numpy as np

class SimpleDEncryptor:
    def encrypt(self, plaintext, key):
        api = mathcadApi()
        DV = api.dec2binM(plaintext, 16)
        k = list()
        CS = list()
        v = list()
        for i in range(int(len(DV) / 8 - 1)):
            h = 0
            for j in range(8*i, 8*(i+1)-1):
                k.insert(h, int(DV[j]))
                h += 1

            length = len(k) if len(k) < len(key) else len(key)
            for f in range(length):
                v.append(int(k[f] ^ key[f]))

            CS = np.array(api.stack(CS, v)).astype(np.int).tolist()
        cypher = api.submatrix(CS, 1, api.last(CS), 0, 0)
        with open('data\cyphertext.txt', 'w+') as f:
            f.write(str(cypher))
        print(cypher)

    def decrypt(self, cyphertext, j):
        api = mathcadApi()
        print(api.bin2dec(cyphertext, j))

