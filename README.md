# SistemaPersonas

Programa de consola en Java para **agregar, consultar, editar y eliminar personas**, con JPA, Hibernate y DAO.

Incluye una base **SQLite integrada**: no necesitas instalar MySQL, configurar contraseñas ni ejecutar SQL. Cada copia guarda sus datos en un archivo local y los conserva al cerrar.

[**Descargar proyecto ZIP**](https://github.com/viny1221/SistemaPersonas-JPA-DAO/archive/refs/heads/main.zip)

## Requisitos

- Java 17 (JDK).
- Maven.

`java` y `mvn` deben estar disponibles en la terminal. El primer arranque necesita internet para descargar las dependencias.

## Cómo abrirlo

1. Descarga el ZIP y extrae la carpeta.
2. En Windows, abre **`Iniciar SistemaPersonas.cmd`**.
3. Aparece el menú; la base y la tabla se crean automáticamente, inicialmente vacías.

**En VS Code:** abre la carpeta que contiene `pom.xml` y ejecuta en su terminal:

```bash
mvn clean package
mvn exec:java
```

**En NetBeans:** abre el proyecto Maven y pulsa **F6**.

## Descargar desde la terminal

Con Git instalado:

```bash
git clone https://github.com/viny1221/SistemaPersonas-JPA-DAO.git
cd SistemaPersonas-JPA-DAO
mvn clean package
mvn exec:java
```

Si ya lo clonaste y no tienes cambios locales, cierra el programa y ejecuta `git pull --ff-only` para actualizarlo.

En Linux o macOS también puedes ejecutar `sh scripts/iniciar-local.sh`.

## Menú

| Opción | Acción |
| --- | --- |
| 1 | Mostrar personas |
| 2 | Agregar persona |
| 3 | Buscar por ID |
| 4 | Editar persona |
| 5 | Eliminar persona |
| 0 | Salir |

## Dónde quedan los datos

En **`datos/sistema_personas.sqlite3`**, relativo a la carpeta desde la que ejecutas el programa. Los iniciadores utilizan siempre la carpeta del proyecto. La ruta completa aparece al iniciar. Para elegir otra carpeta, configura `PERSONAS_DATA_DIR`.

La base comienza vacía. Los datos anteriores de MySQL y H2 permanecen en sus bases y no se importan automáticamente. Esta versión utiliza SQLite; Workbench administra MySQL y no abre este archivo.

Los archivos de datos están excluidos de Git. GitHub distribuye el código, no tus registros. Para trasladar tus datos a otra PC, cierra el programa y copia también la carpeta `datos`. Abre una sola instancia a la vez sobre la misma base.
