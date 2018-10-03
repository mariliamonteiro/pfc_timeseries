import matplotlib
matplotlib.use('agg')
import pandas as pd
from matplotlib import pyplot
import secrets
import os
import pandas as pd

UPLOAD_FOLDER = 'temp_files'

def diff(series, order, rd):
    uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
    root = uppath(__file__, 2)
    
    diff = series
    for i in range(order):
        diff = diff - diff.shift()

    pyplot.plot(diff)
    filename = secrets.token_hex(8)+'.png'
    figure_name = os.path.join(root, 'static','images', filename)
    pyplot.tight_layout()
    pyplot.savefig(figure_name)
    pyplot.close()

    df_output = pd.DataFrame({'Tempo': rd,
                              'Valor Diferenciado': diff})

    return filename, diff, df_output
