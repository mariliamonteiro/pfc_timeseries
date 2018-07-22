from pandas import Series

def extractSerie(path):
    series = Series.from_csv(path, header=0)
    return series
