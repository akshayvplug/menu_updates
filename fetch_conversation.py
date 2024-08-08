import mysql.connector
from connection import db_connection
import json
import pandas as pd

def parse_dict(string_dict):
    try:
        return json.loads(string_dict)
    except json.JSONDecodeError:
        return {}

def fetch_conversation(uuid, db_table):
    try:
        with db_connection() as cursor:
            # Use parameterized query to prevent SQL injection
            cursor.execute(f'''SELECT * FROM {db_table} where call_uuid = %s;''', (uuid,))

            results = cursor.fetchall()

            data = parse_dict(results[0]['conversation_jobj'])
            print(data)
            with open("atest_data.json", 'w') as f:
                json.dump(data, f)

    except Exception as e:
        print(f"{e} ayayapeekapooo")

fetch_conversation('83023e1a-a6d5-4f87-8b2b-acbea9d9026f', 'voiceplugorder.nlu_conversations')