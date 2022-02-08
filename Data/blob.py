import os, logging
import pandas as pd
from azure.storage.blob import BlockBlobService

### All code base on code available: https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python-legacy

def _createBlockBlobService():
    STORAGEACCOUNTNAME = os.environ["STORAGEACCOUNTNAME"]
    STORAGEACCOUNTKEY = os.environ["STORAGEACCOUNTKEY"]

    return BlockBlobService(account_name = STORAGEACCOUNTNAME, account_key = STORAGEACCOUNTKEY)

def saveDataFrameAsCsv(blob_file_name, conteiner, df):

    blob_service = _createBlockBlobService()
    blob_service.create_blob_from_text(conteiner, blob_file_name, df.to_csv(index=False, sep=';'))

    logging.info("Saved {} {}/{}".format(str(df.shape), conteiner, blob_file_name))

def listBlobsInContainer(conteiner):
    
    blob_service = _createBlockBlobService()

    # List the blobs in the container
    blob_list = blob_service.list_blobs(conteiner)
    for blob in blob_list:
        print("\t" + blob.name)