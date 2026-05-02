import os
from dotenv import load_dotenv

import mysql.connector
from mysql.connector import errorcode

def get_connection():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ca_path = os.path.join(current_dir, "ca.pem")
    DB_PASSWORD = os.getenv("AIVEN_DB_PASSWORD")
    DB_USER = os.getenv("AIVEN_DB_USER")
    DB_HOST = os.getenv("AIVEN_DB_HOST")
    DB_PORT = os.getenv("AIVEN_DB_PORT")
    DB_NAME = os.getenv("AIVEN_DB_NAME")
    try:
        cnx = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            ssl_ca=ca_path,
            ssl_verify_cert=True
        )
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ Usuario o contraseña incorrectos")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("❌ La base de datos no existe")
        else:
            print(f"❌ Error: {err}")
        return None
