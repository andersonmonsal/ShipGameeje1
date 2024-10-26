#src/controller/game_controller.py
import sys
sys.path.append("src")

from model.player_model import Jugador 
from model.naval_warfare import NavalWarfare, Player, convert_location
from controller.db_connection import get_connection
class GameController:
    def __init__(self):
        pass # pen desarrollo

    def crear_jugador(self, nombre):
        jugador = Jugador(nombre=nombre)
        return jugador.crear()

    def obtener_jugador(self, jugador_id):
        return Jugador.obtener_por_id(jugador_id)

    def actualizar_jugador(self, jugador_id, nuevo_nombre):
        jugador = Jugador.obtener_por_id(jugador_id)
        if jugador:
            return jugador.actualizar(nuevo_nombre)
        else:
            print("Jugador no encontrado.")
            return False

    def eliminar_jugador(self, jugador_id):
        jugador = Jugador.obtener_por_id(jugador_id)
        if jugador:
            return jugador.eliminar()
        else:
            print("Jugador no encontrado.")
            return False

    def obtener_todos_los_jugadores(self):
        return Jugador.obtener_todos()

    def iniciar_juego(self, jugador1_id, jugador2_id):
        jugador1 = Jugador.obtener_por_id(jugador1_id)
        jugador2 = Jugador.obtener_por_id(jugador2_id)
        if jugador1 and jugador2:
            player1 = Player(jugador1.id, jugador1.nombre)
            player2 = Player(jugador2.id, jugador2.nombre)
            self.juego = NavalWarfare(player1, player2)
            return True
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
