# SistemaPersonas · Java, JPA, DAO y MySQL

Programa de consola para **listar, agregar, buscar, actualizar y eliminar personas**. Guarda ID, nombre, edad y correo en la base `escuela`, tabla `persona`.

[**Descargar proyecto completo en ZIP**](https://github.com/viny1221/SistemaPersonas-JPA-DAO/archive/refs/heads/main.zip)

## Ejecutar en otra PC

### 1. Preparar la computadora

Instala:

- **JDK 17** para ejecutar y compilar Java.
- **MySQL Server** para guardar los datos. Conserva el usuario y contraseña que configures al instalarlo.
- **MySQL Workbench** para consultar y administrar la base.
- **Maven** para el iniciador de terminal, o **NetBeans** para abrir el proyecto en el IDE.

El iniciador de Windows necesita que `java` y `mvn` estén disponibles en el PATH. Necesitas internet en el primer arranque para descargar las dependencias de Maven.

### 2. Preparar la base en Workbench

Con MySQL Server encendido, crea una conexión **Standard TCP/IP**:

| Campo | Valor |
| --- | --- |
| Connection Name | SistemaPersonas |
| Hostname | `127.0.0.1` |
| Port | `3306` |
| Username | `root` o tu usuario de MySQL |
| Password | La contraseña de ese usuario en esa PC |

Descarga y extrae el ZIP. Dentro de Workbench, abre y ejecuta estos archivos en orden:

1. **`sql/escuela.sql`**: prepara la base y la tabla.
2. **`sql/datos-ejemplo.sql`**, opcional: agrega a Juan, María y Pedro para iniciar con los mismos ejemplos.

Puedes ver los registros ejecutando **`sql/Consultar-personas.sql`**. Workbench administra MySQL; el servidor MySQL debe estar encendido para que funcione la aplicación.

### 3. Abrir el programa

**Windows:** abre **`Iniciar con MySQL local.cmd`** desde la carpeta extraída. El iniciador compila el proyecto y abre el menú. Escribe el usuario y contraseña de MySQL de esa computadora.

**NetBeans:** selecciona **File → Open Project**, abre la carpeta que contiene `pom.xml`, espera la descarga de dependencias y ejecuta con **F6**.

**Linux o macOS:** con Java, Maven y MySQL instalados, ejecuta:

```sh
sh scripts/iniciar-local.sh
```

También puedes usar Maven desde la terminal:

```sh
mvn clean package
mvn exec:java
```

Presiona Enter en usuario para usar `root`. Deja la contraseña vacía solamente si tu usuario de MySQL está configurado sin contraseña.

Los datos quedan guardados al cerrar y volver a abrir el programa. Cada computadora tiene su propia base; los cambios no se sincronizan entre equipos.

## Menú

| Opción | Operación |
| --- | --- |
| 1 | Mostrar todas las personas |
| 2 | Agregar una persona |
| 3 | Buscar por ID |
| 4 | Actualizar una persona |
| 5 | Eliminar una persona |
| 0 | Salir |

## Configurar otra conexión

La conexión predeterminada es `localhost:3306/escuela`. El programa admite variables de entorno:

| Variable | Valor predeterminado |
| --- | --- |
| `MYSQL_HOST` | `localhost` |
| `MYSQL_PORT` | `3306` |
| `MYSQL_DATABASE` | `escuela` |
| `MYSQL_USER` | Se solicita al iniciar |
| `MYSQL_PASSWORD` | Se solicita al iniciar |

No necesitas modificar el código para usar otro puerto o usuario. Las credenciales se toman del entorno del proceso o se introducen al iniciar; no se publican contraseñas locales.

Con permisos suficientes, la conexión puede crear la base y Hibernate crear o actualizar la tabla. Los scripts de Workbench permiten preparar la estructura antes de ejecutar Java.

## Estructura

- `Persona.java`: entidad JPA y correspondencia con la tabla.
- `PersonaDAO.java`: contrato de operaciones.
- `PersonaDAOImpl.java`: consultas y transacciones con `EntityManager`.
- `JPAUtil.java`: conexión configurable y administración de JPA.
- `PruebaPersona.java`: menú y entrada de datos.
- `persistence.xml`: Hibernate, proveedor de JPA.
- `sql/`: estructura, ejemplos y consultas para Workbench.

El menú y las operaciones CRUD del proyecto original se conservan.

## Comprobación

GitHub Actions verifica Java 17 y MySQL instalados directamente en Ubuntu. La prueba comprueba listado, inserción, búsqueda, actualización, eliminación y conservación de datos entre ejecuciones. Utiliza una base temporal exclusiva y la elimina al terminar.

Con Python 3, Java, Maven y el cliente de MySQL disponibles, ejecuta:

```sh
python tests/verificar_mysql_local.py
```

La cuenta configurada mediante `MYSQL_USER` y `MYSQL_PASSWORD` debe poder crear y eliminar la base temporal de prueba.
