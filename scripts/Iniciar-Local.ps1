$ErrorActionPreference = 'Stop'
[Console]::InputEncoding = [Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
try {
    if (-not (Get-Command java -ErrorAction SilentlyContinue)) { throw 'Instala JDK 17 y agrega Java al PATH.' }
    if (-not (Get-Command mvn -ErrorAction SilentlyContinue)) { throw 'Instala Maven y agrega mvn al PATH.' }
    & mvn -B -ntp compile dependency:build-classpath '-Dmdep.outputFile=target/classpath.txt'
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo compilar el proyecto.' }
    $dependenciasPersonas = ([IO.File]::ReadAllText((Join-Path $PWD 'target/classpath.txt'))).Trim()
    $classpathPersonas = (Join-Path $PWD 'target/classes') + ';' + $dependenciasPersonas
    & java '-Dfile.encoding=UTF-8' '-cp' $classpathPersonas 'mx.edu.tesoem.sistemapersonas.prueba.PruebaPersona'
    if ($LASTEXITCODE -ne 0) { throw 'El programa termino con error.' }
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
