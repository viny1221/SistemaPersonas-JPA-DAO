package mx.edu.tesoem.sistemapersonas.conexion;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;

import java.util.HashMap;
import java.util.Map;

public final class JPAUtil {

    private static EntityManagerFactory emf;

    private JPAUtil() {
    }

    public static synchronized void iniciar(String usuario, String contrasena) {
        if (emf != null && emf.isOpen()) {
            return;
        }

        String url = "jdbc:mysql://" + obtenerHost() + ":" + obtenerPuerto() + "/" + obtenerBase()
                + "?createDatabaseIfNotExist=true"
                + "&useSSL=false"
                + "&allowPublicKeyRetrieval=true"
                + "&serverTimezone=America/Mexico_City"
                + "&characterEncoding=UTF-8";

        Map<String, Object> propiedades = new HashMap<>();
        propiedades.put("jakarta.persistence.jdbc.driver", "com.mysql.cj.jdbc.Driver");
        propiedades.put("jakarta.persistence.jdbc.url", url);
        propiedades.put("jakarta.persistence.jdbc.user", usuario);
        propiedades.put("jakarta.persistence.jdbc.password", contrasena);

        emf = Persistence.createEntityManagerFactory("SistemaPersonasPU", propiedades);
    }

    public static String obtenerHost() {
        return valorEntorno("MYSQL_HOST", "localhost");
    }

    public static int obtenerPuerto() {
        int puerto = Integer.parseInt(valorEntorno("MYSQL_PORT", "3306"));
        if (puerto < 1 || puerto > 65535) {
            throw new IllegalArgumentException("MYSQL_PORT debe estar entre 1 y 65535.");
        }
        return puerto;
    }

    public static String obtenerBase() {
        String base = valorEntorno("MYSQL_DATABASE", "escuela");
        if (!base.matches("[a-zA-Z_][a-zA-Z0-9_]*")) {
            throw new IllegalArgumentException("MYSQL_DATABASE no es un nombre valido.");
        }
        return base;
    }

    private static String valorEntorno(String nombre, String predeterminado) {
        String valor = System.getenv(nombre);
        return valor == null || valor.isBlank() ? predeterminado : valor.trim();
    }

    public static EntityManager getEntityManager() {
        if (emf == null || !emf.isOpen()) {
            throw new IllegalStateException("JPA no ha sido inicializado.");
        }
        return emf.createEntityManager();
    }

    public static synchronized void cerrar() {
        if (emf != null && emf.isOpen()) {
            emf.close();
        }
    }
}
