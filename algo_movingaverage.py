import pandas as pd
from matplotlib import pyplot as plt
import secrets
import os

UPLOAD_FOLDER = 'temp_files'

def ma_plot(series, window):
    ma = series.rolling(window).mean()
    plt.plot(ma)
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join('static','images', filename)
    plt.savefig(figure_name)
    plt.close()
    return filename

def data_ma(series, window):
    ma = list(series.rolling(window).mean().values)
    print (ma)
    # ma = list(pd.rolling_mean(series, window))
    return ma
