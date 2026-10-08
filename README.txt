SISTEMA PERSONAS - JAVA + JPA + DAO + H2
======================================

Requisitos: Java 17 y Maven. El primer arranque descarga las dependencias.
En Windows abre "Iniciar SistemaPersonas.cmd".
En VS Code abre la carpeta con pom.xml y ejecuta:
  mvn clean package
  mvn exec:java
En NetBeans abre el proyecto Maven y pulsa F6.

La base integrada H2 se crea automáticamente en datos/sistema_personas.mv.db.
No pide usuario ni contraseña de MySQL. No necesita un servidor de base de datos.
Los registros se conservan al cerrar y quedan excluidos de Git.
No importa ni modifica las bases anteriores de MySQL.
Para mover tus registros, cierra el programa y copia la carpeta datos.

ESTRUCTURA
Persona.java: entidad JPA; @Id y @GeneratedValue definen el identificador.
PersonaDAO.java: interfaz con las operaciones CRUD.
PersonaDAOImpl.java: implementación con EntityManager y transacciones.
JPAUtil.java: abre la base H2 y crea EntityManagerFactory.
persistence.xml: declara Hibernate y la unidad de persistencia.
PruebaPersona.java: menú de consola.

Hibernate convierte las operaciones sobre objetos Java en SQL para H2.
El menú permite listar, agregar, buscar, editar y eliminar personas.
Consulta README.md para los pasos completos.
