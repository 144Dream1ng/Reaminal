@echo off

title Reaminal Logs

for /f "delims=" %%i in ('python -c "import yaml; print(yaml.safe_load(open(r'%~dp0config.yml', encoding='utf-8'))['raspberrypi']['ip'])"') do set IP=%%i
for /f "delims=" %%i in ('python -c "import yaml; print(yaml.safe_load(open(r'%~dp0config.yml', encoding='utf-8'))['raspberrypi']['user'])"') do set SSH_USER=%%i

ssh %SSH_USER%@%IP% "journalctl -u reaminal -f"

pause