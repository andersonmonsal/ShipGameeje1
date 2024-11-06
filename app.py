import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
# app.py
# app.py
from src.controller.db_connection import get_connection  # Importa la función get_connection
from src.controller.game_controller import GameController
  # Asegúrate de que este archivo contenga la configuración correcta para tu base de datos
import psycopg2

app = Flask(__name__)
game_controller = GameController()

def conectar_db():
    conn = psycopg2.connect(get_connection)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/players')
def players():
    players = game_controller.obtener_todos_los_jugadores()
    return render_template('player.html', players=players)

@app.route('/create_player', methods=['POST'])
def create_player():
    name = request.form['name']
    player = game_controller.crear_jugador(name)
    if player:
        return redirect(url_for('players'))
    return 'Error al crear el jugador', 400

@app.route('/update_player/<int:player_id>', methods=['POST'])
def update_player(player_id):
    name = request.form['name']
    if game_controller.actualizar_jugador(player_id, name):
        return redirect(url_for('players'))
    return 'Error al actualizar el jugador', 400

@app.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    if game_controller.eliminar_jugador(player_id):
        return redirect(url_for('players'))
    return 'Error al eliminar el jugador', 400

@app.route('/game')
def game():
    players = game_controller.obtener_todos_los_jugadores()
    return render_template('game.html', players=players)

@app.route('/start_game', methods=['POST'])
def start_game():
    player1_id = int(request.form['player1_id'])
    player2_id = int(request.form['player2_id'])
    
    if game_controller.iniciar_juego(player1_id, player2_id):
        return redirect(url_for('play_game'))
    return 'Error al iniciar el juego', 400

@app.route('/play')
def play_game():
    if game_controller.juego:
        return render_template('play.html', 
                             game=game_controller.juego,
                             current_player=game_controller.juego.currentplayer)
    return redirect(url_for('game'))

@app.route('/place_ship', methods=['POST'])
def place_ship():
    position = request.form['position']
    if game_controller.colocar_barco(position):
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Error al colocar el barco'})

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
            response['winner'] = winner.name
            game_controller.actualizar_juego(game_controller.juego_id, 'finalizado', winner.id)
    
    return jsonify(response)

@app.route('/switch_turn', methods=['POST'])
def switch_turn():
    game_controller.cambiar_turno()
    return jsonify({'success': True})

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

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    
    # Lógica para guardar el jugador en la base de datos
    db_connection (name, email)
    
    # Redirige a la página de inicio o muestra un mensaje de éxito
    return redirect(url_for('index'))  # Redirige a la página de inicio

if __name__ == '__main__':
    app.run(debug=True)
