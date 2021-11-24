@set R=%~dp0
cd /d %R%

:st
set FLASK_APP=svr_web_tiny.py
python -m flask run -h 0.0.0.0 -p 8888 --with-threads
goto st
