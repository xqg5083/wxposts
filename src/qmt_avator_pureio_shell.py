def tryx(l,e=print):
    try: return l()
    except Exception as ex: return ex if True==e else e(ex) if e else None
read = lambda f,m='r',encoding='utf-8':open(f,m,encoding=encoding).read()
write = lambda f,s,m='w',encoding='utf-8':open(f,m,encoding=encoding).write(s)

from time import time as now,sleep
import marshal
def do(s):
    i=now()
    write('work/call/{}.txt'.format(i),s)
    sleep(1)
    return marshal.loads(read('work/back/{}.txt'.format(i),'rb',encoding=None))

"""
usage:

python -i qmt_avator_pureio_shell.py
>>>do('my_pos()')
>>>do('my_order("513050.SH",100,1.31)')

"""
