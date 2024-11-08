class Jugador:
    def __init__(self, id=None, nombre=None):
        self.id = id
        self.nombre = nombre

    def validar_nombre(self):
        if not self.nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if len(self.nombre) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        return True

