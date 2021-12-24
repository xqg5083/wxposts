#-*- coding: utf-8 -*-
from time import time as now, sleep
def tryx(l,e=print):
	try: return l()
	except Exception as ex: return ex if True==e else e(ex) if e else None
#####################################################
g_ctx = None
my_eval = eval
#D:\Python36x64>python -m pip install web.py --upgrade -t d:\qmt20211207\bin.x64\Lib
# hack for web.py
##################################################### {
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
	if not acct: acct = my_acct()
	print('debug a1',type(get_last_order_id))
	return get_last_order_id(acct,accttype,datatype)

def my_order(code,amt,prz,sleep_order_id=0,acct=None):
	if not acct: acct = my_acct()
	rst = passorder(23 if amt>0 else 24,1101,acct,code,11,prz,abs(amt),1,g_ctx)
	print('my_order(',code,amt,prz)
	if sleep_order_id>0:
		sleep(sleep_order_id)
		order_id = my_last_order_id(acct=acct)
		print(')order_id:',order_id)
		return order_id
	print('):',rst)
	return rst

##################################################### web.py
import web
web.config.debug=True
import sys
sys.argv=[]
#sck_host = '127.0.0.1'
sck_port = 7777
import os
os.environ['PORT'] = '{}'.format(sck_port)

web_eval=lambda s:tryx(lambda:my_eval(s,globals()),lambda ex:{'errmsg':str(ex)})

class index:
	def GET(self):
		return web_eval('len(get_trade_detail_data(g_acct,"stock","position"))')
		#return web_eval('sys.version_info')
		#return web_eval('get_last_order_id(g_acct,"stock","order")')
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
	pass

