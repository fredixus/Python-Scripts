#%% Imports
import pandas as pd
import dataimport as di

#%% BODY
if __name__ == '__main__':
    sql = "SELECT * FROM Costumers"
    df = di.getSqlAsDf(sql)
    print(df)
