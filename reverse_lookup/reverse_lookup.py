from inspect import getmro, isfunction, ismemberdescriptor
from types import MethodType

def lookup(self: object, mro: tuple[type, ...], name: str):
    for t in mro:
        try:
            attr = object.__getattribute__(t, name)
        except AttributeError:
            continue
        if ismemberdescriptor(attr):
            return attr.__get__(self, t)
        if isfunction(attr):
            return MethodType(attr, self)
        return attr
    
    try:
        return object.__getattribute__(self, '__dict__')[name]
    except (AttributeError, KeyError) as e:
        ...
    raise AttributeError(name=name, obj=self)

class ReverseLookup():
    def __getattribute__(self, name: str):
        mro = super().__getattribute__('__class__').mro()
        return lookup(self, mro, name)

    @classmethod
    def mro(cls):
        return list(reversed(cls.__mro__))

class Inner:
    __slots__ = ('__obj__', '__start_type__')
    
    def __init__(self, obj: object, start_type: type):
        self.__obj__ = obj
        self.__start_type__ = start_type
    
    def __getattribute__(self, name: str):
        if name in ('__obj__', '__start_type__'):
            return super().__getattribute__(name)
        start_type = self.__start_type__
        obj = self.__obj__
        mro = object.__getattribute__(obj, '__class__').mro()
        new_mro = mro[mro.index(start_type)+1:]
        return lookup(obj, new_mro, name)
        