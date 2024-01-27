import pyodbc, struct
import os

# Función para conectar y desconectar
def get_connection():
    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:library-usco.database.windows.net,1433;Database=library;Uid=admin_library;Pwd=Seminariousco123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = connection.cursor()
    return connection, cursor

def close_connection(connection, cursor):
    cursor.close()
    connection.close()