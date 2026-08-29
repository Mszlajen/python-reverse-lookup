from inspect import getmro, isfunction
from types import MethodType

def lookup(self: object, mro: tuple[type, ...], name: str):
    for t in mro:
        try:
            attr = getattr(t, name)
        except AttributeError:
            continue
        if isfunction(attr):
            return MethodType(attr, self)
        return attr
    raise AttributeError(name=name, obj=self)

class ReverseLookup():
    def __getattribute__(self, name: str):
        mro = super().__getattribute__('__class__').mro()
        return lookup(self, mro, name)

    @classmethod
    def mro(cls):
        return list(reversed(cls.__mro__))

class Inner:
    __slots__ = ('obj', 'start_type')
    
    def __init__(self, obj: object, start_type: type):
        self.obj = obj
        self.start_type = start_type
    
    def __getattribute__(self, name: str):
        if name in ('start_type', 'obj'):
            return super().__getattribute__(name)
        start_type = self.start_type
        obj = self.obj
        mro = object.__getattribute__(obj, '__class__').mro()
        new_mro = mro[mro.index(start_type)+1:]
        return lookup(obj, new_mro, name)