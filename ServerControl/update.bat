@echo off

for /f "delims=" %%i in ('python -c "import yaml; print(yaml.safe_load(open(r'%~dp0..\config.yml', encoding='utf-8'))['server']['ip'])"') do set IP=%%i
for /f "delims=" %%i in ('python -c "import yaml; print(yaml.safe_load(open(r'%~dp0..\config.yml', encoding='utf-8'))['server']['user'])"') do set SSH_USER=%%i

ssh %SSH_USER%@%IP% "cd ~/apps/Reaminal && git fetch origin && git reset --hard origin/main && (test -d venv || python3 -m venv venv) && ./venv/bin/pip install -r requirements.txt && sudo systemctl restart reaminal"

pause