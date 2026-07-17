@echo off
REM bmaltais musubi-tuner-gui launcher, pinned to port 7870 (matches Cloudflare tunnel musubi.tjtj.cloud)
set Path=.\uv\windows;%Path%
REM Force UTF-8 so training doesn't crash on CJK log characters (cp949 UnicodeEncodeError on Korean Windows).
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
REM Browse (file dialog) buttons ARE enabled here so they work locally / via Remote Desktop.
REM WARNING: do NOT click Browse from the plain web page (musubi.tjtj.cloud) - it opens a
REM native dialog on THIS PC's desktop and will crash the app if there's no desktop session.
REM Over the web, type paths manually instead. Use Remote Desktop when you need Browse.
cd /d "%~dp0"
uv run gui.py --server_port 7870 %*
pause
