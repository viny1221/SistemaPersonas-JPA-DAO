# SistemaPersonas · Java, JPA, DAO y MySQL

Programa de consola para **listar, agregar, buscar, actualizar y eliminar personas**. Guarda ID, nombre, edad y correo en `escuela.persona`. MySQL Workbench permite administrar esa misma base.

## Descargar y ejecutar en otra PC

[**Descargar proyecto completo en ZIP**](https://github.com/viny1221/SistemaPersonas-JPA-DAO/archive/refs/heads/main.zip)

### Windows

1. Instala y abre [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/). Espera a que el motor esté encendido.
2. Descarga el ZIP y **extrae toda la carpeta**.
3. Abre **`Iniciar con Docker.cmd`**.
4. Espera la preparación inicial. Aparecerá el menú en la terminal.

El iniciador prepara Java 17, compila el programa e inicia MySQL 8.4. **Para este modo no necesitas instalar Java, Maven ni MySQL por separado.** Necesitas internet en el primer arranque y una computadora compatible con Docker Desktop.

Una instalación nueva empieza con Juan, María y Pedro como datos de ejemplo. Cada equipo tiene su propia base: los cambios de una PC no se sincronizan con las otras.

### Linux o macOS

Con Docker y Docker Compose instalados, ejecuta desde la carpeta extraída:

```sh
sh scripts/iniciar-docker.sh
```

### Volver a abrir o detener

Usa el mismo iniciador para abrir el menú otra vez. También puedes ejecutar:

```sh
docker compose run --rm app
```

Para detener la base y conservar los datos:

```sh
docker compose stop db
```

Los datos se guardan en un volumen de Docker. Conserva también `.env`: contiene las contraseñas propias de esa instalación. Cambiar una contraseña en `.env` no cambia la de una base ya creada.

## Ver la base en MySQL Workbench

Workbench es opcional para ejecutar el menú. Crea una conexión **Standard TCP/IP**:

| Campo | Valor |
| --- | --- |
| Connection Name | SistemaPersonas |
| Hostname | `127.0.0.1` |
| Port | `3307` |
| Username | `personas` |
| Password | Valor de `MYSQL_PASSWORD` en tu `.env` local |
| Default Schema | `escuela` |

Abre la conexión y ejecuta `sql/Consultar-personas.sql`. El puerto está limitado a la propia computadora.

Si `3307` está ocupado, cambia `MYSQL_PUBLIC_PORT` en `.env`, ejecuta de nuevo el iniciador y usa ese puerto en Workbench.

## MySQL local o NetBeans

Este modo requiere **JDK 17, Maven y un servidor MySQL local encendido**.

En Windows abre **`Iniciar con MySQL local.cmd`**. El programa solicita usuario y contraseña. Presiona Enter en usuario para usar `root`; deja la contraseña vacía solamente si ese usuario está configurado sin contraseña.

En NetBeans: **File → Open Project**, selecciona la carpeta, espera las dependencias y ejecuta con **F6**.

Desde la terminal:

```sh
mvn clean package
mvn exec:java
```

La conexión predeterminada es `localhost:3306/escuela`. Se puede configurar con variables de entorno:

| Variable | Valor predeterminado |
| --- | --- |
| `MYSQL_HOST` | `localhost` |
| `MYSQL_PORT` | `3306` |
| `MYSQL_DATABASE` | `escuela` |
| `MYSQL_USER` | Se solicita al iniciar |
| `MYSQL_PASSWORD` | Se solicita al iniciar |

Docker Compose utiliza `.env`. Java local utiliza las variables del proceso o las credenciales que escribas al iniciar.

Con permisos suficientes, la conexión crea la base y Hibernate crea o actualiza la tabla. Puedes prepararla en Workbench con `sql/escuela.sql`. El archivo `sql/datos-ejemplo.sql` es opcional para MySQL local.

## Menú

| Opción | Operación |
| --- | --- |
| 1 | Mostrar todas las personas |
| 2 | Agregar una persona |
| 3 | Buscar por ID |
| 4 | Actualizar una persona |
| 5 | Eliminar una persona |
| 0 | Salir |

## Estructura

- `Persona.java`: entidad JPA y correspondencia con la tabla.
- `PersonaDAO.java`: contrato de operaciones.
- `PersonaDAOImpl.java`: consultas y transacciones con `EntityManager`.
- `JPAUtil.java`: conexión configurable y administración de JPA.
- `PruebaPersona.java`: menú y entrada de datos.
- `persistence.xml`: Hibernate, proveedor de JPA.
- `compose.yaml` y `Dockerfile`: ejecución del programa y MySQL en otra computadora.

El menú y las operaciones CRUD del proyecto original se conservan. Las contraseñas locales no se publican: cada instalación Docker genera las suyas.

## Validación

La prueba construye el programa desde cero, inicia una base nueva y verifica listado, inserción, búsqueda, actualización, eliminación y persistencia tras reiniciar MySQL. Utiliza un volumen y contenedores temporales exclusivos.

Con Python 3 y Docker:

```sh
python tests/verificar_portabilidad.py
```

GitHub Actions ejecuta la misma comprobación en Ubuntu.
