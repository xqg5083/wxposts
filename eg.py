from mypy import tryx,s2o,o2s

from superweb import superweb

class web(superweb):

    # /eg.index?a=1
    def index(self):
        from time import time as now
        return {'by':'eg','now':now()}

