import pandas as pd
import mysql.connector.pooling
from connection import db_connection
# cnx = cnxpool.get_connection()
# cursor = cnx.cursor(dictionary = True)
# Fetch data from the table
# cursor = connection.cursor()
rest_abbr = 'olk'
# Fetch distinct store_id values
with db_connection() as cursor:
    olo_table_name = f"olo_menu.{rest_abbr}"
    query_distinct_store_ids = f"SELECT DISTINCT store_id FROM {olo_table_name};"
    cursor.execute(query_distinct_store_ids)
    distinct_store_ids = cursor.fetchall()
    print(distinct_store_ids)
    # Iterate over distinct store_id values
    for store_id_dict in distinct_store_ids:
        store_id = store_id_dict['store_id']
        table_name = f"menu_extracts.{rest_abbr}_{store_id}"
        # Drop table if it already exists
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(drop_table_query)
        # Create table for each store_id
        create_table_query = f"""
        CREATE TABLE {table_name} AS
        SELECT * FROM {olo_table_name} WHERE store_id = {store_id};
        """
        cursor.execute(create_table_query)

        # Remove store_id column from the newly created tables
        alter_table_query = f"""
        ALTER TABLE {table_name}
        DROP COLUMN store_id;
        """
        cursor.execute(alter_table_query)
        print(f"done for store {store_id}")

    # Commit changes and close the connection
    # cursor.commit()
    cursor.close()