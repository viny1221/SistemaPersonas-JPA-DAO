# SistemaPersonas

Programa de consola en Java para **agregar, consultar, editar y eliminar personas**. Al abrirlo por primera vez, crea su propia base **`sistema_personas`** y su tabla en MySQL de esa computadora. Puedes ver los datos en MySQL Workbench.

[**Descargar proyecto ZIP**](https://github.com/viny1221/SistemaPersonas-JPA-DAO/archive/refs/heads/main.zip)

## Requisitos

- Java 17 (JDK).
- MySQL Server encendido y MySQL Workbench.
- Maven, o NetBeans para abrir el proyecto.

Para usar el iniciador de Windows, `java` y `mvn` deben estar disponibles en la terminal. El primer arranque necesita internet para descargar las dependencias.

## Cómo abrirlo

1. Descarga el ZIP y extrae la carpeta.
2. Asegúrate de que MySQL Server esté encendido.
3. En Windows, abre **`Iniciar con MySQL local.cmd`** y escribe el usuario y la contraseña de MySQL de esa computadora.
4. El programa crea la base y la tabla si faltan y muestra el menú. **No necesitas ejecutar archivos SQL antes.**

El usuario de MySQL debe tener permisos para crear la base y sus tablas. La base empieza vacía y los datos que agregues permanecen al cerrar el programa.

**En NetBeans:** abre la carpeta que contiene `pom.xml` y pulsa **F6**.

## Descargar y ejecutar desde la terminal

Con Git, Java, Maven y MySQL instalados:

```bash
git clone https://github.com/viny1221/SistemaPersonas-JPA-DAO.git
cd SistemaPersonas-JPA-DAO
mvn clean package
mvn exec:java
```

## Opciones del menú

| Opción | Acción |
| --- | --- |
| 1 | Mostrar personas |
| 2 | Agregar persona |
| 3 | Buscar por ID |
| 4 | Editar persona |
| 5 | Eliminar persona |
| 0 | Salir |

## Ver la base en Workbench

Conecta a `localhost:3306` con las mismas credenciales, actualiza **Schemas** y abre **`sistema_personas`**. Ejecuta **`sql/Consultar-personas.sql`** para ver los registros.

Si quieres tres personas de ejemplo, ejecuta **`sql/datos-ejemplo.sql`** después del primer arranque. Es opcional y no reemplaza los registros existentes.

**Cada computadora tiene su propia base y sus propias credenciales.** GitHub entrega el código y los scripts; no incluye tus registros ni una contraseña. Descargar el proyecto no lo conecta a tu computadora.

Para usar otro nombre de base o servidor, configura `MYSQL_DATABASE`, `MYSQL_HOST` y `MYSQL_PORT`. Por defecto utiliza `sistema_personas` en `localhost:3306`.
