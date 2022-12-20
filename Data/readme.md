
# Dataimport

## Password file:

``` json
{
    "SERVER":"server.database.windows.net",
    "DBNAME":"database name",
    "USERID":"user",
    "PASSID":"password"
}
```
### How to work with it

1. Create database object
    ``` python
    db = database()
    ```

1. Get connection data (User, Password, Database name, Server Name)
    ``` python
    db.set_variables_json()
    ```

1. Once you get secreets connect with database:
    ``` python
    db.create_conection()
    ```

1. Work with object
    * Get (SELECT) data as python dataframe
    ``` python
    db.data_get_sql_as_df("select * from Test")
    ```

    * Use SQL engine to commit database operations
    ``` python
    transaction = """
    BEGIN TRANSACTION; 
    update Test SET Color = 'Orange' WHERE ID = 1; 
    update Test SET Value = 'WEB' WHERE ID = 1; 
    COMMIT TRANSACTION;
    """

    db.exec(transaction)
    ```

    * Save multi dataframes (for data pipeline) in transaction
    ``` python
    df = pd.DataFrame(data= {"Date":[dt.now()],"Color":["Yellow"],"Value":[1.510]})
    df2 = pd.DataFrame(data= {"Date":[dt.now()],"Color":["Blue"],"Value":[2.0]})

    test =  [{
                "dataframe": df,
                "tablename":"Test"
            },
            {
                "dataframe": df2,
                "tablename":"Test"
            }]

    db.data_save_dataframes_list(test)
    ```


