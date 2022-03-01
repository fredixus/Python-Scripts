DECLARE @ParameterList TABLE(ParameterName nvarchar(255), OperationTyp nvarchar(30), DataTyp nvarchar(20))
INSERT INTO @ParameterList (ParameterName, OperationTyp, DataTyp) Values
('Parameter1','cast','as varchar(25)')
,('Parameter2','cast','as varchar(8)')
,('Parameter3','cast','as float')
,('Parameter4','cast(replace',', '','', ''.'') as float')
,('Parameter5','cast','as datetime')
 
PRINT N'Parameters are ready'
  
WHILE (1 = 1)
  BEGIN
	DECLARE @CurrentParameter nvarchar(255) 
	SET @CurrentParameter = (SELECT TOP(1) ParameterName FROM @ParameterList)
	
	IF @CurrentParameter IS NULL
       BREAK

	DECLARE @CurrentOperationType nvarchar(255) 
	SET @CurrentOperationType = (SELECT OperationTyp FROM @ParameterList WHERE ParameterName = @CurrentParameter)

	DECLARE @CurrentDataType nvarchar(255) 
	SET @CurrentDataType = (SELECT DataTyp FROM @ParameterList WHERE ParameterName = @CurrentParameter)

	PRINT N'Copy data for: '+@CurrentParameter

	-------------
	DECLARE @SQL VARCHAR(MAX) = 
	'update TABLE_UNPIVOTED 
	  SET ' + @CurrentParameter + ' = TEMP_TABLE.CurrentValueOFParameter
	  FROM 
	  (
		SELECT 
			t1.ID,
			t1.SAVE_DATE,
			' + @CurrentOperationType + '(t2.VALUE ' + @CurrentDataType + ') as CurrentValueOFParameter
			FROM TABLE_UNPIVOTED t1
			left join 
				(SELECT * FROM TABLE_PIVOTED WHERE parameter = ''' + @CurrentParameter + ''') t2
			on (t1.ID = t2.ID 
			and t1.SAVE_DATE = t2.SAVE_DATE)
			WHERE t1.SAVE_DATE > ''2020-12-07'' 
			--and t1.SAVE_DATE <= ''2020-12-07''
	  ) TEMP_TABLE
	 WHERE
	 TEMP_TABLE.ID = TABLE_UNPIVOTED.ID
	 and TEMP_TABLE.SAVE_DATE = TABLE_UNPIVOTED.SAVE_DATE'

	 exec (@SQL)
	-------------
	delete FROM @ParameterList WHERE ParameterName = @CurrentParameter
	
  END
  Go

