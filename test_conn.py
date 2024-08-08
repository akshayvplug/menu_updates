from connection import db_connection  # Import the db_connection context manager
import mysql.connector.pooling

# Table name for which you want to view the columns
table_name = "olo_menu.olk"

try:
    with db_connection() as cursor:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [column['Field'] for column in cursor.fetchall()]

    print(f"Columns in table {table_name}:")
    for column in columns:
        print(column)

except mysql.connector.Error as error:
    print(f"Error: {error}")
