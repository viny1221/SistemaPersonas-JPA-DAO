"""Ejecuta el menú real contra archivos SQLite nuevos, sin servidor ni credenciales."""
import json
import os
import re
import shutil
import sqlite3
import subprocess
import tempfile
from contextlib import closing
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
informe = {"motor": "SQLite persistente", "pruebas": []}


def verificar(condicion, nombre):
    if not condicion:
        raise AssertionError(nombre)
    informe["pruebas"].append(nombre)
    print("OK:", nombre, flush=True)


def main():
    maven = shutil.which("mvn")
    java = shutil.which("java")
    if not maven or not java:
        raise RuntimeError("Se necesitan Java 17 y Maven para esta prueba.")
    entorno = os.environ.copy()
    entorno.pop("PERSONAS_DATA_DIR", None)
    # Una configuración MySQL incorrecta no debe afectar a esta versión.
    entorno.update(MYSQL_HOST="servidor-inexistente.invalid", MYSQL_PORT="1",
                   MYSQL_USER="usuario_incorrecto", MYSQL_PASSWORD="incorrecta")
    compilacion = subprocess.run(
        [maven, "-B", "-ntp", "clean", "package", "dependency:copy-dependencies",
         "-DincludeScope=runtime"], cwd=RAIZ, env=entorno, capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=600)
    (RAIZ / "target" / "compilacion-base-integrada.txt").write_text(
        compilacion.stdout + compilacion.stderr, encoding="utf-8")
    verificar(compilacion.returncode == 0, "compilacion con Java 17")
    verificar(not list((RAIZ / "target" / "dependency").glob("mysql*"))
              and not list((RAIZ / "target" / "dependency").glob("h2-*")),
              "dependencias sin driver MySQL ni H2")
    classpath = str(RAIZ / "target" / "classes") + os.pathsep + str(RAIZ / "target" / "dependency" / "*")
    comando = [java, "-Dfile.encoding=UTF-8", "-cp", classpath,
               "mx.edu.tesoem.sistemapersonas.prueba.PruebaPersona"]

    with tempfile.TemporaryDirectory(prefix="personas-sqlite-", dir=RAIZ / "target") as temporal:
        carpeta = Path(temporal) / "PC con espacios y acentos á"
        carpeta.mkdir()

        def menu(entrada, cwd=carpeta, env=entorno):
            resultado = subprocess.run(comando, cwd=cwd, env=env, input=entrada,
                                       capture_output=True, text=True, encoding="utf-8",
                                       errors="replace", timeout=90)
            (RAIZ / "target" / "ultima-ejecucion-base-integrada.txt").write_text(
                resultado.stdout + resultado.stderr, encoding="utf-8")
            verificar(resultado.returncode == 0 and "JPA iniciada correctamente" in resultado.stdout,
                      "inicio sin usuario ni contrasena MySQL")
            return resultado.stdout

        archivo = carpeta / "datos" / "sistema_personas.sqlite3"
        salida = menu("1\n0\n")
        verificar(archivo.is_file() and "No hay personas registradas." in salida,
                  "primer arranque crea base y tabla vacias en la ruta predeterminada")
        with closing(sqlite3.connect(archivo)) as conexion:
            verificar(conexion.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
                      and conexion.execute("SELECT count(*) FROM persona").fetchone()[0] == 0,
                      "archivo SQLite valido y tabla consultable desde otra herramienta")
        salida = menu("2\nMaría López\n28\nmaria@example.test\n0\n")
        encontrado = re.search(r"Persona guardada con ID:\s*(\d+)", salida)
        verificar(encontrado is not None, "insercion real con acentos")
        persona_id = encontrado.group(1)
        salida = menu("1\n3\n" + persona_id + "\n0\n")
        verificar("María López" in salida and "Persona encontrada" in salida,
                  "listado y busqueda en otro proceso Java")
        salida = menu("4\n" + persona_id + "\nMaría Actualizada\n29\nmaria@example.test\n0\n")
        verificar("Persona actualizada correctamente" in salida, "edicion real")
        salida = menu("3\n" + persona_id + "\n0\n")
        verificar("nombre='María Actualizada'" in salida and "edad=29" in salida,
                  "persistencia de la edicion tras cerrar y abrir")
        with closing(sqlite3.connect(archivo)) as conexion:
            verificar(conexion.execute("SELECT id, nombre, edad FROM persona").fetchall()
                      == [(int(persona_id), "María Actualizada", 29)],
                      "ID y datos reales comprobados directamente en SQLite")
        salida = menu("2\nOtro registro\n20\nmaria@example.test\n1\n0\n")
        verificar("Ocurrió un error:" in salida and "María Actualizada" in salida
                  and "Persona guardada con ID:" not in salida,
                  "correo duplicado revierte la transaccion y conserva el menu")
        salida = menu("abc\n99\n3\n999999\n0\n")
        verificar("Escribe un número entero válido." in salida and "Opción no válida." in salida
                  and "No existe una persona con ID 999999" in salida,
                  "opciones invalidas e ID inexistente")

        # Copia del archivo cerrado a otra ubicación: conserva datos y funciona sin servidor.
        otra_pc = Path(temporal) / "otra-pc"
        otra_pc.mkdir()
        salida = menu("1\n0\n", cwd=otra_pc)
        verificar("No hay personas registradas." in salida, "otra copia tiene su propia base vacia")
        shutil.copy2(archivo, otra_pc / "datos" / archivo.name)
        salida = menu("3\n" + persona_id + "\n0\n", cwd=otra_pc)
        verificar("María Actualizada" in salida, "traslado del archivo cerrado conserva registros")

        personalizada = Path(temporal) / "ubicacion personalizada"
        env_personalizado = dict(entorno, PERSONAS_DATA_DIR=str(personalizada))
        menu("0\n", env=env_personalizado)
        verificar((personalizada / archivo.name).is_file(), "carpeta de datos configurable")

        salida = menu("5\n" + persona_id + "\n0\n")
        verificar("Persona eliminada correctamente" in salida, "eliminacion real")
        salida = menu("1\n3\n" + persona_id + "\n0\n")
        verificar("No hay personas registradas." in salida and "No existe una persona con ID" in salida,
                  "eliminacion persistente al volver a abrir")
        archivo_obstaculo = Path(temporal) / "no-es-carpeta"
        archivo_obstaculo.write_text("archivo de prueba", encoding="utf-8")
        error = subprocess.run(comando, cwd=carpeta,
                               env=dict(entorno, PERSONAS_DATA_DIR=str(archivo_obstaculo)),
                               input="0\n", capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=90)
        verificar(error.returncode != 0 and "No fue posible iniciar" in error.stderr,
                  "fallo de almacenamiento devuelve error explicito")
    informe["resultado"] = "aprobado"
    (RAIZ / "target" / "verificacion-base-integrada.json").write_text(
        json.dumps(informe, indent=2, ensure_ascii=False), encoding="utf-8")
    print("BASE INTEGRADA Y CRUD VERIFICADOS.", flush=True)


if __name__ == "__main__":
    main()
