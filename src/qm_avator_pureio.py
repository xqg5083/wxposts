#-*- coding: utf-8 -*-
#print('__name__',__name__)
##################################################### configs
g_acct = '__replace_by_your_acct__'
dr_call = 'd:\\work\\call\\'
dr_back = 'd:\\work\\back\\'
dr_hist = 'd:\\work\\hist\\'

##################################################### libs
def tryx(l,e=print):
	try: return l()
	except Exception as ex: return ex if True==e else e(ex) if e else None
read = lambda f,m='r',encoding='utf-8':open(f,m,encoding=encoding).read()
write = lambda f,s,m='w',encoding='utf-8':open(f,m,encoding=encoding).write(s)
from time import time as now, sleep

#####################################################
g_ctx=None

fn_yymmdd_log = 'work.log' #TODO '{ymd}.log'.format(time_maker(outfmt='%y%m%d'))

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

def my_last_order_id(accttype='stock',datatype='order',acct=g_acct):# order/deal
	return get_last_order_id(acct,accttype,datatype)

def my_order(code,amt,prz,sleep_order_id=0,acct=g_acct):
	global g_ctx
	rst = passorder(23 if amt>0 else 24,1101,acct,code,11 if prz>0 else 5,prz,abs(amt),1,g_ctx)
	print('my_order(',code,amt,prz)
	if sleep_order_id>0:
		sleep(sleep_order_id)
		order_id = my_last_order_id(acct=acct)
		print(')order_id:',order_id)
		return order_id
	print('):',rst)
	return rst

# TODO add lock later. 2, even no use;)
def my_work_step(ContextInfo):
	#global g_ctx
	#g_ctx = ContextInfo
	import marshal
	my_eval = eval
	import os
	c=0
	_now = now()
	for f in os.walk(dr_call):
		c+=1
		if not f[2]: continue
		fn_dir = f[0]
		fn_base = f[2][0]
		fn = '{}/{}'.format(fn_dir, fn_base)
		s = tryx(lambda:read(fn))
		if not s: continue
		print(_now,c,'{',s) # TODO append to log
		os.rename(fn,'{}/{}'.format(dr_hist,fn_base+str(_now)))
		rst = tryx(lambda:my_eval(s),lambda e:str(e))
		rst_bin = tryx(lambda:marshal.dumps(rst),lambda e:str(e).encode())
		print('=>',len(rst_bin),'}',c,_now) # TODO append to log
		fn_back = '{}\\{}'.format(dr_back,fn_base)
		# put to callback-queue
		write(fn_back,rst_bin,'wb',encoding=None)
		# append to log
		write('{}\\{}'.format(dr_hist,fn_yymmdd_log),'\n{}=>{}'.format(s,rst),'a')
		#write('{}\\{}'.format(dr_hist,fn_yymmdd_log),rst_bin,'ab',encoding=None)

##################################################### adaptor
def handlebar(ContextInfo):
	global g_ctx
	g_ctx = ContextInfo
	my_work_step(ContextInfo)

def init(ContextInfo):
	global g_ctx
	g_ctx = ContextInfo
	_now = now()
	ContextInfo.run_time('my_work_step','1nSecond','2020-01-01 00:00:00')
	print('started',_now)


