import mysql.connector
from mysql.connector import errorcode

def get_connection():
    try:
        cnx = mysql.connector.connect(
            user="avnadmin",
            password="AVNS_PABaDsGOCGohlv4zyPJ",
            host="mysql-papeleria-pinonagustin3-e056.b.aivencloud.com",
            port=10136,
            database="defaultdb",
            ssl_ca="ca.pem",
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
