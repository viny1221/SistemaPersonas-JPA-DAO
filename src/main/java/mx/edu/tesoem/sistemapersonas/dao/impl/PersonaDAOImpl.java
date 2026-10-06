package mx.edu.tesoem.sistemapersonas.dao.impl;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityTransaction;
import mx.edu.tesoem.sistemapersonas.conexion.JPAUtil;
import mx.edu.tesoem.sistemapersonas.dao.PersonaDAO;
import mx.edu.tesoem.sistemapersonas.modelo.Persona;

import java.util.List;

public class PersonaDAOImpl implements PersonaDAO {

    @Override
    public void insertar(Persona persona) {
        EntityManager em = JPAUtil.getEntityManager();
        EntityTransaction tx = em.getTransaction();

        try {
            tx.begin();
            em.persist(persona);
            tx.commit();
        } catch (RuntimeException e) {
            if (tx.isActive()) {
                tx.rollback();
            }
            throw e;
        } finally {
            em.close();
        }
    }

    @Override
    public Persona buscarPorId(Integer id) {
        EntityManager em = JPAUtil.getEntityManager();
        try {
            return em.find(Persona.class, id);
        } finally {
            em.close();
        }
    }

    @Override
    public List<Persona> seleccionarTodas() {
        EntityManager em = JPAUtil.getEntityManager();
        try {
            // JPQL: consulta objetos Persona, no filas directamente.
            return em.createQuery(
                    "SELECT p FROM Persona p ORDER BY p.id",
                    Persona.class
            ).getResultList();
        } finally {
            em.close();
        }
    }

    @Override
    public void actualizar(Persona persona) {
        EntityManager em = JPAUtil.getEntityManager();
        EntityTransaction tx = em.getTransaction();

        try {
            tx.begin();
            em.merge(persona);
            tx.commit();
        } catch (RuntimeException e) {
            if (tx.isActive()) {
                tx.rollback();
            }
            throw e;
        } finally {
            em.close();
        }
    }

    @Override
    public boolean eliminar(Integer id) {
        EntityManager em = JPAUtil.getEntityManager();
        EntityTransaction tx = em.getTransaction();

        try {
            tx.begin();
            Persona persona = em.find(Persona.class, id);

            if (persona == null) {
                tx.rollback();
                return false;
            }

            em.remove(persona);
            tx.commit();
            return true;
        } catch (RuntimeException e) {
            if (tx.isActive()) {
                tx.rollback();
            }
            throw e;
        } finally {
            em.close();
        }
    }
}
