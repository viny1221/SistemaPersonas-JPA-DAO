package mx.edu.tesoem.sistemapersonas.prueba;

import mx.edu.tesoem.sistemapersonas.conexion.JPAUtil;
import mx.edu.tesoem.sistemapersonas.dao.PersonaDAO;
import mx.edu.tesoem.sistemapersonas.dao.impl.PersonaDAOImpl;
import mx.edu.tesoem.sistemapersonas.modelo.Persona;

import java.util.List;
import java.util.Scanner;

public class PruebaPersona {

    private static final Scanner TECLADO = new Scanner(System.in);
    private static final PersonaDAO PERSONA_DAO = new PersonaDAOImpl();

    public static void main(String[] args) {

        System.out.println("====================================");
        System.out.println(" SISTEMA DE PERSONAS - JPA + DAO");
        System.out.println("====================================");
        System.out.println("Base de datos integrada: SQLite");
        System.out.println("Archivo: " + JPAUtil.obtenerBase());
        System.out.println();

        boolean inicioFallido = false;
        try {

            JPAUtil.iniciar();

            System.out.println("Conexión JPA iniciada correctamente.");
            System.out.println(
                    "La base y la tabla 'persona' se crean automáticamente."
            );
            System.out.println();

            ejecutarMenu();

        } catch (Exception e) {
            inicioFallido = true;
            System.err.println();
            System.err.println("No fue posible iniciar la aplicación.");
            System.err.println(
                    "Detalle: " + obtenerMensajeUtil(e)
            );

            System.err.println();
            System.err.println(
                    "Verifica que la carpeta de datos permita escritura "
                    + "y que no haya otra instancia del programa usando la misma base."
            );

        } finally {

            JPAUtil.cerrar();
        }
        if (inicioFallido) {
            System.exit(1);
        }
    }

    private static void ejecutarMenu() {

        int opcion;

        do {

            mostrarMenu();

            opcion = leerEntero(
                    "Selecciona una opción: "
            );

            System.out.println();

            try {

                switch (opcion) {

                    case 1 -> listarPersonas();

                    case 2 -> agregarPersona();

                    case 3 -> buscarPersona();

                    case 4 -> actualizarPersona();

                    case 5 -> eliminarPersona();

                    case 0 ->
                        System.out.println(
                                "Programa terminado."
                        );

                    default ->
                        System.out.println(
                                "Opción no válida."
                        );
                }

            } catch (Exception e) {

                System.out.println(
                        "Ocurrió un error: "
                        + obtenerMensajeUtil(e)
                );
            }

            System.out.println();

        } while (opcion != 0);
    }

    private static void mostrarMenu() {

        System.out.println(
                "------------- MENÚ -------------"
        );

        System.out.println(
                "1. Mostrar todas las personas"
        );

        System.out.println(
                "2. Agregar persona"
        );

        System.out.println(
                "3. Buscar persona por ID"
        );

        System.out.println(
                "4. Actualizar persona"
        );

        System.out.println(
                "5. Eliminar persona"
        );

        System.out.println(
                "0. Salir"
        );

        System.out.println(
                "--------------------------------"
        );
    }

    private static void listarPersonas() {

        List<Persona> personas =
                PERSONA_DAO.seleccionarTodas();

        if (personas.isEmpty()) {

            System.out.println(
                    "No hay personas registradas."
            );

            return;
        }

        System.out.println(
                "ID | NOMBRE | EDAD | CORREO"
        );

        System.out.println(
                "-----------------------------------------------"
        );

        for (Persona persona : personas) {

            System.out.printf(
                    "%d | %s | %d | %s%n",
                    persona.getId(),
                    persona.getNombre(),
                    persona.getEdad(),
                    persona.getCorreo()
            );
        }
    }

    private static void agregarPersona() {

        System.out.println(
                "--- Agregar persona ---"
        );

        String nombre =
                leerTexto("Nombre: ");

        int edad =
                leerEntero("Edad: ");

        String correo =
                leerTexto("Correo: ");

        Persona persona =
                new Persona(
                        nombre,
                        edad,
                        correo
                );

        PERSONA_DAO.insertar(persona);

        System.out.println(
                "Persona guardada con ID: "
                + persona.getId()
        );
    }

    private static void buscarPersona() {

        int id =
                leerEntero(
                        "ID a buscar: "
                );

        Persona persona =
                PERSONA_DAO.buscarPorId(id);

        if (persona == null) {

            System.out.println(
                    "No existe una persona con ID "
                    + id
                    + "."
            );

        } else {

            System.out.println(
                    "Persona encontrada:"
            );

            System.out.println(
                    persona
            );
        }
    }

    private static void actualizarPersona() {

        int id =
                leerEntero(
                        "ID de la persona a actualizar: "
                );

        Persona persona =
                PERSONA_DAO.buscarPorId(id);

        if (persona == null) {

            System.out.println(
                    "No existe una persona con ID "
                    + id
                    + "."
            );

            return;
        }

        System.out.println(
                "Datos actuales:"
        );

        System.out.println(
                persona
        );

        System.out.println();
        System.out.println(
                "Escribe los nuevos datos."
        );

        String nuevoNombre =
                leerTexto("Nombre: ");

        int nuevaEdad =
                leerEntero("Edad: ");

        String nuevoCorreo =
                leerTexto("Correo: ");

        persona.setNombre(
                nuevoNombre
        );

        persona.setEdad(
                nuevaEdad
        );

        persona.setCorreo(
                nuevoCorreo
        );

        PERSONA_DAO.actualizar(
                persona
        );

        System.out.println(
                "Persona actualizada correctamente."
        );
    }

    private static void eliminarPersona() {

        int id =
                leerEntero(
                        "ID de la persona a eliminar: "
                );

        boolean eliminado =
                PERSONA_DAO.eliminar(id);

        if (eliminado) {

            System.out.println(
                    "Persona eliminada correctamente."
            );

        } else {

            System.out.println(
                    "No existe una persona con ID "
                    + id
                    + "."
            );
        }
    }

    private static String leerTexto(
            String mensaje
    ) {

        while (true) {

            System.out.print(
                    mensaje
            );

            String valor =
                    TECLADO
                            .nextLine()
                            .trim();

            if (!valor.isEmpty()) {

                return valor;
            }

            System.out.println(
                    "El valor no puede estar vacío."
            );
        }
    }

    private static int leerEntero(
            String mensaje
    ) {

        while (true) {

            System.out.print(
                    mensaje
            );

            String texto =
                    TECLADO
                            .nextLine()
                            .trim();

            try {

                return Integer.parseInt(
                        texto
                );

            } catch (NumberFormatException e) {

                System.out.println(
                        "Escribe un número entero válido."
                );
            }
        }
    }

    private static String obtenerMensajeUtil(
            Throwable error
    ) {

        Throwable actual =
                error;

        while (
                actual.getCause() != null
        ) {

            actual =
                    actual.getCause();
        }

        if (
                actual.getMessage() != null
        ) {

            return actual.getMessage();
        }

        return actual
                .getClass()
                .getSimpleName();
    }
}
