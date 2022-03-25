import os, logging
from azure.storage.blob import BlockBlobService
from azure.keyvault.secrets import SecretClient
from azure.identity import AzureCliCredential, DefaultAzureCredential, CredentialUnavailableError
import json

root = os.getcwd()
projectFolder = ""

class ConnectionObject:
    def __init__(self):
        STORAGEACCOUNTNAME = ""
        STORAGEACCOUNTKEY = ""

    def secretsFromJsonFile(self, filename="pass.json", STORAGEACCOUNTNAME="STORAGEACCOUNTNAME", STORAGEACCOUNTKEY="STORAGEACCOUNTKEY"):
        passFile = root + projectFolder + filename
        fileToOpen = open(passFile)
        secretsFile = json.load(fileToOpen)
        self.STORAGEACCOUNTNAME = secretsFile[STORAGEACCOUNTNAME]
        self.STORAGEACCOUNTKEY = secretsFile[STORAGEACCOUNTKEY]

    def secretsFromKeyVault(self, kv_url = "https://__________.vault.azure.net/", STORAGEACCOUNTNAME="STORAGEACCOUNTNAME", STORAGEACCOUNTKEY="STORAGEACCOUNTKEY"):
        credential = AzureCliCredential()
        client = SecretClient(vault_url=kv_url, credential=credential)
        self.STORAGEACCOUNTNAME = client.get_secret(STORAGEACCOUNTNAME).value 
        self.STORAGEACCOUNTKEY = client.get_secret(STORAGEACCOUNTKEY).value 

    def secretsFromLocal(self, STORAGEACCOUNTNAME="STORAGEACCOUNTNAME", STORAGEACCOUNTKEY="STORAGEACCOUNTKEY"):
        self.STORAGEACCOUNTNAME = os.getenv[STORAGEACCOUNTNAME]
        self.STORAGEACCOUNTKEY = os.getenv[STORAGEACCOUNTKEY] 

    def getSecrets(self):
        return self.STORAGEACCOUNTNAME, self.STORAGEACCOUNTKEY

    def getStorageName(self):
        return self.STORAGEACCOUNTNAME

    def getStorageKey(self):
        return self.STORAGEACCOUNTKEY

class BlobObject(ConnectionObject):
    def __init__(self, container) -> None:
        self.connection = ConnectionObject()
        self.container = container
        self.service = None
        self.notify = False
        self.storageUrl = "https://__________.vault.azure.net/"

    def checkContainerName(self):
        return True if self.container == self.connection.getStorageName() else False
    
    def toggleNotify(self):
        if (self.notify==True):
            self.notify=False 
        else:
            self.notify=True
    
    def turnOnNotify(self):
        self.notify=True

    def setStorageUrl(self, storageUrl):
        self.storageUrl = storageUrl

    def connectToBlobService(self):
        try: 
            self.connection.secretsFromJsonFile()
        except FileNotFoundError:
            self.connection.secretsFromKeyVault(self.storageUrl)
        except CredentialUnavailableError:
            self.connection.secretsFromLocal()
        finally:
            self.service = BlockBlobService(account_name = self.connection.getStorageName(), account_key = self.connection.getStorageKey())
            if(self.notify):
                logging.info("Created new BlockBlobService")
    
    def listBlobsInContainer(self):
        return [x.name for x in self.service.list_blobs(self.container)]

    def printBlobsInContainer(self):
        for blob in self.listBlobsInContainer():
            print("+\t" + blob)

    def getTheBlobAsFile(self, blobName, filePath):
        return self.service.get_blob_to_path(self.container, blobName, filePath)

    def getTheBlobAsText(self, blobName):
        return self.service.get_blob_to_text(self.container, blobName)

    def putDataFrameToBlob(self, df, blob_file_name, **kwargs) -> None:
        #**kwargs can be everything to Pandas.DataFrame.to_csv() f.ex.: {index=False, sep=','}
        self.service.create_blob_from_text(self.container, blob_file_name, df.to_csv(**kwargs))
        if(self.notify):
            logging.info("Saved {} {}/{}".format(str(df.shape), self.container, blob_file_name))