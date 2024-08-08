
# Configuration file for Database.
import os

dbconfig = {
    "development": {
        "host": "ginastg.voiceplug.net",
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        # "database": "vporder_test",
        "CONNECTION_POOL_SIZE" : 2,
        "CONNECTION_POOL_NAME": "MYPOOL"
    },
    "production": {
        "host": "rdsprod.voiceplug.net",
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        # "database": "voiceplugorder",
        "CONNECTION_POOL_SIZE" : 2,
        "CONNECTION_POOL_NAME": "MYPOOL"
    },
}

cache_config = {
    "ttl": 24*60*60
}

TABLE_MENU_ITEMS = "MENUITEMS"