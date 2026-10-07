#!/usr/bin/env sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
docker info >/dev/null
if [ ! -f .env ]; then
    umask 077
    root_password=$(od -An -N32 -tx1 /dev/urandom | tr -d ' \n')
    app_password=$(od -An -N32 -tx1 /dev/urandom | tr -d ' \n')
    printf 'MYSQL_ROOT_PASSWORD=%s\nMYSQL_PASSWORD=%s\nMYSQL_PUBLIC_PORT=3307\n' "$root_password" "$app_password" > .env
    unset root_password app_password
fi
docker compose config --quiet
docker compose up -d --wait --wait-timeout 240 db
printf 'Workbench: 127.0.0.1, puerto 3307 (o MYSQL_PUBLIC_PORT de .env), usuario personas, base escuela.\nLa contrasena esta en MYSQL_PASSWORD de tu .env local.\n'
docker compose run --build --rm app
