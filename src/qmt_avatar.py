#-*- coding: utf-8 -*-

from time import time as now, sleep

def tryx(l,e=print):
	try: return l()
	except Exception as ex: return ex if True==e else e(ex) if e else None

##################################################### libs

#D:\Python36x64>python -m pip install web.py --upgrade -t d:\qmt20211207\bin.x64\Lib
# hack for web.py
import sys
sys.argv=[]
#sck_host = '127.0.0.1'
sck_port = 7777
import os
os.environ['PORT'] = '{}'.format(sck_port)
##################################################### wrap calls
#my_eval = eval
def my_pos(accttype='stock',datatype='position'):
	_now = now()
	obj_list = get_trade_detail_data(g_acct,accttype,datatype)
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

import web
urls = (
    '/', 'index'
)
class index:
	def GET(self):
		#return "Hello, world! {}".format(now())
		return my_pos()
server = web.application(urls, globals())
g_ctx = None
def init(ContextInfo):
	global g_ctx
	g_ctx = ContextInfo
	server.run()
	print('inited')
def stop(ContextInfo):
	server.stop()
	print('stopped')
	
g_acct = "..."
