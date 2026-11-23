#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
cd server
python manage.py migrate --noinput
python - <<'PY'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dealership.settings")
import django
django.setup()
from django.contrib.auth import get_user_model
u,_=get_user_model().objects.get_or_create(username="testuser")
u.set_password("DemoOnly_ChangeMe_123!")
u.save()
PY
python manage.py runserver 127.0.0.1:8000 > /tmp/dealership-logout.log 2>&1 &
pid=$!
cookie=$(mktemp)
trap 'kill "$pid" 2>/dev/null || true; rm -f "$cookie"' EXIT
for i in $(seq 1 40); do if curl -fsS http://127.0.0.1:8000/ >/dev/null 2>&1; then break; fi; sleep 1; done
curl -fsS -c "$cookie" -X POST http://127.0.0.1:8000/djangoapp/login -H "Content-Type: application/json" -d '{"userName":"testuser","password":"DemoOnly_ChangeMe_123!"}' > /dev/null
printf '%s\n' 'curl -sS -b cookies.txt -X POST http://127.0.0.1:8000/djangoapp/logout' > logoutuser
curl -fsS -b "$cookie" -X POST http://127.0.0.1:8000/djangoapp/logout | tee -a logoutuser
printf '\n'
echo "Saved real logout response in server/logoutuser (cookie file is temporary; displayed command uses illustrative cookies.txt filename)."
