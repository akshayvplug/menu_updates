import os
#from sanic.log import logger
from contextlib import contextmanager

import mysql.connector.pooling
from config import dbconfig

# Fetch configuration for the environment.
d_config = dbconfig.get('production')

cnxpool = mysql.connector.pooling.MySQLConnectionPool(
            buffered = True,
            host = d_config['host'],
            user = d_config['user'],
            password = d_config['password'],
            # database = d_config['database'],
            auth_plugin = "mysql_native_password",
            pool_name = d_config['CONNECTION_POOL_NAME'],
            pool_size = d_config['CONNECTION_POOL_SIZE'],
        )

@contextmanager
def db_connection():
    cnx = cnxpool.get_connection()
    try:
        cursor = cnx.cursor(dictionary = True)
        yield cursor
    finally:
        #logger.debug(msg= f"Releasing the connection back to Connection Pool.")
        cnx.commit()
        cnx.close()