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

        String url = "jdbc:mysql://localhost:3306/escuela"
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
