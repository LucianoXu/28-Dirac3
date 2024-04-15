
from __future__ import annotations

from ..trs import *

from ...backends.formprint import *


signature = Signature([Typing])

#######################################################
# types

class ProdType(InfixBinary):
    fsymbol_print = 'PROD'
    fsymbol = '^'

    def __init__(self, T1: TypeTerm, T2: TypeTerm):
        super().__init__(T1, T2)
        self.T1 = T1
        self.T2 = T2
    
    def __str__(self) -> str:
        return f"({self.T1} ^ {self.T2})"
signature.append(ProdType)

class ComplexScalar(StdTypeTerm):
    fsymbol_print = 'CS'
    fsymbol = 'CS'
    arity = 0

    def __init__(self):
        super().__init__()
signature.append(ComplexScalar)

class Sca(StdTypeTerm):
    fsymbol_print = 'S'
    fsymbol = 'S'
    arity = 0


    def __init__(self):
        super().__init__()
signature.append(Sca)

class Ket(StdTypeTerm):
    fsymbol_print = 'K'
    fsymbol = 'K'
    arity = 1

    def __init__(self, T: TypeTerm):
        super().__init__(T)
        self.T = T
signature.append(Ket)
    


class Bra(StdTypeTerm):
    fsymbol_print = 'B'
    fsymbol = 'B'
    arity = 1

    def __init__(self, T: TypeTerm):
        super().__init__(T)
        self.T = T
signature.append(Bra)

class Opt(StdTypeTerm):
    fsymbol_print = 'O'
    fsymbol = 'O'
    arity = 2

    def __init__(self, T1: TypeTerm, T2: TypeTerm):
        super().__init__(T1, T2)
        self.T1 = T1
        self.T2 = T2
signature.append(Opt)

#####################################################
# terms

####
# The symbols for complex avatar
###

class CompAdd(AC):
    fsymbol_print = 'CADD'
    fsymbol = 'CADD'

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)
signature.append(CompAdd)

class CompMul(AC):
    fsymbol_print = 'CMUL'
    fsymbol = 'CMUL'

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)
signature.append(CompMul)

class CompZero(StdTerm):
    fsymbol_print = 'C0'
    fsymbol = 'C0'
    arity = 0

    def __init__(self):
        super().__init__()
signature.append(CompZero)

class CompOne(StdTerm):
    fsymbol_print = 'C1'
    fsymbol = 'C1'
    arity = 0

    def __init__(self):
        super().__init__()
signature.append(CompOne)

class CompAdj(StdTerm):
    fsymbol_print = 'CADJ'
    fsymbol = 'CADJ'
    arity = 1

    def __init__(self, c: Term):
        super().__init__(c)
signature.append(CompAdj)

class Complex(StdTerm):
    fsymbol_print = 'C'
    fsymbol = 'C'
    arity = 1

    def __init__(self, c: Term):
        super().__init__(c)
signature.append(Complex)

class Pair(StdTerm):
    fsymbol_print = 'PAIR'
    fsymbol = 'PAIR'
    arity = 2

    def __init__(self, t1: Term, t2: Term):
        super().__init__(t1, t2)
signature.append(Pair)

    
class Fst(StdTerm):
    fsymbol_print = "FST"
    fsymbol = "FST"
    arity = 1

    def __init__(self, p: Term):
        super().__init__(p)
signature.append(Fst)
    
class Snd(StdTerm):
    fsymbol_print = "SND"
    fsymbol = "SND"
    arity = 1

    def __init__(self, p: Term):
        super().__init__(p)
signature.append(Snd)

class Delta(CommBinary):
    fsymbol_print = "δ"
    fsymbol = "DELTA"

    def __init__(self, b1 : Term, b2 : Term):
        CommBinary.__init__(self, b1, b2)
signature.append(Delta)

class ZeroS(StdTerm):
    fsymbol_print = "𝟎S"
    fsymbol = "0S"
    arity = 0

    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "𝟎S"
signature.append(ZeroS)

class ZeroK(StdTerm):
    fsymbol_print = "𝟎K"
    fsymbol = "0K"
    arity = 1

    def __init__(self, T: TypeTerm):
        super().__init__(T)

    def __str__(self) -> str:
        return "𝟎K"
signature.append(ZeroK)
    
class ZeroB(StdTerm):
    fsymbol_print = "𝟎B"
    fsymbol = "0B"
    arity = 1

    def __init__(self, T: TypeTerm):
        super().__init__(T)

    def __str__(self) -> str:
        return "𝟎B"
signature.append(ZeroB)

class ZeroO(StdTerm):
    fsymbol_print = "𝟎O"
    fsymbol = "0O"
    arity = 2

    def __init__(self, T1: TypeTerm, T2: TypeTerm):
        super().__init__(T1, T2)

    def __str__(self) -> str:
        return "𝟎O"
signature.append(ZeroO)
    
class OneS(StdTerm):
    fsymbol_print = "𝟏S"
    fsymbol = "1S"
    arity = 0

    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "𝟏S"
signature.append(OneS)
    
class OneO(StdTerm):
    fsymbol_print = "𝟏O"
    fsymbol = "1O"
    arity = 1

    def __init__(self, T: TypeTerm):
        super().__init__(T)

    def __str__(self) -> str:
        return "𝟏O"
signature.append(OneO)
    
class KetVec(StdTerm):
    fsymbol_print = "KET"
    fsymbol = "KET"
    arity = 1

    def __init__(self, v : Term):
        super().__init__(v)

    def __str__(self) -> str:
        return f"|{self.args[0]}⟩"
signature.append(KetVec)

class BraVec(StdTerm):
    fsymbol_print = "BRA"
    fsymbol = "BRA"
    arity = 1

    def __init__(self, v : Term):
        super().__init__(v)

    def __str__(self) -> str:
        return f"⟨{self.args[0]}|"
signature.append(BraVec)

class Adj(StdTerm):
    fsymbol_print = "ADJ"
    fsymbol = "ADJ"
    arity = 1

    def __init__(self, e: Term):
        super().__init__(e)
signature.append(Adj)


class Times(AC):
    fsymbol_print = "*"
    fsymbol = "*"

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)
signature.append(Times)

class Scaling(InfixBinary):
    fsymbol_print = "."
    fsymbol = "."

    def __init__(self, s: Term, e: Term):
        super().__init__(s, e)
signature.append(Scaling)

class Add(AC):
    fsymbol_print = "+"
    fsymbol = "+"

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)
signature.append(Add)

class Dot(InfixBinary):
    fsymbol_print = "·"
    fsymbol = "@"

    def __init__(self, e1: Term, e2: Term):
        super().__init__(e1, e2)
signature.append(Dot)

class Tensor(InfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "&"

    def __init__(self, e1: Term, e2: Term):
        super().__init__(e1, e2)
signature.append(Tensor)