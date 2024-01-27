import pyodbc, struct
import os

# Función para conectar y desconectar
def get_connection():
    connection = pyodbc.connect('Drives')
    cursor = connection.cursor()
    return connection, cursor

def close_connection(connection, cursor):
    cursor.close()
    connection.close()
