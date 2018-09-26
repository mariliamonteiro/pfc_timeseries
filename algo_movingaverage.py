import pandas as pd
from matplotlib import pyplot as plt
import secrets
import os
import pandas as pd

UPLOAD_FOLDER = 'temp_files'

def ma_plot(series, window):
    ma = series.rolling(window).mean()
    plt.plot(series, linewidth=0.5, color='#65acff', label='Dados Originais')
    plt.plot(ma, linewidth=0.7, color='#e00a0a', label=u'Média Móvel')
    plt.legend()
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join('static','images', filename)
    plt.savefig(figure_name)
    plt.close()
    return filename

def data_ma(series, window, rd):
    ma = series.rolling(window).mean()
    df_output = pd.DataFrame({'Tempo': rd,
                              'Media Movel': ma})
    # ma = list(pd.rolling_mean(series, window))
    return ma, df_output
