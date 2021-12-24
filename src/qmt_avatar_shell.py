#-*- coding: utf-8 -*-

def tryx(l,e=print):
    try: return l()
    except Exception as ex: return ex if True==e else e(ex) if e else None

def detect_py2():
    import sys
    return sys.version_info.major==2

def get_wc(flag_py2=False):
    flag_py2 = tryx(lambda:detect_py2())
    if flag_py2: from urllib2 import urlopen
    else: from urllib.request import urlopen
    wc=lambda u=None, data=None, m='POST',timeout=10:tryx(lambda:urlopen(url=u,data=data.encode('utf-8') if isinstance(data,str) else o2s(data).encode('utf-8') if data else None,timeout=timeout).read().decode())
    return wc

wc = get_wc()

def do(s): return wc('http://localhost:7777',s)

"""
python -i qmtshell.py
>>>
acct='acct_number'
do('my_acct("{}")'.format(acct))
do('my_pos()')

## list pos>0
[("('{}.{}',{}".format(v[0],v[1],v[2])) for v in s2o(do('my_pos()')) if v[2]>0]

## sell all (一键清仓)
[do("my_order('{}.{}',-round({}),0)".format(v[0],v[1],v[2])) for v in s2o(do('my_pos()')) if v[2]>0]

## sell all (一键清仓2)
do('my_pos_clear()')

## get_market_data
do("g_ctx.get_market_data(['close'],stock_code=['600000.SH'],start_time='20211224',end_time='20211225',skip_paused=True,period='1m',dividend_type='none').to_dict()")
"""

