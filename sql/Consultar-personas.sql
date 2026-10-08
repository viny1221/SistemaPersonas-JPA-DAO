-- Ejecuta este archivo en MySQL Workbench despues de iniciar la aplicacion.
USE sistema_personas;

SHOW TABLES;

SELECT id, nombre, edad, correo
FROM persona
ORDER BY id;

SELECT COUNT(*) AS total_personas
FROM persona;
