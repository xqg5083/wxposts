#-*- coding: utf-8 -*-

from __future__ import print_function
_print= print
_eval= eval
_import= __import__


def tryx(l,e=print):
    try: return l()
    except Exception as ex: return ex if True==e else e(ex) if e else None


import json
class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj): return tryx(lambda:json.JSONEncoder.default(self,obj),str)
s2o = lambda s:tryx(lambda:json.loads(s))
o2s = lambda o,indent=None:tryx(lambda:json.dumps(o, indent=indent, ensure_ascii=False, cls=MyJsonEncoder))


def time_maker(days=0,date=None,outfmt=None,infmt='%Y-%m-%d',months=0):
    from datetime import datetime,timedelta
    if date is None: _dt = datetime.now()
    else: _dt = datetime.fromtimestamp(int(date)) if infmt=='0' or not infmt\
         else datetime.strptime(str(date),infmt)
    if months>0 or months<0:
        from dateutil.relativedelta import relativedelta
        _dt += relativedelta(months=months)
    _dt += timedelta(days=days)
    if outfmt is None: outfmt = infmt
    if outfmt=='0' or not outfmt:return int(mktime(_dt.timetuple()))
    return _dt.strftime(outfmt)


import sys
flag_py2 = sys.version_info.major==2
if flag_py2: from urllib2 import urlopen
else: from urllib.request import urlopen
wc=lambda u=None, data=None, m='POST',timeout=10:tryx(lambda:urlopen(url=u,data=data.encode('utf-8') if isinstance(data,str) else o2s(data).encode('utf-8') if data else None,timeout=timeout).read().decode())


void=lambda *ate:None

