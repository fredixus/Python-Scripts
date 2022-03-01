use DatabaseName

DECLARE @id int, @text_identity varchar(20)

while (
		SELECT COUNT(*) FROM (
			SELECT text_identity FROM TableName GROUP BY text_identity HAVING COUNT(text_identity)>1
		)temp_table_1
	) > 0

	BEGIN
		SET @text_identity = (SELECT TOP 1 text_identity FROM (SELECT text_identity FROM TableName GROUP BY text_identity HAVING COUNT(text_identity) > 1) temp_table_1)
		SET @id = (SELECT top 1 ID FROM TableName WHERE text_identity = @text_identity)
		DELETE FROM SPC_data WHERE ID = @id
	END

---


