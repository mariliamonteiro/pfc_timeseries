import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot
from statsmodels.tsa.seasonal import seasonal_decompose
import secrets
import os
import pandas as pd

UPLOAD_FOLDER = 'temp_files'

def decomposition_plot(series, model, freq, two_sided):
    result = seasonal_decompose(series, model=model, freq=freq, two_sided=two_sided)
    result.plot()
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join('static','images', filename)
    pyplot.tight_layout()
    pyplot.savefig(figure_name)
    pyplot.close()
    return filename

def data_decomposition(series, model, freq, two_sided, rd):
    result = seasonal_decompose(series, model=model, freq=freq, two_sided=two_sided)
    trend = list(result.trend.values)
    seasonal = list(result.seasonal.values)
    residual = list(result.resid.values)
    df_output = pd.DataFrame({'Tempo': rd,
                              'Tendência': trend,
                              'Sazonalidade': seasonal,
                              'Resíduo': residual})
    return trend, seasonal, residual, df_output
