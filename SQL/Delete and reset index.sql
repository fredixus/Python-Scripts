USE DatabaseName

-- Delete filtered data
DELETE FROM TableName WHERE ID > 10 
GO

-- All Data
--TRUNCATE TABLE TableName
--GO

DBCC CHECKIDENT ('TableName', RESEED, 1)
GO
