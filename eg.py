from mypy import tryx,s2o,o2s

class web:
    def __init__(self,request=None):
        self.request = request
        param = {}
        args = self.request.args or {}
        for k in args: param[k] = args[k]

        json_str = request.get_data()
        #print('debug json_str',json_str)
        if json_str:
            json_obj = s2o(json_str) or {}
            for k in json_obj: param[k] = json_obj[k]

        self.param = param
        print('debug param',param)

    # /eg.index?a=1
    def index(self):
        from time import time as now
        return {'now':now()}

