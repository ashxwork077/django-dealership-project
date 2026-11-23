#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../server"
python manage.py runserver 127.0.0.1:8000 > /tmp/dealership-state.log 2>&1 &
pid=$!
trap 'kill "$pid" 2>/dev/null || true' EXIT
for i in $(seq 1 40); do if curl -fsS http://127.0.0.1:8000/ >/dev/null 2>&1; then break; fi; sleep 1; done
printf '%s\n' 'curl -sS http://127.0.0.1:8000/djangoapp/get_dealers/Kansas' > getdealersbyState
curl -fsS http://127.0.0.1:8000/djangoapp/get_dealers/Kansas | tee -a getdealersbyState
printf '\n'
echo "Saved command and actual response in server/getdealersbyState"
