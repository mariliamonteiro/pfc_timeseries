from os import listdir, path
from os.path import isfile, join
import re
import codecs
from flask import Markup

dir = path.dirname(__file__)

# DESCRICAO DOS CARDS PARA SELECAO DE ALGORITMOS ===============================

def shortDesc():

    mypath = path.join(dir, 'static','texts_short')

    files_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    desc_list = []
    for s in files_list:
        file = codecs.open(mypath+'/'+s, encoding='utf-8', mode='r')
        res = file.readlines()
        res = dict([re.split('\s*: \s*|\s*:\s*', s.strip()) for s in res[:4]])
        res['page'] = '/algorithms/' + res['page']

        desc_list.append(res)
        file.close()

    return desc_list

# DESCRICAO DOS CARDS PARA SELECAO DE ALGORITMOS COMO DICIONÁRIO DE DICIONÁRIOS

def shortDescDicionario():

    mypath = path.join(dir, 'static','texts_short')

    files_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    desc_list = {}
    for s in files_list:
        file = codecs.open(mypath+'/'+s, encoding='utf-8', mode='r')
        res = file.readlines()
        res = dict([re.split('\s*: \s*|\s*:\s*', s.strip()) for s in res[:4]])
        res['page'] = '/algorithms/' + res['page']
        desc_list[s.split('.')[0]] = res
        file.close()

    return desc_list

# TEXTOS PARA DESCRICAO COMPLETA DE CADA ALGORITMO =============================
def longDesc():

    mypath = path.join(dir, 'static','texts_long')

    files_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    keys = [s.split('.')[0] for s in files_list]

    values = []
    for s in files_list:
        file = codecs.open(mypath+'/'+s, encoding='utf-8', mode='r')
        res = file.read()
        values.append(Markup(res))
        file.close()

    desc_list = dict(zip(keys, values))

    return desc_list
