
# This file was *autogenerated* from the file src/util/lazylist.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_20 = Integer(20); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1)
import functools
import itertools
import operator

class LazyList:
    def __init__(self, data = lambda n: _sage_const_0 , offset=_sage_const_0 , cache=True, printed=None):
        self.data = data
        self.doCache = cache
        self.offset = offset
        self.cache = {}
        self.printed = printed
        
    def __getitem__(self, n):
        if n in self.cache and self.doCache:
            return self.cache[n]
        if n < self.offset:
            raise IndexError("Index of LazyList too low! Given index was {} and the offset is {}".format(n, self.offset))
        data = self.data(n)
        if hasattr(data, 'simplify_full'):
            data = data.simplify_full()
        if self.doCache:
            self.cache[n] = data
        return data
    
    def __eq__(self, other):
        if self.offset != other.offset or self.toList(_sage_const_20 ) != other.toList(_sage_const_20 ):
            return False
        raise NotImplementedError("It's impossible to calculate if two infinite sequences are equal")
    
    def __iter__(self):
        for n in (itertools.count(self.offset) if self.printed==None else range(self.offset, self.offset + self.printed)):
            yield self[n]
    
    def toList(self, length):
        return [self[i] for i in range(self.offset, self.offset + (self.printed if length == None and self.printed != None else length))]
    
    def __add__(self, B):
        return liftBinaryOpToLazyList(operator.add)(self, B)
    
    def __mul__(self, B):
        return liftBinaryOpToLazyList(operator.mul)(self, B)
    
    def __repr__(self, length = None):
        res = ""
        for i in range(self.offset, self.offset + (_sage_const_20  if self.printed == None else self.printed) if length == None else length):
            res += str(self[i]) + ", "
        return res[:-_sage_const_2 ] + ", ..."
    
    def compress(self, k):
        if self.offset != _sage_const_0 :
            raise NotImplementedError("Can't compress list with non-zero offset")
        return LazyList(data = lambda n: self[n * k], printed = self.printed)
    
    def expand(self, k, filler = lambda n: _sage_const_0 ):
        if self.offset != _sage_const_0 :
            raise NotImplementedError("Can't expand list with non-zero offset")
        return LazyList(data = lambda n: self[n / k] if n % k == _sage_const_0  else filler(n), printed = self.printed)
    
    def applyRecursiveTransform(self, transformCoeffIndexTriples):
        if self.offset != _sage_const_0 :
            raise NotImplementedError("Can't apply recursive transform to list with non-zero offset")
        list = LazyList(cache = True, printed=self.printed)
        list.data = lambda n: sum([coeff * (_sage_const_1  if orIndex == "id" else self[orIndex]) * (_sage_const_1  if recIndex == "id" else list[recIndex]) for coeff, orIndex, recIndex in transformCoeffIndexTriples[n]])
        return list
    
    def fmap(self, f, cache = True):
        return LazyList(data = lambda n: f(self[n]), cache=cache, printed=self.printed, offset=self.offset)

    def toNearestGaussianIntegers(self):
        return self.fmap(toNearestGaussianInteger)
    
    def toNearestIntegers(self):
        return self.fmap(toNearestInteger)
    
BellTransform     = LazyList(data = lambda n: [(_sage_const_1 , "id", "id")] if n == _sage_const_0  else [(n, n, "id")] + [(-_sage_const_1 , i, n - i) for i in range(_sage_const_1 , n)])
BellAntiTransform = LazyList(data = lambda n: [(_sage_const_1 , "id", "id")] if n == _sage_const_0  else [(_sage_const_1 /n, n - i, i) for i in range(n)])


def liftBinaryOpToLazyList(op, exclude = -_sage_const_1 ):
    return lambda X, Y: LazyList(data = lambda n: op(X[n], Y[n]) if n > exclude else X[n], cache=True, printed = min(X.printed, Y.printed), offset = max(X.offset, Y.offset))

def liftUnaryOpToLazyList(func, exclude = -_sage_const_1 ):
    return lambda X: LazyList(data = lambda n: func(X[n]) if n > exclude else X[n], cache=True, printed = X.printed, offset = X.offset)

def toLazyList(list):
    return LazyList(data = lambda n: list[n] if n < len(list) else _sage_const_0 , cache = False, printed = len(list))

def DirichletConvolution(X, Y):
    if X.offset != _sage_const_0  or Y.offset != _sage_const_0 :
        raise NotImplementedError("Can't convolute lists with non-zero offset")
    return LazyList(data = lambda n: sum(X[d] * Y[n - d] for d in range(n + _sage_const_1 )), cache = True, printed = min(X.printed, Y.printed))

PointwiseProduct = liftBinaryOpToLazyList(operator.mul)

