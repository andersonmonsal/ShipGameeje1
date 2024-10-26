--sql/crear_tablas.sql
CREATE TABLE IF NOT EXISTS jugadores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS juegos (
    id SERIAL PRIMARY KEY,
    jugador1_id INT REFERENCES jugadores(id),
    jugador2_id INT REFERENCES jugadores(id),
    estado VARCHAR(20),
    ganador_id INT REFERENCES jugadores(id)
);

CREATE TABLE IF NOT EXISTS tableros (
    id SERIAL PRIMARY KEY,
    juego_id INT REFERENCES juegos(id),
    jugador_id INT REFERENCES jugadores(id),
    posicion VARCHAR(2),
    barco BOOLEAN DEFAULT FALSE,
    golpe BOOLEAN DEFAULT FALSE
);
