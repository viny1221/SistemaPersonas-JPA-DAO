package mx.edu.tesoem.sistemapersonas.conexion;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

public final class JPAUtil {
    private static EntityManagerFactory emf;

    private JPAUtil() {
    }

    public static synchronized void iniciar() {
        if (emf != null && emf.isOpen()) {
            return;
        }
        Path base = obtenerBase();
        try {
            Files.createDirectories(base.getParent());
        } catch (IOException e) {
            throw new IllegalStateException("No se pudo crear la carpeta de datos: " + base.getParent(), e);
        }
        String url = "jdbc:sqlite:" + base.toString().replace('\\', '/');
        Map<String, Object> propiedades = new HashMap<>();
        propiedades.put("jakarta.persistence.jdbc.driver", "org.sqlite.JDBC");
        propiedades.put("jakarta.persistence.jdbc.url", url);
        propiedades.put("hibernate.dialect", "org.hibernate.community.dialect.SQLiteDialect");
        propiedades.put("hibernate.connection.busy_timeout", "5000");
        propiedades.put("hibernate.connection.foreign_keys", "true");
        emf = Persistence.createEntityManagerFactory("SistemaPersonasPU", propiedades);
    }

    public static Path obtenerBase() {
        String carpeta = System.getenv("PERSONAS_DATA_DIR");
        Path base = Path.of(carpeta == null || carpeta.isBlank() ? "datos" : carpeta)
                .toAbsolutePath().normalize().resolve("sistema_personas.sqlite3");
        if (base.toString().contains("?")) {
            throw new IllegalArgumentException("La carpeta de datos no puede contener signo de interrogacion.");
        }
        return base;
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
