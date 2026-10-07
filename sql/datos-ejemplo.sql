-- Datos de ejemplo para una instalacion nueva del paquete Docker.
SET NAMES utf8mb4;
USE escuela;
INSERT IGNORE INTO persona (nombre, edad, correo) VALUES
    ('Juan', 20, 'juan@gmail.com'),
    ('María', 22, 'maria@gmail.com'),
    ('Pedro', 19, 'pedro@gmail.com');
