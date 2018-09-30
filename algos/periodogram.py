import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot
from statsmodels.tsa.stattools import periodogram
import secrets
import os
import pandas as pd
import numpy as np
from scipy import interpolate

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

    tickers = np.linspace(min(periodo[1:]),max(periodo[1:]),10*len(periodo[1:]))
    Spline = interpolate.splrep(np.flip(periodo[1:],0), np.flip(pgram[1:],0))
    y_alt = interpolate.splev(tickers, Spline)

    fig = pyplot.figure()
    fig.tight_layout()

    freq2 = fig.add_subplot(211)
    freq2.plot(freq, pgram)
    pyplot.ylabel('P')
    pyplot.xlabel('Frequência')
    pyplot.grid(True)
    pyplot.tight_layout()

    periodo2 = fig.add_subplot(212)
    periodo2.plot(np.flip(periodo,0), np.flip(pgram,0), '-o')
    pyplot.ylabel('P')
    pyplot.xlabel('Período')
    pyplot.grid(True)
    pyplot.tight_layout()

    fig.savefig(figure_name)
    pyplot.close()
    return filename
