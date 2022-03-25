import openpyxl as oxls
from itertools import islice
import pandas as pd

def toDataFrame(sheetName):
    data = sheetName.values
    cols = next(data)[1:]
    data = list(data)

    data = (islice(r, 1, None) for r in data)
    df = pd.DataFrame(data, columns=cols)
    return df