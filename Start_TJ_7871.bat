@echo off
REM TJ Musubi Tuner (custom UI) launcher - port 7871
set Path=.\uv\windows;%Path%
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
uv run gui.py --server_port 7871 %*
pause
