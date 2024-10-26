#src/model/player_model.py
import sys
sys.path.append("src")

from controller.db_connection import get_connection

class Jugador:
    def __init__(self, id=None, nombre=None):
        self.id = id
        self.nombre = nombre

    def crear(self):
        if not self.nombre:
            print("El nombre no puede estar vacío.")
            return None
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO jugadores (nombre) VALUES (%s) RETURNING id;",
                    (self.nombre,)
                )
                self.id = cursor.fetchone()[0]
                connection.commit()
                return self
            except Exception as e:
                print(f"Error al crear jugador: {e}")
                connection.rollback()
                return None
            finally:
                cursor.close()
                connection.close()

    def actualizar(self, nuevo_nombre):
        if not nuevo_nombre:
            print("El nuevo nombre no puede estar vacío.")
            return False
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "UPDATE jugadores SET nombre = %s WHERE id = %s;",
                    (nuevo_nombre, self.id)
                )
                if cursor.rowcount == 0:
                    print("Jugador no encontrado.")
                    return False
                connection.commit()
                self.nombre = nuevo_nombre
                return True
            except Exception as e:
                print(f"Error al actualizar jugador: {e}")
                connection.rollback()
                return False
            finally:
                cursor.close()
                connection.close()

    def eliminar(self):
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "DELETE FROM jugadores WHERE id = %s;",
                    (self.id,)
                )
                if cursor.rowcount == 0:
                    print("Jugador no encontrado.")
                    return False
                connection.commit()
                return True
            except Exception as e:
                print(f"Error al eliminar jugador: {e}")
                connection.rollback()
                return False
            finally:
                cursor.close()
                connection.close()

    @classmethod
    def obtener_por_id(cls, jugador_id):
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "SELECT id, nombre FROM jugadores WHERE id = %s;",
                    (jugador_id,)
                )
                result = cursor.fetchone()
                if result:
                    return cls(id=result[0], nombre=result[1])
                else:
                    return None
            except Exception as e:
                print(f"Error al obtener jugador: {e}")
                return None
            finally:
                cursor.close()
                connection.close()

    @classmethod
    def obtener_todos(cls):
        connection = get_connection()
        jugadores = []
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT id, nombre FROM jugadores;")
                resultados = cursor.fetchall()
                for row in resultados:
                    jugadores.append(cls(id=row[0], nombre=row[1]))
                return jugadores
            except Exception as e:
                print(f"Error al obtener jugadores: {e}")
                return []
            finally:
                cursor.close()
                connection.close()
        return jugadores
