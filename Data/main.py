#%% Imports
import pandas as pd
import dataimport as di
import blob as blob

#%% BODY
if __name__ == '__main__':
    sql = "SELECT * FROM Costumers"
    df = di.getSqlAsDf(sql)
    print(df)

    df = pd.DataFrame({'grades': [0,1,10,12,100,120,200,250]})
    blob.saveDataFrameAsCsv("test.csv", 'test', df)

    blob.listBlobsInContainer('test')


