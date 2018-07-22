import pandas as pd
import os

def read_csv(filename, separator= ',', header= True, date_column= None):

    fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if header == True:
        header = 0
    else:
        header = None

    df = pd.read_csv(fullpath, sep= separator, header= header)

    if date_column not in [None, 0]:
        dates = df.iloc[:,date_column-1]
        dates = pd.to_datetime(dates)

        df.set_index(dates, inplace= True)
        df.drop(df.columns[date_column -1], axis=1, inplace= True)

    return df
