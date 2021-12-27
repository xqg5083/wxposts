#-*- coding: utf-8 -*-
import sys,os
argv = sys.argv
argc = len(argv)
if argc<2: raise Exception('need argv[1]')
arg_port = int(argv[1])
arg_host = '127.0.0.1' if argc<3 else argv[2]

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

ws = create_connection('ws://{}:{}/'.format(arg_host,arg_port))
def do(s):
    ws.send(s)
    print(ws.recv())

for line in sys.stdin: do(line)

