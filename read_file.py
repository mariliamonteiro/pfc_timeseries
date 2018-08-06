import pandas as pd
from datetime import datetime, timedelta
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

        if (dates.dtype == np.int64):
            try:
                dates = pd.DatetimeIndex([str(x) for x in dates])
            except:
                size = len(dates)
                dates = pd.date_range('1900/01/01', periods=size, freq='D')

        elif (dates.dtype == np.float64):
            try:
                d_aux = [datetime(int(d), 1, 1) + timedelta(days= int((d-int(d))*365.2475)) for d in raw_dates]
                dates = pd.to_datetime(d_aux)
            except:
                size = len(dates)
                dates = pd.date_range('1900/01/01', periods=size, freq='D')

        else:
            val=0
            for fmt in supported_formats:
                try:
                    dates = pd.to_datetime(dates, format= fmt)
                    val = val +1
                    if val >0:
                        break
                except:
                    pass

            if val == 0:
                size = len(dates)
                dates = pd.date_range('1900/01/01', periods=size, freq='D')

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
