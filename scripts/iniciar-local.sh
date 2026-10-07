#!/usr/bin/env sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
mvn -B -ntp compile dependency:build-classpath -Dmdep.outputFile=target/classpath.txt
dependencias_personas=$(cat target/classpath.txt)
java -Dfile.encoding=UTF-8 -cp "target/classes:$dependencias_personas" mx.edu.tesoem.sistemapersonas.prueba.PruebaPersona
