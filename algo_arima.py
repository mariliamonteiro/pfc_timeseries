import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
import secrets
import os
import pandas as pd
from flask import Markup

UPLOAD_FOLDER = 'temp_files'

def individual_data(tables, p, q):
    csv = tables.as_csv()
    lista = csv.replace('\n',',').replace(' ','').split(',')
    elementos = {'titulo': lista[1],
                 'n_obs': lista[3],
                 'modelo': lista[6]+','+lista[7]+','+lista[8],
                 'LogLikelihood': lista[10],
                 'metodo': lista[12],
                 'data': lista[17],
                 'AIC': lista[19],
                 'BIC': lista[23],
                 'HQIC': lista[27],

                 'coef_const': lista[40],
                 'std_err_const': lista[41],
                 'z_const': lista[42],
                 'P>|z|_const': lista[43],
                 '0.025_const': lista[44],
                 '0.975_const': lista[45]
                 }
    index = 46
    for i in range(p):
        index +=1
        elementos['coef_ar.L%s'%(i+1)] = lista[index]; index +=1
        elementos['std_err_ar.L%s'%(i+1)] =  lista[index]; index +=1
        elementos['z_ar.L%s'%(i+1)] = lista[index]; index +=1
        elementos['P>|z|_ar.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.025_ar.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.975_ar.L%s'%(i+1)] = lista[index]; index +=1

    for i in range(q):
        index+=1
        elementos['coef_ma.L%s'%(i+1)] = lista[index]; index +=1
        elementos['std_err_ma.L%s'%(i+1)] =  lista[index]; index +=1
        elementos['z_ma.L%s'%(i+1)] = lista[index]; index +=1
        elementos['P>|z|_ma.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.025_ma.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.975_ma.L%s'%(i+1)] = lista[index]; index +=1

    return elementos

def fit_arima(series, p, d, q):
    mod = ARIMA(series,
                order = (p, d, q))
    results = mod.fit()
    tables = results.summary()
    data_dict = individual_data(tables)

    
    return Markup(tables.as_html())
