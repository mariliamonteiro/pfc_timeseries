import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
import secrets
import os
import pandas as pd
from flask import Markup

UPLOAD_FOLDER = 'temp_files'

def individual_data(tables, p, d, q):
    csv = tables.as_csv()
    lista = csv.replace('\n',',').replace(' ','').split(',')

    if d == 0:
        x = 1
    else:
        x = 0

    elementos = {'titulo': lista[2],
                 'n_obs': lista[4],
                 'LogLikelihood': lista[10-x],
                 'metodo': lista[12-x],
                 'data': lista[17-x],
                 'AIC': lista[19-x],
                 'BIC': lista[23-x],
                 'HQIC': lista[27-x],

                 'coef_const': lista[40-x],
                 'std_err_const': lista[41-x],
                 'z_const': lista[42-x],
                 'P>|z|_const': lista[43-x],
                 '0.025_const': lista[44-x],
                 '0.975_const': lista[45-x]
                 }

    if d == 0:
        elementos['modelo'] = lista[6]+','+lista[7]
    else:
        elementos['modelo'] = lista[6]+','+lista[7]+','+lista[8]

    index = 46 - x
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

def fit_arima(series, p, d, q, test):

    # Reduzir a série retirando dados de teste
    series_clipped = series[0:int((1-test/100)*len(series))]

    # Rodar ARIMA com parâmetros dados
    mod = ARIMA(series_clipped,
                order = (p, d, q))


    # Realizar fit do ARIMA
    results = mod.fit(start_ar_lags = p + 1)

    # Tabelas com parâmetros dos resultados gerados
    # Os parâmentros são salvos individualmente no dict "elementos"
    tables = results.summary()
    elementos = individual_data(tables, p, d, q)
    elementos['n_obs_orig'] = len(series)
    print(tables)
    # Análise de erros do fit

    # Gráfico dos resíduos
    residuals = pd.DataFrame(results.resid)
    std = residuals.plot(title='Erro', legend=False)
    std.set_xlabel('Tempo')
    std.set_ylabel('Resíduo')

    filename_residuo = secrets.token_hex(8)+'.png'
    figure_name_residuo = os.path.join('static','images', filename_residuo)
    pyplot.savefig(figure_name_residuo)
    pyplot.close()

    # Histograma de erros e densidade de kernel
    ax = residuals.plot(kind='hist', density=True, label='Histograma')
    hist = residuals.plot(kind='kde',
                          ax=ax,
                          title = 'Histograma e Estimador de Densidade dos Erros',
                          label ='KDE')
    hist.legend(['KDE', 'Histograma'])

    filename_hist = secrets.token_hex(8)+'.png'
    figure_name_hist = os.path.join('static','images', filename_hist)
    pyplot.savefig(figure_name_hist)
    pyplot.close()

    # Forecast dentro da série para exibição
    forecast, stderr, conf_int = results.forecast(len(series)-len(series_clipped))

    real = series[int((1-test/100)*len(series)):]

    df = pd.DataFrame(real)
    df['predict'] = forecast

    pyplot.plot(df)

    filename_forecast = secrets.token_hex(8)+'.png'
    figure_name_forecast = os.path.join('static','images', filename_forecast)
    pyplot.savefig(figure_name_forecast)
    pyplot.close()


    return elementos, filename_residuo, filename_hist, filename_forecast

def predict_arima(series, p, d, q, predict_range):
    # Rodar ARIMA com parâmetros dados
    mod = ARIMA(series,
                order = (p, d, q))
    results = mod.fit(start_ar_lags = p + 1)

    results.plot_predict(start = int(0.9*len(series)),
                         end = len(series) + predict_range,
                         dynamic = False,
                         plot_insample = True)

    filename_predict = secrets.token_hex(8)+'.png'
    figure_name_predict = os.path.join('static','images', filename_predict)
    pyplot.savefig(figure_name_predict)
    pyplot.close()

    return filename_predict
