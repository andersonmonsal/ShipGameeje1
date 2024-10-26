# src/model/naval_warfare.py

def create_matrix():
    w, h = 5, 5
    return [[0 for _ in range(w)] for _ in range(h)]

def convert_location(position: str) -> tuple:
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
        self.id = id
        self.name = name
        self.ships: int = 3
        self.ships_in_game = 0
        self.board = create_matrix()
        self.board_attack = create_matrix()

    def colocar_barco(self, fila, columna):
        if self.board[fila][columna] == 0:
            self.board[fila][columna] = 1
            self.ships_in_game += 1
            return True
        else:
            raise ValueError("Ya hay un barco en esa posición.")

class NavalWarfare:
    def __init__(self, player1: Player, player2: Player):
        self.Player1 = player1
        self.Player2 = player2
        self.currentplayer = self.Player1

    def posicionate_ship(self, position: str):
        fila, columna = convert_location(position)
        self.currentplayer.colocar_barco(fila, columna)

    def shoot(self, position: str):
        fila, columna = convert_location(position)
        opponent = self.Player2 if self.currentplayer == self.Player1 else self.Player1

        if opponent.board[fila][columna] == 1:
            opponent.board[fila][columna] = 2  # Marcamos como golpeado
            self.currentplayer.board_attack[fila][columna] = 2
            opponent.ships_in_game -= 1
            return True
        else:
            self.currentplayer.board_attack[fila][columna] = -1
            return False

    def update_current_player(self):
        self.currentplayer = self.Player2 if self.currentplayer == self.Player1 else self.Player1

    def game_over(self):
        return self.Player1.ships_in_game == 0 or self.Player2.ships_in_game == 0

    def get_winner(self):
        if self.Player1.ships_in_game == 0:
            return self.Player2
        elif self.Player2.ships_in_game == 0:
            return self.Player1
        else:
            return None
