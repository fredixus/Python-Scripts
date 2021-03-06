DECLARE @ParameterList TABLE(ParameterName nvarchar(255), OperationTyp nvarchar(30), DataTyp nvarchar(20))

INSERT INTO @ParameterList (ParameterName, OperationTyp, DataTyp) VALUES
-- Pass one type in one time!
/*('Parameter1','cast','as char(10)')
,('Parameter2','cast','as char(25)')*/
('Parameter3','cast','as float')
,('Parameter4','cast','as float')
,('Parameter5','cast','as float')
/*,('Parameter6','cast','as varchar(15)')
,('Parameter7','cast','as varchar(15)')
,('Parameter8','cast','as char(15)')*/
 
PRINT N'Parameters are ready'
  
while (1 = 1)
  BEGIN
	DECLARE @CurrentParameter nvarchar(255) 
	SET @CurrentParameter = (SELECT TOP(1) ParameterName FROM @ParameterList)
	
	IF @CurrentParameter IS NULL
       BREAK

	DECLARE @CurrentOperationType nvarchar(255) 
	SET @CurrentOperationType = (SELECT OperationTyp FROM @ParameterList WHERE ParameterName = @CurrentParameter)

	DECLARE @CurrentDataType nvarchar(255) 
	SET @CurrentDataType = (SELECT DataTyp FROM @ParameterList WHERE ParameterName = @CurrentParameter)

	PRINT N'Copy data for: ' + @CurrentParameter

	-------------
	DECLARE @SQL VARCHAR(MAX) = 
	'update TABLE_UNPIVOTED 
	  SET ' + @CurrentParameter + ' = TEMP_TABLE.CurrentValueOFParameter
	  FROM 
	  (
		SELECT 
			t1.ID,
			t1.SAVE_DATE,

			'+@CurrentOperationType+'( replace(t2.VALUE, '','',''.'') '+@CurrentDataType+') as CurrentValueOFParameter
			FROM TABLE_UNPIVOTED t1
			left join 
				(SELECT * FROM TABLE_PIVOTED WHERE parameter = ''' + @CurrentParameter + ''') t2
			on (t1.ID = t2.ID 
			and t1.SAVE_DATE = t2.SAVE_DATE)
			WHERE t1.SAVE_DATE > ''2020-01-01'' and t1.SAVE_DATE < ''2020-02-01''
	  ) TEMP_TABLE
	 WHERE
	 TEMP_TABLE.ID = TABLE_UNPIVOTED.ID
	 and TEMP_TABLE.SAVE_DATE = TABLE_UNPIVOTED.SAVE_DATE'

	 -- Match key on two columns

	 EXEC (@SQL)
	-------------
	DELETE FROM @ParameterList WHERE ParameterName = @CurrentParameter
	
  END
  GO