@echo off

for /f "delims=" %%i in ('python -c "import yaml; print(yaml.safe_load(open(r'%~dp0..\config.yml', encoding='utf-8'))['server']['ip'])"') do set IP=%%i
for /f "delims=" %%i in ('python -c "import yaml; print(yaml.safe_load(open(r'%~dp0..\config.yml', encoding='utf-8'))['server']['user'])"') do set SSH_USER=%%i

ssh %SSH_USER%@%IP% "sudo poweroff"

pause