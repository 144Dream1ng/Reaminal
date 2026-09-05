@echo off

ssh user@192.168.219.122 "cd ~/apps/Reaminal && git pull && sudo systemctl restart reaminal"

pause