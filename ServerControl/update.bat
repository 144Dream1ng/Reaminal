@echo off

for /f "delims=" %%i in ('python -c "import yaml; print(yaml.safe_load(open(r'%~dp0config.yml', encoding='utf-8'))['raspberrypi']['ip'])"') do set IP=%%i
for /f "delims=" %%i in ('python -c "import yaml; print(yaml.safe_load(open(r'%~dp0config.yml', encoding='utf-8'))['raspberrypi']['user'])"') do set SSH_USER=%%i

ssh %SSH_USER%@%IP% "cd ~/apps/Reaminal && git pull && (test -d venv || python3 -m venv venv) && ./venv/bin/pip install -r requirements.txt && sudo systemctl restart reaminal"

pause