import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
import secrets
import os
import pandas as pd

UPLOAD_FOLDER = 'temp_files'

def acf_plot(series, lags):
    plot_acf(series, lags=lags)

    uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
    root = uppath(__file__, 2)

    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join(root, 'static','images', filename)

    pyplot.tight_layout()
    pyplot.savefig(figure_name)
    pyplot.close()
    return filename

def data_acf(series, lags):
    autocorr = list(acf(series, nlags = lags))
    df_output = pd.DataFrame({'Lag': range(lags + 1),
                              'Autocorrelacao': autocorr})
    return autocorr, df_output
