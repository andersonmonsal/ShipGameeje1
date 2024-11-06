import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.controller.db_connection import get_connection  # Para conectarse a la base de datos
from src.controller.game_controller import GameController
import psycopg2

app = Flask(__name__)
game_controller = GameController()

# Conexión a la base de datos
def conectar_db():
    conn = psycopg2.connect(get_connection)
    return conn

# Ruta principal - Página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para mostrar todos los jugadores
@app.route('/players')
def players():
    players = game_controller.obtener_todos_los_jugadores()
    return render_template('player.html', players=players)

# Ruta para crear un jugador
@app.route('/create_player', methods=['POST'])
def create_player():
    name = request.form['name']
    player = game_controller.crear_jugador(name)
    if player:
        return redirect(url_for('players'))
    return 'Error al crear el jugador', 400

# Ruta para actualizar un jugador
@app.route('/update_player/<int:player_id>', methods=['POST'])
def update_player(player_id):
    name = request.form['name']
    if game_controller.actualizar_jugador(player_id, name):
        return redirect(url_for('players'))
    return 'Error al actualizar el jugador', 400

# Ruta para eliminar un jugador
@app.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    if game_controller.eliminar_jugador(player_id):
        return redirect(url_for('players'))
    return 'Error al eliminar el jugador', 400

# Ruta para mostrar la página del juego
@app.route('/game')
def game():
    players = game_controller.obtener_todos_los_jugadores()
    return render_template('game.html', players=players)

# Ruta para iniciar el juego
@app.route('/start_game', methods=['POST'])
def start_game():
    player1_id = int(request.form['player1_id'])
    player2_id = int(request.form['player2_id'])
    
    if game_controller.iniciar_juego(player1_id, player2_id):
        return redirect(url_for('play_game'))
    return 'Error al iniciar el juego', 400

# Ruta para jugar el juego
@app.route('/play')
def play_game():
    if game_controller.juego:
        return render_template('play.html', 
                             game=game_controller.juego,
                             current_player=game_controller.juego.currentplayer)
    return redirect(url_for('game'))

# Ruta para colocar un barco
@app.route('/place_ship', methods=['POST'])
def place_ship():
    position = request.form['position']
    if game_controller.colocar_barco(position):
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Error al colocar el barco'})

# Ruta para realizar un disparo
@app.route('/shoot', methods=['POST'])
def shoot():
    position = request.form['position']
    result = game_controller.realizar_disparo(position)
    
    response = {
        'success': True if result else False,
        'hit': result,
        'game_over': game_controller.verificar_fin_juego()
    }
    
    if response['game_over']:
        winner = game_controller.obtener_ganador()
        if winner:
            response['winner'] = winner.nombre
            game_controller.actualizar_juego(game_controller.juego_id, 'finalizado', winner.id)
    
    return jsonify(response)

# Ruta para cambiar de turno
@app.route('/switch_turn', methods=['POST'])
def switch_turn():
    game_controller.cambiar_turno()
    return jsonify({'success': True})

# Ruta para obtener el tablero del jugador actual
@app.route('/get_board')
def get_board():
    if game_controller.juego and game_controller.juego.currentplayer:
        board = game_controller.juego.currentplayer.board
        board_attack = game_controller.juego.currentplayer.board_attack
        return jsonify({
            'board': board,
            'board_attack': board_attack
        })
    return jsonify({'error': 'No hay juego en curso'}), 400

# Ruta para registrar un nuevo jugador
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    # Cambié 'registrar_jugador' por 'crear_jugador', ya que es el método correcto
    player = game_controller.crear_jugador(name)
    if player:
        return redirect(url_for('players'))
    return 'Error al registrar el jugador', 400

# Otra ruta para registrar un jugador (opcional)
@app.route('/registrar_jugador', methods=['POST'])
def registrar_jugador():
    nombre = request.form['nombre']
    jugador = game_controller.crear_jugador(nombre)
    
    if jugador:
        return f"Jugador {jugador.nombre} registrado con éxito!"
    else:
        return "No se pudo registrar al jugador."
    
if __name__ == '__main__':
    app.run(debug=True)
