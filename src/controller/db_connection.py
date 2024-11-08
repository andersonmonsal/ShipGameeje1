#src/controller/db_connection.py
import sys
import os

# Obtener la ruta absoluta de la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import psycopg2
import config

def get_connection():
    try:
        connection = psycopg2.connect(
            host=config.PGHOST,
            database=config.PGDATABASE,
            user=config.PGUSER,
            password=config.PGPASSWORD,
            port=config.PGPORT
        )
        return connection
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

