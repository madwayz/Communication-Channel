from modules.api import mathcadApi
from config import GraphicSettings
from components.source import digitalTransmission

if __name__ == '__main__':
    api = mathcadApi()
    matrix = api.rbinom(1000, 1, 0.5)

    # Запускаем источник
    dT = digitalTransmission(sigma=0.5, q=20, tau=0.1, matrix=matrix)
    dT.start()

    settings = GraphicSettings(b_grid=True)
