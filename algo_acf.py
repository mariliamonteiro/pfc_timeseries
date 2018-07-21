from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
import secrets
import os

UPLOAD_FOLDER = 'temp_files'

def acf_plot(series, lags):
    plot_acf(series, lags=lags)
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join('temp_files', filename)
    pyplot.savefig(figure_name)
    return figure_name

def data_acf(series, lags):
    autocorr = acf(series, nlags = lags)
    return autocorr
