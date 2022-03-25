#%% Imports
import pandas as pd
import dataimport as di
from blob import BlobObject

#%% BODY
if __name__ == '__main__':
    sql = "SELECT * FROM Costumers"
    df = di.getSqlAsDf(sql)
    print(df)

    df = pd.DataFrame({'grades': [0,1,10,12,100,120,200,250]})

    blob = BlobObject("blobContainerName")
    blob.turnOnNotify()
    blob.connectToBlobService()

    print(blob.listBlobsInContainer())

    blob.putDataFrameToBlob(df, blob_file_name="test.csv", index=False, sep=",")



