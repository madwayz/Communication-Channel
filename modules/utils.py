def genText(n):
    import random
    return ''.join([chr(random.randrange(65, 90)) for _ in range(n)])