from yaml import Loader
from os.path import abspath

class Base:
    def __init__(self, *args, **kwargs):
        for a in args:  
            if type(a) is dict:
                self.__dict__ = a
        for k, v in kwargs.items():
            if k in allkw:
                self.__dict__.update({k:v})

    def __repr__(self):
        items = [f'{k}={v}' for k, v in self.__dict__.items()]
        return f"<{self.__class__.__name__}({', '.join(items)})>"

def load(n):
    with open(n, 'r') as f:
        data = Loader(f.read()).get_data()
    return unpack(data)

def unpack(i, c=0, rk=''):
    c += 1
    attrs = {}
    if type(i) is dict:
        for k, v in i.items():
            if type(v) is dict:
                attrs.update({k:unpack(v, c, k)})
            elif type(v) is list:
                attrs.update({k:unpack(v, c, k)})
            elif type(v) is (str or int):
                attrs.update({k:v})
    elif type(i) is list:
        attrs = []
        for li in i:
            if type(li) is dict:
                attrs.append(unpack(li, c, rk))
            elif type(li) is list:
                attrs.append(unpack(li, c, rk))
            elif type(li) is (str or int):
                attrs.append(li)
        return attrs
    elif type(i) is (str or int):
        return i
    return type(rk[:-1] if rk.endswith('s') else rk, (Base,), {})(attrs)
