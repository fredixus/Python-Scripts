import pandas as pd
import pyodbc
import urllib
import os

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