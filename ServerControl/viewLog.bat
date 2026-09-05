@echo off
title Reaminal Logs
ssh user@192.168.219.122 "journalctl -u reaminal -f"
pause