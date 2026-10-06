# SistemaPersonas JPA DAO

Aplicación de terminal en **Java 17**, con **Maven**, **JPA/Hibernate**, patrón **DAO** y **MySQL**. Permite listar, agregar, buscar por ID, actualizar y eliminar personas.

## Requisitos

- JDK 17.
- Maven.
- MySQL accesible en `localhost:3306`.
- NetBeans, opcional para abrir y ejecutar el proyecto.

## Ejecutar

Desde la carpeta del proyecto:

```sh
mvn clean verify
mvn exec:java
```

La aplicación solicita el usuario y la contraseña de MySQL al iniciar. También puedes proporcionar `MYSQL_USER` y `MYSQL_PASSWORD` como variables de entorno. No guarda una contraseña en el repositorio. La configuración actual puede crear la base `escuela` y crear o actualizar la tabla `persona` si el usuario tiene permisos. El script `sql/escuela.sql` permite preparar la base manualmente.

### NetBeans

Selecciona **File → Open Project**, abre esta carpeta y espera la sincronización de Maven. Ejecuta el proyecto con **F6**. `nbactions.xml` define la clase principal del menú.

## Menú

| Opción | Operación |
| --- | --- |
| 1 | Listar personas |
| 2 | Agregar una persona |
| 3 | Buscar por ID |
| 4 | Actualizar una persona |
| 5 | Eliminar una persona |
| 0 | Salir |

## Estructura

```text
pom.xml                                Dependencias y compilación Java 17
nbactions.xml                          Ejecución en NetBeans
sql/escuela.sql                        Preparación opcional de MySQL
src/main/java/mx/edu/tesoem/sistemapersonas/
  modelo/Persona.java                  Entidad JPA
  dao/PersonaDAO.java                  Contrato de acceso a datos
  dao/impl/PersonaDAOImpl.java         Operaciones JPA y transacciones
  conexion/JPAUtil.java                Conexión y ciclo de vida de JPA
  prueba/PruebaPersona.java            Menú de terminal
src/main/resources/META-INF/
  persistence.xml                     Unidad SistemaPersonasPU
```

Las consultas y las transacciones están en el DAO. La interfaz de terminal utiliza ese contrato para realizar las operaciones. Hibernate es el proveedor de JPA y utiliza el driver JDBC para comunicarse con MySQL.

El proyecto conserva las operaciones del ZIP original. Se sustituyó la contraseña fija del programa principal por entrada al arrancar o variables de entorno. Se excluyen del repositorio los archivos compilados de `target/`, configuraciones privadas del IDE y credenciales locales. El ZIP original no contiene pruebas automatizadas.
