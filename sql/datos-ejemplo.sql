-- Datos de ejemplo opcionales para una instalacion nueva.
SET NAMES utf8mb4;
USE sistema_personas;
INSERT IGNORE INTO persona (nombre, edad, correo) VALUES
    ('Juan', 20, 'juan@gmail.com'),
    ('María', 22, 'maria@gmail.com'),
    ('Pedro', 19, 'pedro@gmail.com');
