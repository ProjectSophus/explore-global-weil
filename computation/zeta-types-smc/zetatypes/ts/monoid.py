# coding=utf8

# This file was *autogenerated* from the file src/ts/monoid.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_0 = Integer(0)# input=raw_input 


### Methods for Tannakian symbols with elements from a general commutative monoid
###
### Binary operations:     Direct sum (+)
###                        Tensor product (*)
###
### Unary operations:      lambdaoperation
###                        adamsoperation
###                        gammaoperation
###                        symmetricpoweroperation
###
### Invariants:            determintant
###                        augmentation
###                        evendimension
###                        odddimension
###                        superdimension
###
### Factory methods:       createElement
###                        parseSymbol
###
### Printing methods:      _repr_
###                        _latex_
###
### Other:                 upstairs
###                        downstairs
###                        islineelement
###                        fmap
###
### For examples, see separate tutorial file (add file name???)


from sage.categories.additive_monoids import AdditiveMonoids
import re

class TannakianSymbols(CombinatorialFreeModule):
    """
    """
    def __init__(self, R, M, multiplicative=True):
        self.base_monoid = M
        
        if multiplicative:
            category = Monoids().Commutative()
        else:
            category = AdditiveMonoids().AdditiveCommutative()
            
        CombinatorialFreeModule.__init__(self, R, M, category=category.Algebras(R))

    #Create a Tannakian Symbol from a list of element-multiplicity pairs
    def createElement(self,e):
        B = self.basis()
        t = _sage_const_0  * B[_sage_const_1 ]
        for x,m in e:
            t += m*B[x]
        return t

    # Compiling regexes for parsing (flat structure so regex should be fine.)
    flatTerm = re.compile("^\s*((?:-|)\s*\d+)\s*\*\s*\[([^\[\]]*)\]\s*$") # Parses a term of a flat expression (into two groups)
    flatFormMatch = re.compile("^\|(.*)\|$") # Removes bars on the sides of flat expression
    flatMinusSub = re.compile("(?<=\])\s*-([^\[\]]*)\[") # Replaces a single minus with a plus and a minus (when app.)
    flatMinusNoneSub = re.compile("-\s*\[") # Replaces a minus with no coeff with a - 1 * ...
    flatPlusSub = re.compile("\+\s*\[") # Replaces a flat plus without a coeff with a 1 * ...
    flatNoneSub = re.compile("^\s*\[") # Replaces an empty coeff on start with 1 * ...

    # Create a Tannakian Symbol from a string containing symbol notation (e.g. "{2}/{1, 5}")
    def parseSymbol(self, string):
        B = self.basis()
        f = _sage_const_0  * B[_sage_const_1 ]
        if self.flatFormMatch.match(string):
            s = string
            s = self.flatFormMatch.match(s).group(_sage_const_1 )
            s = self.flatMinusSub.sub(lambda match: ' + - %s [' % match.group(_sage_const_1 ), s)
            s = self.flatMinusNoneSub.sub(' - 1 * [', s)
            s = self.flatPlusSub.sub(' + 1 * [', s)
            s = self.flatNoneSub.sub('1 * [', s)

            terms = s.split('+')
            for x in terms:
                amt, b = self.flatTerm.match(x).groups()
                f += int(amt) * B[eval(preparse(b))]
        else:
            s = preparse(string)
            upstairs = s.split('/')[_sage_const_0 ].replace('{','').replace('}','').split(',')
            downstairs = s.split('/')[_sage_const_1 ].replace('{','').replace('}','').split(',')
            if not "Ø" in upstairs[_sage_const_0 ]:
                for x in upstairs:
                    if (x.strip() != ""):
                        f += B[eval(x.strip())]
            if not "Ø" in downstairs[_sage_const_0 ]:
                for x in downstairs:
                    if (x.strip() != ""):
                        f -= B[eval(x.strip())]
        return f

        
    #Tannakian Symbol Class
    class Element(CombinatorialFreeModule.Element):
        
        def __init__(self,*args,**kwargs):
            self.lambdacache={}
            self.symmetricpowercache={}
            CombinatorialFreeModule.Element.__init__(self, *args, **kwargs)
        
        #Adams-operation applied to a Tannakian Symbol
        def adamsoperation(self, k):
            e = []
            for a,m in self:
                e.append((a**k,m))
            return parent(self).createElement(e)
        
        #Lambda-operation applied to a Tannakian Symbol
        def lambdaoperation(self, k):
            if k in self.lambdacache:
                return self.lambdacache[k]
            if k == _sage_const_0 :
                self.lambdacache[_sage_const_0 ] = parent(self).createElement([[_sage_const_1 ,_sage_const_1 ]])
                return self.lambdacache[_sage_const_0 ]
            if k == _sage_const_1 :
                self.lambdacache[_sage_const_1 ] = self
                return self.lambdacache[_sage_const_1 ]
            output = _sage_const_0 
            for i in range(k):
                output += (-_sage_const_1 )**i * self.lambdaoperation(i) * self.adamsoperation(k-i)
            output = (-_sage_const_1 )**(k+_sage_const_1 ) * output/(k)
            self.lambdacache[k] = output
            return output
        
        #Gamma-operation applied to a Tannakian Symbol
        def gammaoperation(self, k):
            output = _sage_const_0 
            for i in range(k):
                output += self.lambdaoperation(k-i) * binomial(k-_sage_const_1 ,i)
            return output
        
        #Symmetric power operations applied to Tannakian symbol
        def symmetricpoweroperation(self, k):
            if k in self.symmetricpowercache:
                return self.symmetricpowercache[k]
            else:
                if k == _sage_const_0 :
                    self.symmetricpowercache[k] = parent(self).createElement([[_sage_const_1 ,_sage_const_1 ]])
                    return self.symmetricpowercache[k]
            
                output = parent(self).createElement([])
                for i in range(_sage_const_1 , k + _sage_const_1 ):
                    output += (-_sage_const_1 )**(i+_sage_const_1 ) * self.lambdaoperation(i) * self.symmetricpoweroperation(k - i)
                
                self.symmetricpowercache[k] = output
                return output
            
            
        def determinant(self):
            prod = parent(self).base_monoid.one()
            for x, n in self:
                prod *= x**n
            return prod
        
        def augmentation(self):
            amt = _sage_const_0 
            for x, n in self:
                amt += n
            return amt
        
        def evendimension(self):
            amt = _sage_const_0 
            for x, n in self:
                if n > _sage_const_0 :
                    amt += n
            return amt
        
        def odddimension(self):
            amt = _sage_const_0 
            for x, n in self:
                if n < _sage_const_0 :
                    amt += -n
            return amt
        
        def superdimension(self):
            return (self.evendimension(), self.odddimension())
        
        def islineelement(self):
            return self.superdimension() == (_sage_const_1 , _sage_const_0 )
        
        def upstairs(self):
            return sum([[x]*n for x, n in self if n > _sage_const_0 ], [])
        
        def downstairs(self):
            return sum([[x]*(-n) for x, n in self if n < _sage_const_0 ], [])
        
        def fmap(self, f):
            return parent(self).createElement([(f(x), n) for x, n in self])
        
        def filter(self, f):
            return parent(self).createElement([(x, n) for x, n in self if f(x)])
        
        #Function to automatically print Tannakian symbols as a string (e.g. "{2}/{1, 5}") or in LaTeX format
        def _repr_(self, latex=false, element_stringifier = str, post_proc=None):
            #if self.parent().base_ring() != ZZ:
            #    return CombinatorialFreeModule.Element._repr_(self)
            
            upstairs = []
            downstairs = []
            for a,m in self:
                if m < _sage_const_0 :
                    for i in range(-m):
                        downstairs.append(a)
                if m > _sage_const_0 :
                    for i in range(m):
                        upstairs.append(a)
            
            upstairsText = multisetString(upstairs, latex=latex, element_stringifier=element_stringifier)
            downstairsText = multisetString(downstairs, latex=latex, element_stringifier=element_stringifier)
            
            ans = ""
            
            if latex:
                ans = "\\frac{"+upstairsText+"}{"+downstairsText+"}"
            else:
                ans = upstairsText + "/" + downstairsText
            
            if post_proc == None:
                return ans
            else:
                return post_proc(ans)
            
            
        #Function to create LaTeX representation of a Tannakian Symbol
        def _latex_(self):
            #if self.parent().base_ring() != ZZ:
            #    return CombinatorialFreeModule.Element._repr_(self)
            
            return self._repr_(latex=true)

### Helper Functions ###

def multisetString(multiset, latex=false, element_stringifier=str):
    if element_stringifier == str and latex:
        element_stringifier = lambda x: x._latex_()
    if not multiset:
        return ("\\varnothing" if latex else "Ø")
    else:
        return ("{" if not latex else "\\{") + ', '.join([element_stringifier(a) for a in multiset]) + ("}" if not latex else "\\}")

