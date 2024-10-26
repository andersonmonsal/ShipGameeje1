#src/view/main.py
import sys
sys.path.append("src")

from controller.game_controller import GameController

def imprimir_tablero(matrix):
    letras = "ABCDE"
    print("  " + " ".join(letras))
    for idx, row in enumerate(matrix):
        fila = []
        for cell in row:
            if cell == 0:
                fila.append(".")
            elif cell == 1:
                fila.append("B")  # Barco
            elif cell == 2:
                fila.append("X")  # Barco golpeado
            elif cell == -1:
                fila.append("A")  # Agua
        print(f"{idx + 1} " + " ".join(fila))

def imprimir_tablero_oculto(matrix):
    letras = "ABCDE"
    print("  " + " ".join(letras))
    for idx, row in enumerate(matrix):
        fila = []
        for cell in row:
            if cell == 2:
                fila.append("X")  # Barco golpeado
            elif cell == -1:
                fila.append("A")  # Agua
            else:
                fila.append(".")
        print(f"{idx + 1} " + " ".join(fila))

def mostrar_menu():
    print("\n--- Menú Principal ---")
    print("1. Crear Jugador")
    print("2. Ver Jugadores")
    print("3. Actualizar Jugador")
    print("4. Eliminar Jugador")
    print("5. Iniciar Juego")
    print("6. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion

def main():
    controller = GameController()
    while True:
        opcion = mostrar_menu()
        if opcion == '1':
            # aqui se crea el  jugador
            nombre = input("Ingrese el nombre del jugador: ")
            jugador = controller.crear_jugador(nombre)
            if jugador:
                print(f"Jugador '{jugador.nombre}' creado con ID {jugador.id}")
            else:
                print("Error al crear el jugador.")
        elif opcion == '2':
            # para ver jugadores
            jugadores = controller.obtener_todos_los_jugadores()
            if jugadores:
                print("\nLista de Jugadores:")
                for jugador in jugadores:
                    print(f"ID: {jugador.id}, Nombre: {jugador.nombre}")
            else:
                print("No hay jugadores registrados.")
        elif opcion == '3':
            # para actualizar jugador
            try:
                jugador_id = int(input("Ingrese el ID del jugador a actualizar: "))
                nuevo_nombre = input("Ingrese el nuevo nombre del jugador: ")
                resultado = controller.actualizar_jugador(jugador_id, nuevo_nombre)
                if resultado:
                    print("Jugador actualizado exitosamente.")
                else:
                    print("Error al actualizar el jugador.")
            except ValueError:
                print("ID inválido. Debe ser un número entero.")
        elif opcion == '4':
            #  para eliminar jugador
            try:
                jugador_id = int(input("Ingrese el ID del jugador a eliminar: "))
                resultado = controller.eliminar_jugador(jugador_id)
                if resultado:
                    print("Jugador eliminado exitosamente.")
                else:
                    print("Error al eliminar el jugador.")
            except ValueError:
                print("ID inválido. Debe ser un número entero.")
        elif opcion == '5':
            #  para iniciar el juego
            try:
                jugador1_id = int(input("Ingrese el ID del jugador 1: "))
                jugador2_id = int(input("Ingrese el ID del jugador 2: "))
                if controller.iniciar_juego(jugador1_id, jugador2_id):
                    # Colocación de barcos
                    for _ in range(2):
                        print(f"\nJugador {controller.juego.currentplayer.name}, coloca tus barcos.")
                        for _ in range(3):  # Cada jugador coloca 3 barcos
                            imprimir_tablero(controller.juego.currentplayer.board)
                            position = input("Ingrese una posición para su barco (ej. A1): ")
                            if controller.colocar_barco(position):
                                print("¡Barco colocado!")
                            else:
                                print("Error al colocar el barco. Intente nuevamente.")
                        controller.cambiar_turno()

                    # Inicio del juego
                    while not controller.verificar_fin_juego():
                        print(f"\nTurno del jugador {controller.juego.currentplayer.name}")
                        imprimir_tablero_oculto(controller.juego.currentplayer.board_attack)
                        position = input("Ingrese una posición para atacar (ej. A1): ")
                        if controller.realizar_disparo(position):
                            print("¡Has acertado un barco!")
                        else:
                            print("Has fallado.")
                        if controller.verificar_fin_juego():
                            break
                        controller.cambiar_turno()

                    # Fin del juego
                    ganador = controller.obtener_ganador()
                    if ganador:
                        print(f"\n¡El jugador {ganador.name} ha ganado el juego!")
                else:
                    print("No se pudo iniciar el juego.")
            except ValueError:
                print("ID inválido. Debe ser un número entero.")
        elif opcion == '6':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()

