# src/model/player_model.py

class Jugador:
    def __init__(self, id=None, nombre=None):
        self.id = id
        self.nombre = nombre

    def validar_nombre(self):
        if not self.nombre:
            raise ValueError("El nombre no puede estar vacío.")
        return True
