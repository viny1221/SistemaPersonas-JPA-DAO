"""Prueba el menu real con Java y MySQL instalados en el equipo."""
import json
import os
import re
import secrets
import shutil
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
base_prueba = 'personas_prueba_' + secrets.token_hex(6)
informe = {'base_temporal': base_prueba, 'pruebas': []}


def verificar(condicion, nombre):
    if not condicion:
        raise AssertionError(nombre)
    informe['pruebas'].append(nombre)
    print('OK:', nombre, flush=True)


def main():
    entorno = os.environ.copy()
    usuario = entorno.get('MYSQL_USER', 'root')
    contrasena = entorno.get('MYSQL_PASSWORD', '')
    host = entorno.get('MYSQL_HOST', '127.0.0.1')
    puerto = entorno.get('MYSQL_PORT', '3306')
    entorno.update(MYSQL_USER=usuario, MYSQL_PASSWORD=contrasena, MYSQL_HOST=host, MYSQL_PORT=puerto, MYSQL_DATABASE=base_prueba)
    entorno_cliente = dict(entorno, MYSQL_PWD=contrasena)
    cliente = os.environ.get('MYSQL_CLIENT') or shutil.which('mysql')
    if not cliente and os.name == 'nt':
        candidatos = sorted((Path(os.environ.get('ProgramFiles', r'C:\Program Files')) / 'MySQL').glob('MySQL Server */bin/mysql.exe'), reverse=True)
        cliente = str(candidatos[0]) if candidatos else None
    maven = shutil.which('mvn')
    java = shutil.which('java')
    if not all((cliente, maven, java)):
        raise RuntimeError('Se necesitan Java, Maven y el cliente mysql para esta prueba.')

    def ejecutar(argumentos, entrada=None, env=entorno, limite=120):
        resultado = subprocess.run(argumentos, cwd=str(RAIZ), env=env, input=entrada, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=limite)
        if resultado.returncode:
            raise RuntimeError((resultado.stdout + resultado.stderr)[-4000:])
        return resultado.stdout

    def sql(consulta):
        return ejecutar([cliente, '--protocol=TCP', '--host=' + host, '--port=' + puerto, '--user=' + usuario, '--default-character-set=utf8mb4', '--connect-timeout=5', '--batch', '--skip-column-names'], consulta, env=entorno_cliente)

    ejecutar([maven, '-B', '-ntp', 'clean', 'package', 'dependency:copy-dependencies', '-DincludeScope=runtime'], limite=600)
    classpath = str(RAIZ / 'target' / 'classes') + os.pathsep + str(RAIZ / 'target' / 'dependency' / '*')
    comando_java = [java, '-Dfile.encoding=UTF-8', '-cp', classpath, 'mx.edu.tesoem.sistemapersonas.prueba.PruebaPersona']

    def menu(entrada):
        salida = ejecutar(comando_java, entrada)
        (RAIZ / 'target' / 'ultima-ejecucion-mysql-local.txt').write_text(salida, encoding='utf-8')
        verificar('JPA iniciada correctamente' in salida and 'No fue posible iniciar' not in salida, 'conexion JPA con MySQL local')
        return salida

    def contar():
        return int(sql('SELECT COUNT(*) FROM `' + base_prueba + '`.persona;').strip())

    try:
        salida = menu('1\n0\n')
        verificar(contar() == 0 and 'No hay personas registradas.' in salida,
                  'primer arranque crea su propia base y tabla sin ejecutar SQL')
        esquema = (RAIZ / 'sql' / 'crear-base.sql').read_text(encoding='utf-8-sig')
        ejemplos = (RAIZ / 'sql' / 'datos-ejemplo.sql').read_text(encoding='utf-8-sig')
        sql(re.sub(r'\bsistema_personas\b', base_prueba, esquema + '\n' + ejemplos))
        verificar(contar() == 3, 'tres personas de ejemplo en una base nueva')
        salida = menu('1\n0\n')
        verificar(all(nombre in salida for nombre in ('Juan', 'María', 'Pedro')), 'listado y acentos correctos')
        correo = 'prueba-' + secrets.token_hex(5) + '@example.test'
        salida = menu('2\nPersona de prueba\n25\n' + correo + '\n0\n')
        encontrado = re.search(r'Persona guardada con ID:\s*(\d+)', salida)
        verificar(encontrado is not None and contar() == 4, 'insercion real')
        persona_id = encontrado.group(1)
        salida = menu('3\n' + persona_id + '\n0\n')
        verificar(correo in salida and 'Persona encontrada' in salida, 'busqueda por ID')
        salida = menu('4\n' + persona_id + '\nPersona actualizada\n26\n' + correo + '\n0\n')
        verificar('Persona actualizada correctamente' in salida, 'actualizacion')
        salida = menu('3\n' + persona_id + '\n0\n')
        verificar("nombre='Persona actualizada'" in salida and 'edad=26' in salida and contar() == 4, 'datos conservados al volver a abrir Java')
        salida = menu('5\n' + persona_id + '\n3\n' + persona_id + '\n0\n')
        verificar('Persona eliminada correctamente' in salida and 'No existe una persona con ID ' + persona_id in salida and contar() == 3, 'eliminacion comprobada')
        informe['resultado'] = 'aprobado'
    finally:
        # Solo elimina el nombre aleatorio creado por esta prueba.
        if not re.fullmatch(r'personas_prueba_[0-9a-f]{12}', base_prueba):
            raise RuntimeError('Nombre de base temporal inesperado; se cancelo la limpieza.')
        sql('DROP DATABASE IF EXISTS `' + base_prueba + '`;')
        informe['base_temporal_eliminada'] = True
    (RAIZ / 'target' / 'verificacion-mysql-local.json').write_text(json.dumps(informe, indent=2, ensure_ascii=False), encoding='utf-8')
    print('JAVA Y MYSQL LOCAL VERIFICADOS.', flush=True)


if __name__ == '__main__':
    main()
