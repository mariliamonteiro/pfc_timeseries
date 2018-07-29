from matplotlib import pyplot
from statsmodels.tsa.seasonal import seasonal_decompose
import secrets
import os

UPLOAD_FOLDER = 'temp_files'

def decomposition_plot(series, model, freq, reference):
    result = seasonal_decompose(series, model=model, two_sided=reference)
    result.plot()
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join('static','images', filename)
    pyplot.savefig(figure_name)
    pyplot.close()
    return filename

# def data_acf(series, lags):
#     autocorr = list(acf(series, nlags = lags))
#     return autocorr
