import pandas as pd
import pyodbc
import urllib
import os
from sqlalchemy import create_engine

from azure.keyvault.secrets import SecretClient
from azure.identity import AzureCliCredential

def getLocalEnviromentSqlServer():
    """
    Gets the parameters, from local machine to connect to Database engine.

    :param server: {str} :: Server name with SQL:
    :param dbname: {str} :: Database name in {server},
    :param userID: {str} :: User name in {server} with access to {dbname},
    :param passID: {str} :: Password for {User} in {server} with access to {dbname}

    :return:
        set of strings (server, dbname, userID, passID)
    """
    server = os.environ["SERVER"]
    dbname = os.environ["DBNAME"]
    userID = os.environ["USERID"]
    passID = os.environ["PASSID"]

    return server, dbname, userID, passID

def getKeyValutEnviromentSqlServer(database = 'DataBase Name'):
    """
    Gets the parameters, from local machine to connect to Database engine.

    :param server: {str} :: Server name with SQL:
    :param dbname: {str} :: Database name in {server},
    :param userID: {str} :: User name in {server} with access to {dbname},
    :param passID: {str} :: Password for {User} in {server} with access to {dbname}

    :return:
        set of strings (server, dbname, userID, passID)
    """

    #Names of secrets
    server = 'dbserver'
    username = 'dbuser'
    passwd = "dbpass"

    #Azure Key Vault adress
    kv_url = "https://__________.vault.azure.net/"
    
    #Login
    credential = AzureCliCredential()

    #Create client
    client = SecretClient(vault_url=kv_url, credential=credential)

    #Get secrets
    password = client.get_secret(passwd).value
    username = client.get_secret(username).value
    server = client.get_secret(server).value
    
    return server, database, username, password

def getKeyValutSecret(secret = 'secretName'):
    """
    Gets the secret, from KeyValut.
    :param secret: {str} :: Secret name.
    :return:
        str secret
    """

    #Azure Key Vault adress
    kv_url = "https://__________.vault.azure.net/"
    
    #Login
    credential = AzureCliCredential()

    #Create client
    client = SecretClient(vault_url=kv_url, credential=credential)

    #Get secrets
    secret = client.get_secret(secret).value
    
    return secret

def connectSql(driver, server, dbname, userID, passID):
    """
    Connect to Database engine.

    :param driver: SQL Driver f.ex.: SQL Server Native Client 11.0
    :param server: SQL Server name
    :param dbname: Database name in {server}
    :param userID: User name in {server} with access to {dbname}
    :param passID: Password for {User} in {server} with access to {dbname}

    :return:
    conection :: {pyodbc.connect} :: Connection object
    """
    conection = pyodbc.connect(
        "Driver={"  + driver +"};"
        "Server="   + server +";"
        "Database=" + dbname +";"
        "uid="      + userID +";"
        "pwd="      + passID +";"
    )
    return conection

def getSqlAsDf(sql, driver = "SQL Server Native Client 11.0"):
    """
    Connect to Database engine, and execute SQL command.

    :param sql: SQL formula to execute on Database f.ex. 'Select * From TableName'
    :param driver: SQL Driver f.ex.: SQL Server Native Client 11.0

    :return:
    df :: {pandas.DataFrame} :: Object with SQL data
    """
    server, dbname, userID, passID = getLocalEnviromentSqlServer()
    conection = pyodbc.connect(
        "Driver={"  + driver + "};"
        "Server="   + server + ";"
        "Database=" + dbname + ";"
        "uid="      + userID + ";"
        "pwd="      + passID + ";"
    )
    df = pd.read_sql(sql, conection)
    conection.close()
    return df

def putData(df, database = 'DataBase Name', tableName=""):
    """Save data into Database"""
    server, dbname, uid, pwd = getKeyValutEnviromentSqlServer(database)
    driver = "ODBC Driver 17 for SQL Server"
    connectionstring = 'mssql+pyodbc://{uid}:{password}@{server}:1433/{database}?driver={driver}'.format(
        uid=uid,
        password=pwd,
        server=server,
        database=dbname,
        driver=driver.replace(' ', '+'))

    engn = create_engine(connectionstring)
    df.to_sql(tableName, engn, if_exists='append', index=False) 