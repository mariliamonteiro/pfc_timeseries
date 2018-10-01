import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from statsmodels.tsa.statespace.sarimax import SARIMAX
import secrets
import os
import pandas as pd
import re
import statsmodels.api as sm

UPLOAD_FOLDER = 'temp_files'

def get_data(tables):
    string = tables.as_html()
    begin = [m.start() for m in re.finditer('<td>', string)]
    end = [m.start() for m in re.finditer('</td', string)]
    lista = []
    for i in range(len(begin)):
        info = string[begin[i] + 4: end[i]]
        lista.append(info)
    return lista

def individual_data_sarima(lista, p, q, P, Q):

    for i in range(len(lista)):
        lista[i] = lista[i].replace(' ', '')

    elementos = {'titulo': lista[0],
                 'n_obs': lista[1],
                 'modelo': lista[2],
                 'LogLikelihood': lista[3],
                 'data': lista[4],
                 'AIC': lista[5],
                 'BIC': lista[7],
                 'HQIC': lista[9],
                 }

    index = 14
    for i in range(p):
        index +=1
        elementos['coef_ar.L%s'%(i+1)] = lista[index]; index +=1
        elementos['std_err_ar.L%s'%(i+1)] =  lista[index]; index +=1
        elementos['z_ar.L%s'%(i+1)] = lista[index]; index +=1
        elementos['P>|z|_ar.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.025_ar.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.975_ar.L%s'%(i+1)] = lista[index]; index +=1

    for i in range(q):
        elementos['coef_ma.L%s'%(i+1)] = lista[index]; index +=1
        elementos['std_err_ma.L%s'%(i+1)] =  lista[index]; index +=1
        elementos['z_ma.L%s'%(i+1)] = lista[index]; index +=1
        elementos['P>|z|_ma.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.025_ma.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.975_ma.L%s'%(i+1)] = lista[index]; index +=1

    for i in range(P):
        index +=1
        elementos['coef_ar.S.L%s'%(i+1)] = lista[index]; index +=1
        elementos['std_err_ar.S.L%s'%(i+1)] =  lista[index]; index +=1
        elementos['z_ar.S.L%s'%(i+1)] = lista[index]; index +=1
        elementos['P>|z|_ar.S.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.025_ar.S.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.975_ar.S.L%s'%(i+1)] = lista[index]; index +=1

    for i in range(Q):
        elementos['coef_ma.S.L%s'%(i+1)] = lista[index]; index +=1
        elementos['std_err_ma.S.L%s'%(i+1)] =  lista[index]; index +=1
        elementos['z_ma.S.L%s'%(i+1)] = lista[index]; index +=1
        elementos['P>|z|_ma.S.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.025_ma.S.L%s'%(i+1)] = lista[index]; index +=1
        elementos['0.975_ma.S.L%s'%(i+1)] = lista[index]; index +=1

    return elementos

def fit_sarima(series, p, d, q, P, D, Q, s, ptest, predict_range):
    test=ptest
    # Reduzir a série retirando dados de teste
    series_clipped = series[0:int((1-test/100)*len(series))]

    # Rodar SARIMA com parâmetros dados
    if P == 0 and Q==0 and D==0:
        mod = SARIMAX(series_clipped,
                      order = (p,d,q),
                      enforce_stationarity = False,
                      enforce_invertibility = False,
                      )
    else:
        mod = SARIMAX(series_clipped,
                      order = (p,d,q),
                      seasonal_order = (P,D,Q,s),
                      enforce_stationarity = False,
                      enforce_invertibility = False,
                      )

    # Fit do SARIMA
    results = mod.fit()

    # Tabelas com parâmetros dos resultados gerados
    # Os parâmentros são salvos individualmente no dict "elementos"
    tables = results.summary()

    lista = get_data(tables)
    elementos = individual_data_sarima(lista, p, q, P, Q)
    elementos['n_obs_orig'] = len(series)
    # Gráficos com análises do Fit
    results.plot_diagnostics(figsize=(15,12))

    filename_diag = secrets.token_hex(8)+'.png'
    figure_name_diag = os.path.join('static','images', filename_diag)
    plt.tight_layout()
    plt.savefig(figure_name_diag)
    plt.close()

    # Forecast dentro da própria série para exibição
    mod_comp = sm.tsa.statespace.SARIMAX(series,
                                         order=(p, d, q),
                                         seasonal_order = (P,D,Q,s),
                                         enforce_stationarity = False,
                                         enforce_invertibility = False)
    res = mod_comp.filter(results.params)

    pred = res.get_prediction()
    pred_ci = pred.conf_int()

    ax = series[int((1-test/100)*len(series)):].plot(label='Observado')
    pred.predicted_mean[int((1-test/100)*len(series)):].plot(ax=ax, label='Predição um passo a frente', alpha=.7)

    ax.fill_between(pred_ci[int((1-test/100)*len(series)):].index,
                    pred_ci[int((1-test/100)*len(series)):].iloc[:, 0],
                    pred_ci[int((1-test/100)*len(series)):].iloc[:, 1], color='k', alpha=.2)

    ax.set_xlabel('Data')
    plt.legend()

    filename_mse = secrets.token_hex(8)+'.png'
    figure_name_mse = os.path.join('static','images', filename_mse)
    plt.tight_layout()
    plt.savefig(figure_name_mse)
    plt.close()

    # Cálculo do erro médio quadrático
    y_forecasted = pred.predicted_mean
    y_real = series[int((1-test/100)*len(series)):]
    mse = ((y_forecasted - y_real) ** 2).mean()
    mape = ((abs((y_forecasted - y_real)/y_real))).mean()

    elementos['mse'] = mse
    elementos['mape'] = mape

    # Forecast completo considerando modelo calculado sobre toda a série
    result_comp = mod_comp.fit()
    pred_comp = result_comp.get_forecast(steps = predict_range)
    pred_comp_ci = pred_comp.conf_int()

    ax = series.plot(label='Observado', figsize=(20, 15))
    pred_comp.predicted_mean.plot(ax=ax, label='Predição')
    ax.fill_between(pred_comp_ci.index,
                    pred_comp_ci.iloc[:, 0],
                    pred_comp_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Tempo')
    plt.legend()

    filename_forecast = secrets.token_hex(8)+'.png'
    figure_name_forecast = os.path.join('static','images', filename_forecast)
    plt.tight_layout()
    plt.savefig(figure_name_forecast)
    plt.close()

    df_output = pred_comp.predicted_mean
    return elementos, filename_diag, filename_mse, filename_forecast, df_output
