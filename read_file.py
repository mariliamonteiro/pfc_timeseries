import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy import stats
import os

def read_csv(fullpath, filename, separator= ',', header= True, date_column= 0, main_column= 1, isseries= False, missing= 'drop'):

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

    # Estatísticas dos dado bruto de entrada
    sizedf = df.shape
    total_nan = sum(pd.isnull(mainc))

    df_summary = [['Número de registros', str(sizedf[0])],
                  ['Número de colunas', str(sizedf[1])],
                  ['Quantidade de dados faltantes', str(total_nan)],
                  ['Percentual de dados faltantes', str(round(100*total_nan/sizedf[0],2))+'%'],
                  ['Método de tratamento de dados faltantes', str(missing)]]

    # Tentar interpretar coluna de datas
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

    # Problema univariado ou multivariado
    col = list(df.columns.values)
    title = col[main_column -1]

    if isseries == True:
        df.set_index(dates, inplace= True)

        df.drop(df.columns[:], axis=1, inplace= True)
        df[title] = mainc

    else:
        df.set_index(dates, inplace= True)

        date_title = col[date_column -1]
        rest_title = col.remove(title); rest_title = rest_title.remove(date_title)

        df = df[[title]+rest_title]

    # Tratamento de dados faltantes na coluna principal
    if missing == 'ffill':
        df[title] = df[title].ffill()
    elif missing == 'linear':
        df[title] = df[title].interpolate(method= 'linear')
    elif missing == 'cubic':
        df[title] = df[title].interpolate(method= 'cubic')

    logical = pd.notnull(df[title])
    df = df[logical]
    raw_dates = list(np.array(raw_dates)[logical])

    # Converter para série (step final)
    if isseries == True:
        df = df.iloc[:,0]

    return df, raw_dates, df_summary

def summary_maincol(df):

    if isinstance(df, pd.Series):
        mainc = np.array(df)
    else:
        mainc = np.array(df.iloc[:,0])

    avg = np.mean(mainc); std = np.std(mainc)
    skew = stats.skew(mainc); kurt = stats.kurtosis(mainc)
    min = np.min(mainc); max = np.max(mainc)

    q25 = np.percentile(mainc, 25); med = np.median(mainc)
    q75 = np.percentile(mainc, 75); iqr = 1.5*(q75 - q25)
    lbo = sum(mainc < (q25 - iqr)); ubo = sum(mainc > (q75 + iqr))

    summ_table = [['Média', 'Desvio Padrão', 'Assimetria', 'Curtose', 'Min', 'Max'],
                  [str(round(avg,5)), str(round(std,5)), str(round(skew,5)), str(round(kurt,5)), str(round(min,5)), str(round(max,5))],
                  ['Q25', 'Mediana', 'Q75', 'IQR', 'LBO', 'UBO'],
                  [str(round(q25,5)), str(round(med,5)), str(round(q75,5)), str(round(iqr,5)), str(lbo), str(ubo)]]

    return summ_table
