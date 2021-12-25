#-*- coding: utf-8 -*-
from time import time as now, sleep
def tryx(l,e=print):
	try: return l()
	except Exception as ex: return ex if True==e else e(ex) if e else None
import json
class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj): return tryx(lambda:json.JSONEncoder.default(self,obj),str)
s2o = lambda s:tryx(lambda:json.loads(s))
o2s = lambda o,indent=None:tryx(lambda:json.dumps(o, indent=indent, ensure_ascii=False, cls=MyJsonEncoder))

#####################################################

#https://github.com/Pithikos/websocket-client
#pip3 install websocket-client

from websocket import create_connection

ws = create_connection("ws://127.0.0.1:17777/")
ws.send("sys.version_info")
result =  ws.recv()
print(result)
ws.close()


