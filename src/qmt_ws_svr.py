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
web_eval=lambda s:o2s(tryx(lambda:eval(s,globals()),lambda ex:{'errmsg':str(ex)}))

#####################################################

import sys,os

from websocket_server import WebsocketServer
server_ws = WebsocketServer(host='127.0.0.1', port=17777)
#server_ws.set_fn_new_client(lambda clt,svr:print('set_fn_new_client'))
server_ws.set_fn_message_received(lambda clt,svr,msg:server_ws.send_message(clt,web_eval(msg)))
server_ws.run_forever()


