# src/model/naval_warfare.py

def create_matrix():
    """
    Crea una matriz de 5x5 inicializada en 0.
    Representa el tablero de juego.
    """
    w, h = 5, 5
    return [[0 for _ in range(w)] for _ in range(h)]

def convert_location(position: str) -> tuple:
    """
    Convierte una posición en formato 'A1', 'B3', etc., a índices de matriz (fila, columna).
    """
    letras = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
    try:
        letra = position[0].upper()
        fila = int(position[1]) - 1
        columna = letras[letra]
        return fila, columna
    except (IndexError, KeyError, ValueError):
        raise ValueError("Posición inválida. Use formato 'A1' a 'E5'.")

class Player:
    def __init__(self, id, name: str):
        """
        Inicializa un jugador con un identificador, nombre, número de barcos, y tableros.
        """
        self.id = id
        self.name = name
        self.ships: int = 3  # Número total de barcos
        self.ships_in_game = 0  # Barcos en el juego
        self.board = create_matrix()  # Tablero de barcos
        self.board_attack = create_matrix()  # Tablero de ataques

    def colocar_barco(self, fila, columna):
        """
        Coloca un barco en la posición dada en el tablero del jugador.
        """
        if self.board[fila][columna] == 0:
            self.board[fila][columna] = 1  # Marcamos el barco en la matriz
            self.ships_in_game += 1
            return True
        else:
            raise ValueError("Ya hay un barco en esa posición.")

class NavalWarfare:
    def __init__(self, player1: Player, player2: Player):
        """
        Inicializa el juego con dos jugadores.
        """
        self.Player1 = player1
        self.Player2 = player2
        self.currentplayer = self.Player1  # Comienza con el primer jugador

    def posicionate_ship(self, position: str):
        """
        Permite al jugador actual colocar un barco en una posición.
        """
        fila, columna = convert_location(position)
        self.currentplayer.colocar_barco(fila, columna)

    def shoot(self, position: str):
        """
        Realiza un disparo en la posición dada por el jugador actual.
        """
        fila, columna = convert_location(position)
        opponent = self.Player2 if self.currentplayer == self.Player1 else self.Player1

        if opponent.board[fila][columna] == 1:
            # Marcamos el barco como golpeado
            opponent.board[fila][columna] = 2
            self.currentplayer.board_attack[fila][columna] = 2
            opponent.ships_in_game -= 1  # Restamos un barco al oponente
            return True  # Éxito, tocado
        else:
            # Marcamos el disparo fallido
            self.currentplayer.board_attack[fila][columna] = -1
            return False  # Fallo, agua

    def update_current_player(self):
        """
        Cambia al siguiente jugador.
        """
        self.currentplayer = self.Player2 if self.currentplayer == self.Player1 else self.Player1

    def game_over(self):
        """
        Verifica si alguno de los jugadores ha perdido todos sus barcos.
        """
        return self.Player1.ships_in_game == 0 or self.Player2.ships_in_game == 0

    def get_winner(self):
        """
        Devuelve el ganador si el juego ha terminado.
        """
        if self.Player1.ships_in_game == 0:
            return self.Player2  # El segundo jugador es el ganador
        elif self.Player2.ships_in_game == 0:
            return self.Player1  # El primer jugador es el ganador
        else:
            return None  # El juego no ha terminado

    def display_board(self, player):
        """
        Devuelve una representación del tablero de un jugador.
        """
        board = ""
        for row in player.board_attack:
            board += " ".join(str(cell) for cell in row) + "\n"
        return board
