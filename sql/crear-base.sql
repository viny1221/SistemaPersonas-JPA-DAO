-- Este script es opcional.
-- Hibernate puede crear automáticamente la base y la tabla con la configuración del proyecto.

CREATE DATABASE IF NOT EXISTS sistema_personas
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE sistema_personas;

CREATE TABLE IF NOT EXISTS persona (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);
