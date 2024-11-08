# test/test_player.py

import sys
sys.path.append("src")

import unittest
from controller.game_controller import GameController

class TestJugadorModelo(unittest.TestCase):
    def setUp(self):
        self.controller = GameController()
        self.controller.limpiar_base_de_datos()

    def test_crear_jugador_exitoso(self):
        jugador = self.controller.crear_jugador("JugadorPrueba")
        self.assertIsNotNone(jugador)
        self.assertIsNotNone(jugador.id)
        self.assertEqual(jugador.nombre, "JugadorPrueba")

    def test_crear_jugador_error(self):
        jugador = self.controller.crear_jugador("")
        self.assertIsNone(jugador)

    def test_actualizar_jugador_exitoso(self):
        jugador = self.controller.crear_jugador("JugadorActualizar")
        resultado = self.controller.actualizar_jugador(jugador.id, "NuevoNombre")
        self.assertTrue(resultado)
        jugador_actualizado = self.controller.obtener_jugador(jugador.id)
        self.assertEqual(jugador_actualizado.nombre, "NuevoNombre")

    def test_actualizar_jugador_error(self):
        resultado = self.controller.actualizar_jugador(9999, "NombreInexistente")
        self.assertFalse(resultado)

    def test_eliminar_jugador_exitoso(self):
        jugador = self.controller.crear_jugador("JugadorEliminar")
        resultado = self.controller.eliminar_jugador(jugador.id)
        self.assertTrue(resultado)
        jugador_eliminado = self.controller.obtener_jugador(jugador.id)
        self.assertIsNone(jugador_eliminado)

    def test_eliminar_jugador_error(self):
        resultado = self.controller.eliminar_jugador(9999)
        self.assertFalse(resultado)

    def test_obtener_jugador_no_existente(self):
        jugador = self.controller.obtener_jugador(9999)
        self.assertIsNone(jugador)

    def test_obtener_todos_los_jugadores(self):
        # Crear algunos jugadores
        self.controller.crear_jugador("Jugador1")
        self.controller.crear_jugador("Jugador2")
        jugadores = self.controller.obtener_todos_los_jugadores()
        self.assertEqual(len(jugadores), 2)
        nombres = [jugador.nombre for jugador in jugadores]
        self.assertIn("Jugador1", nombres)
        self.assertIn("Jugador2", nombres)

if __name__ == '__main__':
    unittest.main()
