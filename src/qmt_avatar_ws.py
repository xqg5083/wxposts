#-*- coding: utf-8 -*-
"""
TODO websocket server (to replace web.py)
https://github.com/Pithikos/python-websocket-server
TODO
do("g_ctx.get_market_data(['close'],stock_code=['600000.SH'],start_time='20211224',end_time='20211225',skip_paused=True,period='1m',dividend_type='none').to_dict()")
"""
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
g_ctx = None
#my_eval = eval
g_acct = None
def my_acct(acct=None):
	global g_acct
	if acct: g_acct = acct
	if not g_acct: raise Exception('empty g_acct') 
	return g_acct

def my_pos(accttype='stock',datatype='position',acct=None):
	if not acct: acct = my_acct()
	_now = now()
	obj_list = get_trade_detail_data(acct,accttype,datatype)
	print('my_pos',obj_list)
	rt = []
	c=0
	for obj in obj_list:
		code6 = str(obj.m_strInstrumentID) #TODO padding 6
		mk2 =str(obj.m_strExchangeID) # SZ/SH?
		last = float(obj.m_nYesterdayVolume)
		vol = float(obj.m_nVolume)
		prz = float(obj.m_dSettlementPrice)
		mkp = float(obj.m_dMarketValue)
		c+=1
		print(_now,c,code6,mk2,vol,prz,mkp)
		rt.append([code6,mk2,vol,mkp,prz,last])
		if False:
			for k in dir(obj):#print(k)
				if str(k).startswith('m_'):
					v = eval('obj.'+k)
					print(k,'=',v)
	return rt

def my_last_order_id(accttype='stock',datatype='order',acct=None):# order/deal
	return get_last_order_id(acct or my_acct(),accttype,datatype)

def my_order(code,amt,prz=0,sleep_order_id=0,acct=None):
	global g_ctx
	if not acct: acct = my_acct()
	#rst = passorder(23 if amt>0 else 24,1101,acct,code,11,prz,abs(amt),2,g_ctx)
	#rst = passorder(23 if amt>0 else 24,1101,acct,code,5,prz,abs(amt),2,g_ctx)
	rst = passorder(23 if amt>0 else 24,1101,acct,code,11 if prz>0 else 14,prz,abs(amt),2,g_ctx)
	print('my_order(',code,amt,prz)
	if sleep_order_id>0:
		sleep(sleep_order_id)
		order_id = my_last_order_id(acct=acct)
		print(')order_id:',order_id)
		return order_id
	print('):',rst)
	return rst

my_pos_clear=lambda:[my_order('{}.{}'.format(v[0],v[1]),-round(v[2])) for v in my_pos() if v[2]>0]

##################################################### web.py
import web
web.config.debug=True
import sys
sys.argv=[]
#sck_host = '127.0.0.1'
sck_port = 7777
import os
os.environ['PORT'] = '{}'.format(sck_port)

#web_eval=lambda s:o2s(tryx(lambda:my_eval(s,globals()),lambda ex:{'errmsg':str(ex)}))
web_eval=lambda s:o2s(tryx(lambda:eval(s,globals()),lambda ex:{'errmsg':str(ex)}))

#D:\Python36x64>python -m pip install web.py --upgrade -t d:\qmt20211207\bin.x64\Lib
class index:
	def POST(self): return web_eval(web.data())
server = web.application(('/', 'index',), globals())

##################################################### qmt
def init(ContextInfo):
	global g_ctx
	g_ctx = ContextInfo
	server.run()
	print('inited')
def stop(ContextInfo):
	server.stop()
	print('stopped')
def handlebar(ContextInfo):
	global g_ctx
	g_ctx = ContextInfo
	pass
