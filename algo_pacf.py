from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.stattools import pacf
import secrets
import os

UPLOAD_FOLDER = 'temp_files'

def pacf_plot(series, lags):
    plot_pacf(series, lags=lags)
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join('static','images', filename)
    pyplot.savefig(figure_name)
    pyplot.close()
    return filename

def data_pacf(series, lags):
    autocorr = list(pacf(series, nlags = lags))
    return autocorr
