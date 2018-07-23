import pandas as pd
import numpy as np
import os

def read_csv(fullpath, filename, separator= ',', header= True, date_column= None):

    if header == True:
        header = 0
    else:
        header = None

    df = pd.read_csv(fullpath, sep= separator, header= header)

    os_path = 'temp_files/'
    os.remove(os_path + filename)

    if date_column not in [None, 0]:
        dates = df.iloc[:,date_column-1]

        try:
            dates = pd.to_datetime(dates)
        except:
            size = len(dates)
            dates = np.array(range(1,size+1)).reshape(size,1)

        df.set_index(dates, inplace= True)
        df.drop(df.columns[date_column -1], axis=1, inplace= True)

    return df
