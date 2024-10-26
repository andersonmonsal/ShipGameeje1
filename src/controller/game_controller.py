# src/controller/game_controller.py

from model.player_model import Jugador
from model.naval_warfare import NavalWarfare, Player
from controller.db_connection import get_connection

class GameController:
    def __init__(self):
        self.juego = None
        self.juego_id = None 

    def crear_jugador(self, nombre):
        jugador = Jugador(nombre=nombre)
        try:
            jugador.validar_nombre()
        except ValueError as e:
            print(e)
            return None

        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO jugadores (nombre) VALUES (%s) RETURNING id;",
                    (jugador.nombre,)
                )
                jugador.id = cursor.fetchone()[0]
                connection.commit()
                print(f"Jugador creado con ID: {jugador.id}")
                return jugador
            except Exception as e:
                print(f"Error al crear jugador: {e}")
                connection.rollback()
                return None
            finally:
                cursor.close()
                connection.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
        return None

    def obtener_jugador(self, jugador_id):
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
                    return Jugador(id=result[0], nombre=result[1])
                else:
                    return None
            except Exception as e:
                print(f"Error al obtener jugador: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
        return None

    def actualizar_jugador(self, jugador_id, nuevo_nombre):
        try:
            jugador = Jugador(id=jugador_id, nombre=nuevo_nombre)
            jugador.validar_nombre()
        except ValueError as e:
            print(e)
            return False

        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "UPDATE jugadores SET nombre = %s WHERE id = %s;",
                    (jugador.nombre, jugador.id)
                )
                if cursor.rowcount == 0:
                    print("Jugador no encontrado.")
                    return False
                connection.commit()
                print(f"Jugador con ID {jugador.id} actualizado.")
                return True
            except Exception as e:
                print(f"Error al actualizar jugador: {e}")
                connection.rollback()
                return False
            finally:
                cursor.close()
                connection.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
        return False

    def eliminar_jugador(self, jugador_id):
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "DELETE FROM jugadores WHERE id = %s;",
                    (jugador_id,)
                )
                if cursor.rowcount == 0:
                    print("Jugador no encontrado.")
                    return False
                connection.commit()
                print(f"Jugador con ID {jugador_id} eliminado.")
                return True
            except Exception as e:
                print(f"Error al eliminar jugador: {e}")
                connection.rollback()
                return False
            finally:
                cursor.close()
                connection.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
        return False

    def obtener_todos_los_jugadores(self):
        connection = get_connection()
        jugadores = []
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT id, nombre FROM jugadores;")
                resultados = cursor.fetchall()
                for row in resultados:
                    jugadores.append(Jugador(id=row[0], nombre=row[1]))
                return jugadores
            except Exception as e:
                print(f"Error al obtener jugadores: {e}")
                return []
            finally:
                cursor.close()
                connection.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
        return jugadores

    def iniciar_juego(self, jugador1_id, jugador2_id):
        jugador1 = self.obtener_jugador(jugador1_id)
        jugador2 = self.obtener_jugador(jugador2_id)
        if jugador1 and jugador2:
            player1 = Player(jugador1.id, jugador1.nombre)
            player2 = Player(jugador2.id, jugador2.nombre)
            self.juego = NavalWarfare(player1, player2)
            # Crear el juego en la base de datos
            self.juego_id = self.crear_juego(jugador1_id, jugador2_id)
            if self.juego_id:
                return True
            else:
                print("No se pudo crear el juego en la base de datos.")
                return False
        else:
            print("Uno o ambos jugadores no existen.")
            return False

    def colocar_barco(self, position):
        try:
            self.juego.posicionate_ship(position)
            return True
        except ValueError as e:
            print(e)
            return False

    def realizar_disparo(self, position):
        try:
            resultado = self.juego.shoot(position)
            return resultado
        except ValueError as e:
            print(e)
            return False

    def cambiar_turno(self):
        self.juego.update_current_player()

    def verificar_fin_juego(self):
        return self.juego.game_over()

    def obtener_ganador(self):
        return self.juego.get_winner()

    def crear_juego(self, jugador1_id, jugador2_id):
        """Crea un nuevo juego en la base de datos y retorna el ID del juego."""
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO juegos (jugador1_id, jugador2_id, estado) VALUES (%s, %s, %s) RETURNING id;",
                    (jugador1_id, jugador2_id, 'en progreso')
                )
                juego_id = cursor.fetchone()[0]
                connection.commit()
                print(f"Juego creado con ID: {juego_id}")
                return juego_id
            except Exception as e:
                print(f"Error al crear juego: {e}")
                connection.rollback()
                return None
            finally:
                cursor.close()
                connection.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return None

    def actualizar_juego(self, juego_id, estado, ganador_id=None):
        """Actualiza el estado y el ganador del juego en la base de datos."""
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "UPDATE juegos SET estado = %s, ganador_id = %s WHERE id = %s;",
                    (estado, ganador_id, juego_id)
                )
                if cursor.rowcount == 0:
                    print(f"No se encontró el juego con ID {juego_id}.")
                    return False
                connection.commit()
                print(f"Juego con ID {juego_id} actualizado.")
                return True
            except Exception as e:
                print(f"Error al actualizar juego: {e}")
                connection.rollback()
                return False
            finally:
                cursor.close()
                connection.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return False

    # Método para limpiar la base de datos (solo para pruebas)
    def limpiar_base_de_datos(self):
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM tableros;")
                cursor.execute("DELETE FROM juegos;")
                cursor.execute("DELETE FROM jugadores;")
                connection.commit()
                print("Base de datos limpiada.")
            except Exception as e:
                print(f"Error al limpiar la base de datos: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
