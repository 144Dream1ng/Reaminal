@echo off

ssh user@192.168.219.122 "cd ~/apps/Reaminal && git pull && (test -d venv || python3 -m venv venv) && ./venv/bin/pip install -r requirements.txt && sudo systemctl restart reaminal"

pause