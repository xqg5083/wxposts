@set R=%~dp0
cd /d %R%

@rem dependency:
@rem python -m pip install websocket-client

@python clt_cli.py 19999

pause