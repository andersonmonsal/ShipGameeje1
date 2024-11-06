import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.controller.db_connection import get_connection
from src.controller.game_controller import GameController
import psycopg2

app = Flask(__name__)
game_controller = GameController()

def conectar_db():
    """Establece y retorna una conexión a la base de datos"""
    try:
        conn = psycopg2.connect(get_connection())
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

@app.route('/')
def index():
    """Ruta principal - Página de inicio"""
    return render_template('index.html')

@app.route('/players')
def players():
    """Ruta para mostrar todos los jugadores"""
    try:
        players = game_controller.obtener_todos_los_jugadores()
        return render_template('player.html', players=players)
    except Exception as e:
        print(f"Error al obtener jugadores: {e}")
        return 'Error al obtener jugadores', 500

@app.route('/register', methods=['POST'])
def register():
    """Ruta unificada para registrar/crear jugadores"""
    try:
        name = request.form['name']
        player = game_controller.crear_jugador(name)
        if player:
            return redirect(url_for('players'))
        return 'Error al registrar el jugador', 400
    except Exception as e:
        print(f"Error en registro: {e}")
        return 'Error en el registro', 500

@app.route('/update_player/<int:player_id>', methods=['POST'])
def update_player(player_id):
    """Ruta para actualizar un jugador"""
    try:
        name = request.form['name']
        if game_controller.actualizar_jugador(player_id, name):
            return redirect(url_for('players'))
        return 'Error al actualizar el jugador', 400
    except Exception as e:
        print(f"Error en actualización: {e}")
        return 'Error en la actualización', 500

@app.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    """Ruta para eliminar un jugador"""
    try:
        if game_controller.eliminar_jugador(player_id):
            return redirect(url_for('players'))
        return 'Error al eliminar el jugador', 400
    except Exception as e:
        print(f"Error en eliminación: {e}")
        return 'Error en la eliminación', 500

@app.route('/game')
def game():
    """Ruta para mostrar la página del juego"""
    try:
        players = game_controller.obtener_todos_los_jugadores()
        return render_template('game.html', players=players)
    except Exception as e:
        print(f"Error al cargar juego: {e}")
        return 'Error al cargar el juego', 500

@app.route('/start_game', methods=['POST'])
def start_game():
    """Ruta para iniciar el juego"""
    try:
        player1_id = int(request.form['player1_id'])
        player2_id = int(request.form['player2_id'])
        
        if game_controller.iniciar_juego(player1_id, player2_id):
            return redirect(url_for('play_game'))
        return 'Error al iniciar el juego', 400
    except Exception as e:
        print(f"Error al iniciar juego: {e}")
        return 'Error al iniciar el juego', 500

@app.route('/play')
def play_game():
    """Ruta para jugar el juego"""
    try:
        if game_controller.juego:
            return render_template('play.html', 
                                game=game_controller.juego,
                                current_player=game_controller.juego.currentplayer)
        return redirect(url_for('game'))
    except Exception as e:
        print(f"Error en el juego: {e}")
        return 'Error en el juego', 500

@app.route('/place_ship', methods=['POST'])
def place_ship():
    """Ruta para colocar un barco"""
    try:
        # Obtiene los datos de la solicitud
        position = int(request.form['position'])
        orientation = request.form.get('orientation', 'horizontal')
        size = int(request.form.get('size', 3))

        # Coloca el barco con los parámetros proporcionados
        if game_controller.colocar_barco(position, orientation, size):
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'No se puede colocar el barco en esa posición'})
    except Exception as e:
        print(f"Error al colocar barco: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/shoot', methods=['POST'])
def shoot():
    """Ruta para realizar un disparo"""
    try:
        position = int(request.form['position'])
        result = game_controller.realizar_disparo(position)
        
        response = {
            'success': True,
            'hit': result,
            'game_over': game_controller.verificar_fin_juego()
        }
        
        if response['game_over']:
            winner = game_controller.obtener_ganador()
            if winner:
                response['winner'] = winner.nombre
                game_controller.actualizar_juego(game_controller.juego_id, 'finalizado', winner.id)
        
        return jsonify(response)
    except Exception as e:
        print(f"Error al realizar disparo: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get_board')
def get_board():
    """Ruta para obtener los tableros del jugador actual"""
    try:
        if game_controller.juego and game_controller.juego.currentplayer:
            board = game_controller.obtener_tablero_jugador()
            board_attack = game_controller.obtener_tablero_ataque()
            return jsonify({
                'board': board,
                'board_attack': board_attack
            })
        return jsonify({'error': 'No hay juego en curso'}), 400
    except Exception as e:
        print(f"Error al obtener tablero: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/switch_turn', methods=['POST'])
def switch_turn():
    """Ruta para cambiar de turno"""
    try:
        game_controller.cambiar_turno()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error al cambiar turno: {e}")
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
