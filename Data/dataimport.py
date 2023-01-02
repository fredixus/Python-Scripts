import pandas as pd
import pyodbc
import urllib
import os
from sqlalchemy import create_engine
import json

class database:

    def __init__(self, driver = "ODBC Driver 17 for SQL Server"):
        server = None
        name = None
        user = None
        password = None
        self.driver = driver
        connection = None

    def set_variables_local_enviroment(self):
        """
        Sets the parameters, from local machine to connect to Database engine.

        :param server: {str} :: Server name with SQL:
        :param dbname: {str} :: Database name in {server},
        :param userID: {str} :: User name in {server} with access to {dbname},
        :param passID: {str} :: Password for {User} in {server} with access to {dbname}

        :return:
            set of strings (server, dbname, userID, passID)
        """
        self.server = os.environ["SERVER"]
        self.name = os.environ["DBNAME"]
        self.user = os.environ["USERID"]
        self.password = os.environ["PASSID"]

    def set_variables_key_vault(self, kv_url = "https://name.vault.azure.net/", server = "SERVER", name = "DBNAME", user = "USERID", password = "PASSID"):
        from azure.keyvault.secrets import SecretClient
        from azure.identity import AzureCliCredential

        credential = AzureCliCredential()
        client = SecretClient(vault_url = kv_url, credential = credential)
        self.server = client.get_secret(server).value 
        self.name = client.get_secret(name).value
        self.user = client.get_secret(user).value
        self.password = client.get_secret(password).value

    def set_variables_json(self, path_file_name="pass.json"):
        """
        Sets the parameters, from local machine to connect to Database engine.

        :param server: {str} :: Server name with SQL:
        :param dbname: {str} :: Database name in {server},
        :param userID: {str} :: User name in {server} with access to {dbname},
        :param passID: {str} :: Password for {User} in {server} with access to {dbname}

        :return:
            set of strings (server, dbname, userID, passID)
        """
        fileToOpen = open(path_file_name)
        secretsFile = json.load(fileToOpen)
        self.server = secretsFile["SERVER"]
        self.name = secretsFile["DBNAME"]
        self.user = secretsFile["USERID"]
        self.password = secretsFile["PASSID"]
    
    def create_conection(self):
        """
        Create conection with database.
        """
        driver, server, dbname, userID, passID = self.get_configuration()
        connectionstring = 'mssql+pyodbc://{uid}:{password}@{server}:1433/{database}?driver={driver}'.format(
            uid = userID,
            password = passID,
            server = server,
            database = dbname,
            driver = driver.replace(' ', '+'))

        self.conection = create_engine(connectionstring)
    
    def data_get_sql_as_df(self, sql) -> pd.DataFrame:
        """
        Capture SQL formula and transform into pandas object.
        :param sql: SQL formula to execute on Database f.ex. 'Select * From TableName'
        :return:
        df :: {pandas.DataFrame} :: Object with SQL data
        """
        return pd.read_sql(sql, self.conection)
    
    def data_get_sql_with_params_as_df(self, sql, param) -> pd.DataFrame:
        """
        Capture SQL formula and transform into pandas object.
        :param sql: SQL formula to execute on Database f.ex. 'Select * From TableName'
        :param param: parameters to include into SQL, defence SQL INJECTION.
        
        Example:
        sql = "select TOP (1) * from Customers where ID = ?"
        params = (id, )
        finall_query "select TOP (1) * from Customers where ID = id"

        :return:
        df :: {pandas.DataFrame} :: Object with SQL data
        """
        return pd.read_sql(sql, self.conection, params = param)

    def close_connection(self) -> None:
        """
        Disconnect with db engine.
        """
        self.conection.close()

    def exec(self, sql) -> None:
        """
        Execute SQL formulas (Update, Delete, Insert, others...).
        :param sql: SQL formula to execute on Database f.ex. 'Select * From TableName'
        """
        self.conection.execute(sql)

    def get_configuration(self) -> tuple:
        """
        Returns tuple of secrets.
        """
        return self.driver, self.server, self.name, self.user, self.password
    
    def data_save_dataframe(self, df, tableName = ""):
        """
        Save data from a dataframe into Database
        :param df: dataframe (local table) to save on 
        """
        df.to_sql(tableName, self.conection, if_exists = 'append', index = False)

    def data_save_dataframes_list(self, data_dict):
        """
        Save data from a dataframes into Database. Dataframes need to be pass as a list, of dictionaries like:
        [{
            "dataframe":df,
            "tablename":"tablename"
        },
        ...
        {
            "dataframe":df_n,
            "tablename":"tablename_n"
        }]
        """
        with self.conection.begin() as conn:
            for df in data_dict:
                print("Saving to", df["tablename"], "with rows:", len(df["dataframe"]))
                df["dataframe"].to_sql(df["tablename"], con=conn, if_exists = 'append', index = False)

    def data_save_csv_dataframes_list(self, data_dict):
        for df in data_dict:
            print(" Saving to csv", df["tablename"], "with rows:", len(df["dataframe"]))
            df["dataframe"].to_csv(df["tablename"], index = False)

    