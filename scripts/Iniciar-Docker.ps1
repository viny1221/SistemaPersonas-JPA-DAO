param([switch]$SoloBase)
$ErrorActionPreference = 'Stop'
[Console]::InputEncoding = [Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$raizPersonas = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $raizPersonas
try {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        throw 'Instala Docker Desktop y vuelve a abrir este iniciador.'
    }
    & docker info --format '{{.ServerVersion}}' | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Abre Docker Desktop y espera a que su motor este encendido.' }
    if (-not (Test-Path -LiteralPath '.env')) {
        function NuevaClave {
            $bytesClave = New-Object byte[] 32
            $generadorClave = [Security.Cryptography.RandomNumberGenerator]::Create()
            try { $generadorClave.GetBytes($bytesClave) } finally { $generadorClave.Dispose() }
            return [BitConverter]::ToString($bytesClave).Replace('-', '').ToLowerInvariant()
        }
        $configPersonas = 'MYSQL_ROOT_PASSWORD=' + (NuevaClave) + "`nMYSQL_PASSWORD=" + (NuevaClave) + "`nMYSQL_PUBLIC_PORT=3307`n"
        [IO.File]::WriteAllText((Join-Path $raizPersonas '.env'), $configPersonas, [Text.UTF8Encoding]::new($false))
        $configPersonas = $null
        Write-Host 'Configuracion local creada en .env.'
    }
    & docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { throw 'Revisa los valores del archivo .env.' }
    Write-Host 'Preparando MySQL. La primera vez necesita internet y puede tardar varios minutos.'
    & docker compose up -d --wait --wait-timeout 240 db
    if ($LASTEXITCODE -ne 0) { throw 'MySQL no pudo iniciar. Si el puerto 3307 esta ocupado, cambia MYSQL_PUBLIC_PORT en .env.' }
    Write-Host 'Workbench: host 127.0.0.1, puerto MYSQL_PUBLIC_PORT de .env, usuario personas, base escuela.'
    Write-Host 'La contrasena para Workbench es MYSQL_PASSWORD, en tu archivo local .env.'
    if (-not $SoloBase) {
        & docker compose run --build --rm app
        if ($LASTEXITCODE -ne 0) { throw 'La aplicacion no termino correctamente.' }
    }
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
