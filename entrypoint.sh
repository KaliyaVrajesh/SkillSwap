#!/bin/sh
set -e

echo "=> Waiting for database..."

python - <<'PY'
import os, time, sys
import psycopg2
db_url = os.getenv('DATABASE_URL')
if db_url:
    dsn = db_url
else:
    dsn = "dbname={db} user={user} password={pw} host={host} port={port}".format(
        db=os.getenv('POSTGRES_DB','skillswap_db'),
        user=os.getenv('POSTGRES_USER','skillswap'),
        pw=os.getenv('POSTGRES_PASSWORD','secretpassword'),
        host=os.getenv('POSTGRES_HOST','db'),
        port=os.getenv('POSTGRES_PORT','5432'),
    )
for i in range(60):
    try:
        psycopg2.connect(dsn).close()
        print("Database reachable")
        sys.exit(0)
    except Exception as e:
        print("Waiting for DB... ({}/60)".format(i+1))
        time.sleep(1)
print("Could not connect to DB after waiting")
sys.exit(1)
PY

echo "=> Running DB migrations (flask db upgrade)"
export FLASK_APP=${FLASK_APP:-run.py}
flask db upgrade

echo "=> Starting Gunicorn"
exec gunicorn -w ${GUNICORN_WORKERS:-4} -b 0.0.0.0:${PORT:-5000} run:app
