from mypy import o2s,tryx
from flask import request,Flask

import importlib

app=Flask(__name__)

app.add_url_rule('/','default',lambda:{})

app.add_url_rule('/<c>.<m>','main',lambda c,m:o2s(tryx(lambda:getattr(importlib.import_module(c).web(request),m)(),lambda ex:{'errmsg':str(ex)})),methods=['GET','POST'])
