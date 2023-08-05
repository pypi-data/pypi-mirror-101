# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/4/6
import copy
import operator

empty = object()
anti_recursion_dict = {}


def new_method_proxy(func):
    def inner(self, *args):
        if self._wrapped is empty:
            self._setup()
        return func(self._wrapped, *args)

    return inner


class LazyLoader:
    _wrapped = None

    def __init__(self, **kwargs):
        self._wrapped = empty
        anti_recursion_dict.update(kwargs)

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == "_wrapped":
            self.__dict__["_wrapped"] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == "_wrapped":
            raise TypeError("can't delete _wrapped.")
        if self._wrapped is empty:
            self._setup()

        delattr(self._wrapped, name)

    def _setup(self):
        raise NotImplementedError('subclasses of LazyObject must provide a _setup() method')

    def __reduce__(self):
        if self._wrapped is empty:
            self._setup()
        return unpickle_lazy_object, (self._wrapped,)

    def __getstate__(self):
        return {}

    def __copy__(self):
        if self._wrapped is empty:
            return type(self)()
        else:
            return copy.copy(self._wrapped)

    def __deepcopy__(self, memo):
        if self._wrapped is empty:
            result = type(self)()
            memo[id(self)] = result
            return result
        return copy.deepcopy(self._wrapped, memo)

    __str__ = new_method_proxy(str)
    __nonzero__ = new_method_proxy(bool)

    __dir__ = new_method_proxy(dir)

    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)

    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)


def unpickle_lazy_object(wrapped):
    return wrapped


class LazyHandler(LazyLoader):
    def _setup(self):
        self._wrapped = Handler(**copy.deepcopy(anti_recursion_dict))


class Handler:
    def __init__(self, **kwargs):
        print(kwargs, 'lazy handler')


if __name__ == '__main__':
    handler = LazyHandler(a=1, b=2)
    print(handler)
