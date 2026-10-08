# SistemaPersonas

Programa de consola en Java para **agregar, consultar, editar y eliminar personas**. Guarda los datos en MySQL y permite verlos en MySQL Workbench.

[**Descargar proyecto ZIP**](https://github.com/viny1221/SistemaPersonas-JPA-DAO/archive/refs/heads/main.zip)

## Requisitos

- Java 17 (JDK).
- MySQL Server encendido y MySQL Workbench.
- Maven, o NetBeans para abrir el proyecto.

Para usar el iniciador de Windows, `java` y `mvn` deben estar disponibles en la terminal. El primer arranque necesita internet para descargar las dependencias.

## Cómo abrirlo

1. Descarga el ZIP y extrae la carpeta.
2. En Workbench, conecta a `localhost:3306` con tu usuario y contraseña de MySQL.
3. Abre y ejecuta **`sql/escuela.sql`** para crear la base y la tabla.
4. Si quieres las tres personas de ejemplo, ejecuta también **`sql/datos-ejemplo.sql`**.
5. En Windows, abre **`Iniciar con MySQL local.cmd`** y escribe tus datos de conexión cuando los solicite.

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

Los datos permanecen al cerrar el programa. Para verlos en Workbench, ejecuta **`sql/Consultar-personas.sql`**.

Cada computadora utiliza su propia base `escuela` y sus propias credenciales de MySQL.
