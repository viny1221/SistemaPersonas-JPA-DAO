SISTEMA PERSONAS - JAVA + JPA + DAO + MYSQL + TERMINAL
======================================================

REQUISITOS QUE CUMPLE
---------------------
1. Java: Sí. Proyecto Maven con Java 17.
2. Aplicación de terminal: Sí. Tiene un menú CRUD ejecutado desde main().
3. Capa de datos: Sí. La persistencia está separada del programa principal.
4. DAO: Sí. PersonaDAO define las operaciones y PersonaDAOImpl las implementa.
5. JPA: Sí. Se usa jakarta.persistence y EntityManager.
6. Hibernate: Sí. Hibernate es el proveedor/implementación de JPA.
7. MySQL: Sí. Usa MySQL Connector/J.

ESTRUCTURA IMPORTANTE
---------------------
src/main/java/
  mx.edu.tesoem.sistemapersonas/
    modelo/Persona.java             -> Entidad JPA (@Entity)
    dao/PersonaDAO.java             -> Interfaz DAO
    dao/impl/PersonaDAOImpl.java    -> DAO usando EntityManager
    conexion/JPAUtil.java           -> Crea EntityManagerFactory
    prueba/PruebaPersona.java       -> Aplicación de terminal

src/main/resources/
  META-INF/persistence.xml          -> Configuración de JPA/Hibernate

CÓMO EJECUTAR EN NETBEANS
-------------------------
Para descargar y ejecutar en otra PC, sigue README.md.
En Windows: instala Java 17, Maven y MySQL Server; extrae el ZIP y abre "Iniciar con MySQL local.cmd".
Workbench se conecta al servidor local en 127.0.0.1:3306.

1. Asegúrate de que MySQL esté encendido en localhost:3306.
2. Abre NetBeans.
3. File > Open Project y selecciona esta carpeta.
4. Espera a que Maven descargue las dependencias.
5. Ejecuta el proyecto.
6. La terminal pedirá:
     Usuario de MySQL [root]:
     Contraseña de MySQL:
7. Si tu usuario es root, solo presiona Enter en usuario.
8. Escribe la contraseña de MySQL. Si root no tiene contraseña, presiona Enter.

IMPORTANTE
----------
La URL usa:
  createDatabaseIfNotExist=true

Por eso, si el usuario de MySQL tiene permisos, se crea automáticamente la base:
  escuela

y Hibernate crea/actualiza la tabla:
  persona

Si tu usuario root no tiene permiso para crear bases, ejecuta primero:
  sql/escuela.sql

desde MySQL Workbench.

QUÉ EXPLICAR AL PROFESOR
------------------------
- Persona.java es una entidad JPA porque tiene @Entity.
- @Id indica la llave primaria.
- @GeneratedValue hace que MySQL genere el ID.
- PersonaDAO define las operaciones CRUD sin decir cómo se guardan los datos.
- PersonaDAOImpl implementa el DAO usando EntityManager de JPA.
- JPAUtil crea el EntityManagerFactory y administra la conexión de persistencia.
- persistence.xml declara la unidad de persistencia y a Hibernate como proveedor.
- PruebaPersona.java es la interfaz de terminal.
- Hibernate convierte las operaciones de objetos Java en instrucciones SQL para MySQL.

CRUD DEL MENÚ
-------------
1. SELECT / listar
2. INSERT / agregar
3. SELECT por ID
4. UPDATE / actualizar
5. DELETE / eliminar
0. Salir
