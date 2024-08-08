


import mysql.connector
from get_xml import Menu
from extract import parse_xml
from typing import Text
from zipfile import ZipFile
from connection import db_connection
import logging
import json
import pandas as pd

try:
    with db_connection() as cursor:
        cursor.execute(f'''SELECT * FROM voiceplugorder.nlu_conversations 
                          WHERE created_at BETWEEN '2024-01-30 15:00:00' AND '2024-01-31 10:00:00'
                          AND (rest_id = 60 OR rest_id > 71);''')

        # Fetch all the results
        results = cursor.fetchall()

        # Create a dataframe from the fetched results
        df = pd.DataFrame(results)


        def parse_dict(string_dict):
            try:
                return json.loads(string_dict)
            except json.JSONDecodeError:
                return {}

        # Convert string representation of dictionaries into actual dictionaries
        dicts = [parse_dict(conversation) for conversation in df['conversation_jobj']]

        # Filter out empty dictionaries
        non_empty_dicts = [conversation for conversation in dicts if conversation]


        # Define the search phrase
        search_phrase = "Transferring the call to our representative who will assist you with the order."

        # Initialize a dictionary to track counts for each key
        key_count = {str(i): 0 for i in range(15)}

        # Iterate over each conversation dictionary
        for conversation in non_empty_dicts:
            found_keys = set()
            # Check if the phrase is present in the "NLU" list
            for key, value in conversation.items():
                if isinstance(value, dict) and "NLU" in value:
                    if search_phrase in value["NLU"]:
                        found_keys.add(key)
            # Update the key_count dictionary
            for key in found_keys:
                key_count[key] += 1

        print(key_count)
        

except Exception as e:
    print("Error:", e)