package mx.edu.tesoem.sistemapersonas.dao;

import mx.edu.tesoem.sistemapersonas.modelo.Persona;

import java.util.List;

public interface PersonaDAO {

    void insertar(Persona persona);

    Persona buscarPorId(Integer id);

    List<Persona> seleccionarTodas();

    void actualizar(Persona persona);

    boolean eliminar(Integer id);
}
