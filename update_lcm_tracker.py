import pandas as pd
import mysql.connector
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from connection import cnxpool
from datetime import datetime, timedelta
from sqlalchemy import create_engine

today_date = datetime.now().strftime('%Y-%m-%d')
yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')



cnx = cnxpool.get_connection()
try:
    cursor = cnx.cursor(dictionary = True)
    # yield cursor   # SQL query
    sql_query = f"""
        USE live_call_monitor;
        SELECT 
            customer_phone_number, tracker_id, start_date, updated_date, client, location, processor, 
            customer_name, language, remark, call_type, ordered_by, order_number, order_total, 
            button_action, call_uuid, phc_id, rest_zip, rest_unique_id, duration
        FROM lcm_tracker 
        WHERE updated_date BETWEEN '2023-11-26 09:00:00' AND '2023-11-27 09:00:00' 
        WHERE customer_phone_number like '%+1%' and updated_date BETWEEN '{yesterday_date} 09:00:00' AND '{today_date} 09:00:00' 
        ORDER BY tracker_id DESC;
    """

    cursor.execute(sql_query)
    # Fetch all results into a DataFrame
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)

    # Close the database connection
    cursor.close()

    # Export the DataFrame to an Excel file with formatting
    excel_file = "output_data.xlsx"
    wb = Workbook()
    ws = wb.active

    # Write the DataFrame to the Excel worksheet while maintaining formatting
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Apply number formatting for date/time columns
    date_time_columns = ['start_date', 'updated_date', 'UTC start time', 'PST Date']
    date_format = 'MM-DD-YYYY HH:MM'
    for col in date_time_columns:
        for cell in ws[col][1:]:
            cell.number_format = date_format

    # Save the Excel file
    wb.save(excel_file)
    print(f"Data exported to '{excel_file}' successfully.")
except Exception as e:
    print(e)
