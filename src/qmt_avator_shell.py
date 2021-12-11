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
>>>do('my_pos()')
"""

