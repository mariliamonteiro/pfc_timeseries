import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot
from statsmodels.tsa.stattools import periodogram
import secrets
import os
import pandas as pd
import numpy as np

UPLOAD_FOLDER = 'temp_files'

def data_periodogram(dados):
    freq = np.arange(0, 0.5, 1/len(dados))
    periodo = 1/freq

    pyplot.plot(dados)
    pyplot.show()

    pgram = periodogram(dados)
    if len(pgram) % 2 == 0:
        pgram = pgram[0:int(len(dados)/2)]
        index = np.argmax(pgram)
    else:
        pgram = pgram[0:int((len(dados))/2)+1]
        index = np.argmax(pgram)

    freq_max = freq[index]
    T = len(dados)/index

    df_output = pd.DataFrame({'Frequencia': freq,
                              'Periodograma': pgram})
    return pgram, freq, df_output, index, freq_max

def periodogram_plot(series):
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join('static','images', filename)

    pgram, freq, df, index, freq_max = data_periodogram(series)

    with np.errstate(divide='ignore'):
        periodo = 1/freq

    fig = pyplot.figure()
    freq2 = fig.add_subplot(211)
    periodo2 = fig.add_subplot(212)
    freq2.plot(np.flip(periodo,0), np.flip(pgram,0), 'o')
    pyplot.ylabel('P')
    pyplot.xlabel('Periodo')

    periodo2.plot(freq, pgram)
    pyplot.ylabel('P')
    pyplot.xlabel('Frequência')
    fig.savefig(figure_name)
    pyplot.close()
    return filename
