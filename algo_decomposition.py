from matplotlib import pyplot
from statsmodels.tsa.seasonal import seasonal_decompose
import secrets
import os

UPLOAD_FOLDER = 'temp_files'

def decomposition_plot(series, model, freq, two_sided):
    result = seasonal_decompose(series, model=model, freq=freq, two_sided=two_sided)
    result.plot()
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join('static','images', filename)
    pyplot.savefig(figure_name)
    pyplot.close()
    return filename

def data_decomposition(series, model, freq, two_sided):
    result = seasonal_decompose(series, model=model)
    trend = list(result.trend.values)
    seasonal = list(result.seasonal.values)
    residual = list(result.resid.values)
    return trend, seasonal, residual
