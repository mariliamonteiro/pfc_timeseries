import pandas as pd
import numpy as np
import os

def read_csv(fullpath, filename, separator= ',', header= True, date_column= 0, main_column= 1, isseries= False):

    if header == True:
        header = 0
    else:
        header = None

    df = pd.read_csv(fullpath, sep= separator, header= header)

    os_path = 'temp_files/'
    os.remove(os_path + filename)

    supported_formats = ['%d-%m-%Y', '%d-%m-%y', '%d/%m/%Y', '%d/%m/%y',
                         '%Y-%m-%d', '%y-%m-%d', '%Y/%m/%d', '%y/%m/%d']

    mainc = list(df.iloc[:,main_column-1])

    if date_column > 0:
        dates = df.iloc[:,date_column-1]
        raw_dates = list(dates)

        if (dates.dtype == np.int64) or (dates.dtype == np.float64):
            pass

        else:
            val=0
            for fmt in supported_formats:
                try:
                    dates = pd.to_datetime(dates, format= fmt)
                    val= val +1
                except:
                    pass

            if val == 0:
                size = len(dates)
                dates = np.arange(1,size+1)

    if isseries == True:
        df.set_index(dates, inplace= True)

        col = list(df.columns.values); title = col[main_column -1]

        df.drop(df.columns[:], axis=1, inplace= True)
        df[title] = mainc

        df = df.iloc[:,0]

    else:
        df.set_index(dates, inplace= True)
        df.drop(df.columns[date_column -1], axis=1, inplace= True)


    return df, raw_dates
