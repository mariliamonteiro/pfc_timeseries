import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import scipy.stats as stats
import os

dir = os.path.dirname(__file__)
mypath = os.path.join(dir, 'temp_files')

# Construir DatetimeIndex a partir da frequência passada e dos dados originais
def infer_dates(dates, freq='D'):
    qty = len(dates)

    if (dates.dtype == np.int64):
        try:
            final_dates = pd.DatetimeIndex([str(x) for x in dates])
        except:
            final_dates = pd.date_range('1900-01-01', periods= qty, freq= freq)

    elif (dates.dtype == np.float64):
        try:
            beg = dates[0]
            start_date = datetime(int(beg),1,1) + timedelta(days= int((beg-int(beg))*365))

            final_dates = pd.date_range(start_date, periods= qty, freq= freq)

        except:
            final_dates = pd.date_range('1900-01-01', periods= qty, freq= freq)

    else:
        try:
            final_dates = pd.to_datetime(dates)
            final_dates.freq = pd.tseries.frequencies.to_offset(freq)

            if final_dates.freq == None:
                start_date = final_dates[0]
                final_dates = pd.date_range(start_date, periods= qty, freq= freq)

        except:
            final_dates = pd.date_range('1900-01-01', periods= qty, freq= freq)

    return final_dates

# Leitura do arquivo, considerando as opções na plataforma
def read_csv(fullpath, filename, separator= ',', header= True, date_column= 0, main_column= 1, freq= 'D', missing= 'drop', isseries= True):

    if header == True:
        header = 0
    else:
        header = None

    df = pd.read_csv(fullpath, sep= separator, header= header)
    os.remove(os.path.join(mypath, filename))

    col = list(df.columns.values)
    title = col[main_column -1]

    # Tratamento de dados faltantes na coluna principal
    if missing == 'ffill':
        df[title] = df[title].ffill()
    elif missing == 'linear':
        df[title] = df[title].interpolate(method= 'linear')
    elif missing == 'cubic':
        df[title] = df[title].interpolate(method= 'cubic')

    logical = pd.notnull(df[title])
    df = df[logical]

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

        dates = infer_dates(dates, freq)

    else:
        qty = sizedf[0]
        dates = pd.date_range('1900-01-01', periods= qty, freq= freq)
        raw_dates = list(range(1,qty+1))

    # Problema univariado ou multivariado
    if isseries == True:
        df.set_index(dates, inplace= True)

        df.drop(df.columns[:], axis=1, inplace= True)
        df[title] = mainc

    else:
        df.set_index(dates, inplace= True)

        date_title = col[date_column -1]
        rest_title = col.remove(title); rest_title = rest_title.remove(date_title)

        df = df[[title]+rest_title]

    # Converter para série (step final)
    if isseries == True:
        df = df.iloc[:,0]

    return df, raw_dates, df_summary

# Função para reduzir número de linhas no app (limpeza)
def deal_inputs(filepath, filename, form, isseries= True):

    separator = form.sep.data
    header = form.header.data
    date_column = form.datec.data
    main_column = form.datac.data
    missing = form.missing.data
    freq = form.freq.data

    serie, rd, quality_param = read_csv(filepath, filename, separator, header, date_column, main_column, freq, missing, isseries)

    return serie, rd, quality_param

# Geração de tabela para inclusão no relatório
def readdata_table(form):

    separator = form.sep.data
    header = form.header.data
    date_column = form.datec.data
    main_column = form.datac.data
    missing = form.missing.data
    freq = form.freq.data

    readdata_param = [['Separador', str(separator)],
                      ['Cabeçalho', str(header)],
                      ['Coluna de Datas', str(date_column)],
                      ['Coluna Principal', str(main_column)],
                      ['Frequência dos Dados', str(freq)],
                      ['Tratamento de Dados Faltantes', str(missing)]]

    return readdata_param

# Sumarização dos dados iniciais para inclusão no relatório
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
