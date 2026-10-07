"""Verifica el menu real contra un MySQL nuevo, aislado de las bases del usuario."""
import json
import os
import re
import secrets
import subprocess
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
proyecto_prueba = "personas-prueba-" + secrets.token_hex(4)
informe = {"proyecto": proyecto_prueba, "pruebas": []}


def verificar(condicion, nombre):
    if not condicion:
        raise AssertionError(nombre)
    informe["pruebas"].append(nombre)
    print("OK:", nombre, flush=True)


def main():
    with tempfile.TemporaryDirectory(prefix="sistemapersonas-prueba-") as temporal:
        archivo_env = Path(temporal) / ".env"
        archivo_env.write_text("MYSQL_ROOT_PASSWORD=" + secrets.token_hex(32) + "\nMYSQL_PASSWORD=" + secrets.token_hex(32) + "\nMYSQL_PUBLIC_PORT=" + os.environ.get("PERSONAS_TEST_PORT", "3317") + "\n", encoding="utf-8")
        comando = ["docker", "compose", "--project-directory", str(RAIZ), "--file", str(RAIZ / "compose.yaml"), "--env-file", str(archivo_env), "--project-name", proyecto_prueba]

        def ejecutar(argumentos, entrada=None, limite=120):
            resultado = subprocess.run(comando + argumentos, input=entrada, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=limite)
            if resultado.returncode:
                raise RuntimeError((resultado.stdout + resultado.stderr)[-6000:])
            return resultado.stdout

        def menu(entrada):
            salida = ejecutar(["run", "--rm", "--no-deps", "-T", "app"], entrada)
            (RAIZ / "target").mkdir(exist_ok=True)
            (RAIZ / "target" / "ultima-ejecucion-portabilidad.txt").write_text(salida, encoding="utf-8")
            verificar("JPA iniciada correctamente" in salida and "No fue posible iniciar" not in salida, "conexion JPA en el contenedor")
            return salida

        def contar():
            salida = ejecutar(["exec", "-T", "db", "sh", "-c", 'MYSQL_PWD="$MYSQL_PASSWORD" mysql --host=127.0.0.1 --user="$MYSQL_USER" --database=escuela --batch --skip-column-names --execute="SELECT COUNT(*) FROM persona"'])
            return int(salida.strip())

        try:
            print("Construyendo con Maven y Java sin el cache local de Windows...", flush=True)
            ejecutar(["build", "app"], limite=900)
            print("Iniciando un MySQL nuevo y separado...", flush=True)
            ejecutar(["up", "-d", "--wait", "--wait-timeout", "240", "db"], limite=600)
            verificar(contar() == 3, "tres personas de ejemplo en la instalacion nueva")
            salida = menu("1\n0\n")
            verificar(all(nombre in salida for nombre in ("Juan", "María", "Pedro")), "listado de las tres personas")
            correo = "prueba-" + secrets.token_hex(5) + "@example.test"
            salida = menu("2\nPersona de prueba\n25\n" + correo + "\n0\n")
            encontrado = re.search(r"Persona guardada con ID:\s*(\d+)", salida)
            verificar(encontrado is not None and contar() == 4, "insercion real de una persona")
            persona_id = encontrado.group(1)
            salida = menu("3\n" + persona_id + "\n0\n")
            verificar(correo in salida and "Persona encontrada" in salida, "busqueda por ID")
            salida = menu("4\n" + persona_id + "\nPersona actualizada\n26\n" + correo + "\n3\n" + persona_id + "\n0\n")
            verificar("Persona actualizada correctamente" in salida and "nombre='Persona actualizada'" in salida and "edad=26" in salida, "actualizacion y nueva consulta")
            ejecutar(["restart", "db"], limite=60)
            ejecutar(["up", "-d", "--wait", "--wait-timeout", "120", "db"], limite=180)
            salida = menu("3\n" + persona_id + "\n0\n")
            verificar("nombre='Persona actualizada'" in salida and contar() == 4, "persistencia tras reiniciar MySQL")
            salida = menu("5\n" + persona_id + "\n3\n" + persona_id + "\n0\n")
            verificar("Persona eliminada correctamente" in salida and "No existe una persona con ID " + persona_id in salida and contar() == 3, "eliminacion y comprobacion en MySQL")
            informe["resultado"] = "aprobado"
        finally:
            ejecutar(["down", "--volumes", "--remove-orphans"], limite=120)
            informe["entorno_temporal_eliminado"] = True
        (RAIZ / "target").mkdir(exist_ok=True)
        (RAIZ / "target" / "portabilidad.json").write_text(json.dumps(informe, indent=2, ensure_ascii=False), encoding="utf-8")
        print("PORTABILIDAD APROBADA. Informe: target/portabilidad.json", flush=True)


if __name__ == "__main__":
    main()
