@set R=%~dp0
cd /d %R%

@rem dependency:
@rem python -m pip install websocket-server

:st
@echo %date% %time%
@python svrws.py 19999
@goto st
