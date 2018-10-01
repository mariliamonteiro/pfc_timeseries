import matplotlib
matplotlib.use('agg')
import pandas as pd
from matplotlib import pyplot as plt
import secrets
import os
import pandas as pd

UPLOAD_FOLDER = 'temp_files'

def ma_plot(series, window):
    ma = series.rolling(window).mean()
    plt.plot(series, color='#65acff', label='Dados Originais')
    plt.plot(ma, color='#e00a0a', label=u'Média Móvel')
    plt.legend()
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join('static','images', filename)
    plt.tight_layout()
    plt.savefig(figure_name)
    plt.close()
    return filename

def data_ma(series, window, rd):
    ma = series.rolling(window).mean()
    df_output = pd.DataFrame({'Tempo': rd,
                              'Media Movel': ma})
    # ma = list(pd.rolling_mean(series, window))
    return ma, df_output
