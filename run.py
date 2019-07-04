from modules.api import mathcadApi
from modules.api import Source, GraphicSettings

if __name__ == '__main__':
    api = mathcadApi()
    matrix = api.rbinom(2000, 1, 0.4)
    source = Source(debug=True)
    source.BPSK(q=20, tau=0.1, matrix=matrix)
    settings = GraphicSettings(b_grid=True)
