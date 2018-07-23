from os import listdir, path
from os.path import isfile, join

# DESCRICAO DOS CARDS PARA SELECAO DE ALGORITMOS ===============================
algos_list = [
    {'page': '/algorithms/arima',
    'title': 'ARIMA',
    'subtitle': 'Forecasting',
    'desc': 'Teste'
    },
    {'page': '/algorithms/acf',
    'title': 'Função de Autocorrelação',
    'subtitle': 'Exploratory Analysis',
    'desc': 'Esse é um teste para checar quantos caracteres conseguimos digitar nessa descrição sem ficar muito muito muito bizarríssimo demais'
    },
    {'page': '/algorithms/pacf',
    'title': 'Função de Autocorrelação Parcial',
    'subtitle': 'Exploratory Analysis',
    'desc': 'Teste2'
    }
]

# TEXTOS PARA DESCRICAO COMPLETA DE CADA ALGORITMO =============================
def longDesc():

    dirname = path.dirname(__file__)
    mypath = path.join(dirname, 'texts')

    files_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    keys = [s.split('.')[0] for s in files_list]

    values = []
    for s in files_list:
        file = open(mypath+'/'+s,'r')
        res = file.read()
        values.append(res)
        file.close()

    desc_list = dict(zip(keys, values))

    return desc_list
