#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m pip install -r requirements.txt
cd server
python manage.py migrate --noinput
python - <<'PY'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dealership.settings")
import django
django.setup()
from django.contrib.auth import get_user_model
User=get_user_model()
u,created=User.objects.get_or_create(username="testuser",defaults={"email":"testuser@example.com"})
u.set_password("DemoOnly_ChangeMe_123!")
u.save()
print("Created/reset temporary local testuser account")
PY
python manage.py runserver 127.0.0.1:8000 > /tmp/dealership-django.log 2>&1 &
pid=$!
trap 'kill "$pid" 2>/dev/null || true' EXIT
for i in $(seq 1 40); do if curl -fsS http://127.0.0.1:8000/ >/dev/null 2>&1; then break; fi; sleep 1; done
command='curl -sS -X POST http://127.0.0.1:8000/djangoapp/login -H "Content-Type: application/json" -d '\''{"userName":"testuser","password":"DemoOnly_ChangeMe_123!"}'\'''
printf '%s\n' "$command" > loginuser
eval "$command" | tee -a loginuser
printf '\n'
echo "Saved command and real response in server/loginuser"
