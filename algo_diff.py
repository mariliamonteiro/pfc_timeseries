import matplotlib
matplotlib.use('agg')
import pandas as pd
from matplotlib import pyplot
import secrets
import os
import pandas as pd

UPLOAD_FOLDER = 'temp_files'

def diff(series, order, rd):
    diff = series
    for i in range(order):
        diff = diff - diff.shift()

    pyplot.plot(diff)
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join('static','images', filename)
    pyplot.savefig(figure_name)
    pyplot.close()

    df_output = pd.DataFrame({'Tempo': rd,
                              'Valor Diferenciado': diff})

    return filename, diff, df_output
