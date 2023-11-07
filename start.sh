#!/bin/sh
set -e

if [ -z "$(ls static)" ]; then
  echo "*** Collecting static"
  ./manage.py collectstatic --noinput
fi

# There will be an attempt of DB migration during each start of a container.
echo "*** Running migration"
./manage.py migrate --noinput
echo "*** Migration finished"

exec "$@"