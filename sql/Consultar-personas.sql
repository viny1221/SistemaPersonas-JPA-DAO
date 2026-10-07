-- Ejecuta este archivo en MySQL Workbench despues de preparar escuela.sql
-- o de iniciar la aplicacion Java correctamente.
USE escuela;

SHOW TABLES;

SELECT id, nombre, edad, correo
FROM persona
ORDER BY id;

SELECT COUNT(*) AS total_personas
FROM persona;
