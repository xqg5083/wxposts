#-*- coding: utf-8 -*-

import sys,os

################################### work from ..
#cwd = os.getcwd()
#sys.path.append(cwd+'/..')
##print(sys.path)
#os.chdir(cwd+'/..')

###################################
from time import time as now, sleep

def tryx(l,e=print):
  try: return l()
  except Exception as ex: return ex if True==e else e(ex) if e else None

import json
class MyJsonEncoder(json.JSONEncoder):
  def default(self, obj): return tryx(lambda:json.JSONEncoder.default(self,obj),str)
s2o = lambda s:tryx(lambda:json.loads(s))
o2s = lambda o,indent=None:tryx(lambda:json.dumps(o, indent=indent, ensure_ascii=False, cls=MyJsonEncoder))

# eval hid the globals/locals.... and then expose the data module later
safe_eval=lambda s,the_globals={},the_locals={}:o2s(tryx(lambda:eval(s,{'__builtins__':{'print':print,'globals':lambda:the_globals,'locals':lambda:the_locals}}),lambda ex:{'errmsg':str(ex)}))

my_import=lambda name, reload=False:__import__('importlib').reload(__import__(name)) if reload else __import__(name)

class obj(dict):
  def __init__(self,pa={}):
    for k in pa: self[k]=pa[k]
  def __getattr__(self,k):
    return tryx(lambda:self[k],False)
  def __setattr__(self,k,v):
    self[k]=v

# global datastore
g_obj = obj()

argv = sys.argv
argc = len(argv)
if argc<2: raise Exception('need argv[1]')
arg_port = int(argv[1])
arg_host = '127.0.0.1' if argc<3 else argv[2]

from websocket_server import WebsocketServer

def start_ws(port,host='127.0.0.1'):
  server_ws = WebsocketServer(host=host, port=port)
  server_ws.set_fn_new_client(lambda clt,svr:print('set_fn_new_client {}'.format(now())))
  server_ws.set_fn_message_received(lambda clt,svr,msg:server_ws.send_message(clt,safe_eval(msg,{'g':g_obj})))
  server_ws.run_forever()
  return server_ws

import threading
threading.Thread(target=start_ws,args=[arg_port,arg_host]).start()

# interact on stdin
for line in sys.stdin: print(tryx(lambda:eval(line)))

