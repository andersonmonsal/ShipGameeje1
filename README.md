## Autores Anteriores 
AUTOR1: Yonatan Calimeño
AUTOR2: Santiago

## Autores recientes 
Tomas Lopez
Anderson Monsalve 

# NAVAL WARFAME GAME

Este proyecto es un sistema de batallas navales multijugador con manejo de jugadores, tableros y lógica de juego. La aplicación permite crear jugadores, iniciar juegos entre ellos y realizar las acciones típicas del juego de batallas navales, como posicionar barcos y disparar a las posiciones del tablero enemigo.

## Requisitos
Python 3.6 o superior, en este casp nososotros usamos anancoda
PostgreSQL (para gestionar la base de datos)

## Estructura del proyecto


proyecto/
├── src/
│   ├── model/
│   │   ├── naval_warfare.py
│   │   └── player_model.py
│   ├── controller/
│   │   ├── game_controller.py
│   │   └── db_connection.py
│   └── view/
│       └── main.py
├── test/
│   └── test_player.py
├── sql/
│   └── crear_tablas.sql
├── config.py
└── README.md
## Descripción de Carpetas y Archivos
src/: Contiene el código fuente de la aplicación.

model/: Define las clases y la lógica del dominio del problema.

naval_warfare.py: Implementa las clases Player y NavalWarfare, que contienen la lógica del juego.

player_model.py: Define la clase Jugador, representando a un jugador en el juego.

controller/: Maneja la lógica de negocio y la comunicación con la base de datos.

game_controller.py: Implementa la clase GameController, que sirve como intermediario entre la vista y el modelo, y maneja las operaciones de base de datos.

db_connection.py: Proporciona la función get_connection() para conectarse a la base de datos.
view/: Maneja la interacción con el usuario.

main.py: Es el punto de entrada de la aplicación y contiene la interfaz de línea de comandos.
test/: Contiene las pruebas unitarias.

test_player.py: Pruebas para las funcionalidades relacionadas con los jugadores.
sql/:
crear_tablas.sql: Script SQL para crear las tablas necesarias en la base de datos.
config.py: Archivo de configuración que contiene las credenciales y parámetros para la conexión a la base de datos.

## Instalación de dependencias
Instalar las librerías necesarias:


                               pip install psycopg2
## web
para que el proyecto web te pueda funcionar lo que debes hacer es instalar la siguiente extención 

                               pip install Flask
 


## Base de datos
El proyecto utiliza PostgreSQL como base de datos. El esquema de la base de datos incluye las siguientes tablas:

jugadores: Almacena la información básica de los jugadores.
juegos: Gestiona las partidas entre dos jugadores.
tableros: Representa el estado de cada tablero de un jugador en un juego.


## Ejecución
Ejecutar el Programa

Navega al directorio del proyecto:
cd ruta/al/directorio/proyecto
ejemplo: En mi caso: Cd Users\yonatan\Desktop\lenguaje dos\ShipGameeje1
una vez en la ruta del archivo debes usar el siguiente comando: 


                                     python src/view/main.py




## Pruebas
El proyecto incluye un conjunto de pruebas unitarias para verificar la funcionalidad del modelo de jugadores.

Para ejecutar las pruebas, corre el siguiente comando:
noata: Debes estar ubicado en el lugar donde descargaste el programa y depues ejecutar el siguiente codigo


                                     python test/test_player.py


## web
En la caroeta templates encuestras todo lo del html
para ejecutar este archivo debes entrar a el archivo "" app.py "" y aca podras ejecutar esto para que se de el funcionamiento web donde este te brindara una url donde podras ejecutar la web

                                   



