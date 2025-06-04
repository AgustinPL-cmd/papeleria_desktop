import mysql.connector
from mysql.connector import errorcode

def get_connection():
    try:
        cnx = mysql.connector.connect(
            user="root",
            password="12345",
            host="localhost",
            port=3306,
            database="Papeleria_Marlons"
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
