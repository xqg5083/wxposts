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
import sys,os
my_eval = eval
web_eval=lambda s:o2s(tryx(lambda:my_eval(s,globals()),lambda ex:{'errmsg':str(ex)}))

#####################################################
# e.g. my_import('myqmt').ver
my_import=lambda name, reload=True:__import__('importlib').reload(__import__(name)) if reload else __import__(name)

class obj(dict):
  def __init__(self,pa={}):
    for k in pa: self[k]=pa[k]
  def __getattr__(self,k):
    return tryx(lambda:self[k],False)
  def __setattr__(self,k,v):
    self[k]=v

# global obj store
g_obj = obj()

#####################################################
g_ctx = None
g_acct = None
def my_acct(acct=None):
    global g_acct
    if acct: g_acct = acct
    if not g_acct: raise Exception('empty g_acct') 
    return g_acct

def my_pos(accttype='stock',datatype='position',acct=None):
    rt = []
    for obj in get_trade_detail_data(acct or my_acct(),accttype,datatype):
        code6 = str(obj.m_strInstrumentID)
        mk2 = str(obj.m_strExchangeID)
        vol = float(obj.m_nVolume)
        mkp = float(obj.m_dMarketValue)
        prz = float(obj.m_dSettlementPrice)
        last = float(obj.m_nYesterdayVolume)
        rt.append([code6,mk2,vol,mkp,prz,last])
    return rt

def my_last_order_id(accttype='stock',datatype='order',acct=None):
    return get_last_order_id(acct or my_acct(),accttype,datatype)

def my_order(code,amt,prz=0,sleep_order_id=0,acct=None):
    global g_ctx
    if not acct: acct = my_acct()
    rst = passorder(23 if amt>0 else 24,1101,acct,code,11 if prz>0 else 14,prz,abs(amt),2,g_ctx)
    print('my_order:',code,amt,prz)
    if sleep_order_id>0:
        sleep(sleep_order_id)
        order_id = my_last_order_id(acct=acct)
        print('.order_id=',order_id)
        return order_id
    print('=>',rst)
    return rst

my_pos_clear=lambda:[my_order('{}.{}'.format(v[0],v[1]),-round(v[2])) for v in my_pos() if v[2]>0]

##################################################### websocket-server
#D:\py368x64\python -m pip install websocket-server --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple -t d:\qmt20211207\bin.x64\Lib
#https://github.com/Pithikos/python-websocket-server#api
from websocket_server import WebsocketServer
server_ws = WebsocketServer(host='0.0.0.0', port=17777)

##################################################### qmt start/stop
def init(ContextInfo):
    global g_ctx
    g_ctx = ContextInfo
    print('init')
    server_ws.set_fn_message_received(lambda clt,svr,msg:tryx(lambda:server_ws.send_message(clt,web_eval(msg))))
    server_ws.run_forever()
def stop(ContextInfo):
    print('stop')
    server_ws.disconnect_clients_abruptly()
def handlebar(ContextInfo):
    #global g_ctx
    #g_ctx = ContextInfo
    pass


