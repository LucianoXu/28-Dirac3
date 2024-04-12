
from __future__ import annotations

from ..trs import *

from ...backends.formprint import *

#######################################################
# types

class ProdType(StdTypeTerm):
    fsymbol_print = 'prod'
    fsymbol = 'PROD'

    def __init__(self, T1: TypeTerm, T2: TypeTerm):
        super().__init__(T1, T2)
        self.T1 = T1
        self.T2 = T2
    
    def __str__(self) -> str:
        return f"({self.T1} ^ {self.T2})"
    

class Sca(StdTypeTerm):
    fsymbol_print = 'S'
    fsymbol = 'S'

    def __init__(self):
        super().__init__()
    

class Ket(StdTypeTerm):
    fsymbol_print = 'K'
    fsymbol = 'K'

    def __init__(self, T: TypeTerm):
        super().__init__(T)
        self.T = T
    


class Bra(StdTypeTerm):
    fsymbol_print = 'B'
    fsymbol = 'B'

    def __init__(self, T: TypeTerm):
        super().__init__(T)
        self.T = T


class Opt(StdTypeTerm):
    fsymbol_print = 'O'
    fsymbol = 'O'

    def __init__(self, T1: TypeTerm, T2: TypeTerm):
        super().__init__(T1, T2)
        self.T1 = T1
        self.T2 = T2
    
#####################################################
# terms

class Pair(StdTerm):
    fsymbol_print = 'PAIR'
    fsymbol = 'PAIR'

    def __init__(self, t1: Term, t2: Term):
        super().__init__(t1, t2)
    

    
class Fst(StdTerm):
    fsymbol_print = "FST"
    fsymbol = "FST"

    def __init__(self, p: Term):
        super().__init__(p)
    
class Snd(StdTerm):
    fsymbol_print = "SND"
    fsymbol = "SND"

    def __init__(self, p: Term):
        super().__init__(p)

class Delta(CommBinary):
    fsymbol_print = "δ"
    fsymbol = "DELTA"

    def __init__(self, b1 : Term, b2 : Term):
        CommBinary.__init__(self, b1, b2)

class ZeroS(StdTerm):
    fsymbol_print = "𝟎S"
    fsymbol = "0S"

    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "𝟎S"

class ZeroK(StdTerm):
    fsymbol_print = "𝟎K"
    fsymbol = "0K"

    def __init__(self, T: TypeTerm):
        super().__init__(T)

    def __str__(self) -> str:
        return "𝟎K"
    
class ZeroB(StdTerm):
    fsymbol_print = "𝟎B"
    fsymbol = "0B"

    def __init__(self, T: TypeTerm):
        super().__init__(T)

    def __str__(self) -> str:
        return "𝟎B"
    
class ZeroO(StdTerm):
    fsymbol_print = "𝟎O"
    fsymbol = "0O"

    def __init__(self, T1: TypeTerm, T2: TypeTerm):
        super().__init__(T1, T2)

    def __str__(self) -> str:
        return "𝟎O"
    
class OneS(StdTerm):
    fsymbol_print = "𝟏S"
    fsymbol = "1S"

    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "𝟏S"
    
class OneO(StdTerm):
    fsymbol_print = "𝟏O"
    fsymbol = "1O"

    def __init__(self, T: TypeTerm):
        super().__init__(T)

    def __str__(self) -> str:
        return "𝟏O"
    
class KetVec(StdTerm):
    fsymbol_print = "ket"
    fsymbol = "KET"

    def __init__(self, v : Term):
        super().__init__(v)

    def __str__(self) -> str:
        return f"|{self.args[0]}⟩"
    
class BraVec(StdTerm):
    fsymbol_print = "bra"
    fsymbol = "BRA"

    def __init__(self, v : Term):
        super().__init__(v)

    def __str__(self) -> str:
        return f"⟨{self.args[0]}|"

class Adj(StdTerm):
    fsymbol_print = "adj"
    fsymbol = "ADJ"

    def __init__(self, e: Term):
        super().__init__(e)


class Times(AC):
    fsymbol_print = "*"
    fsymbol = "TIMES"

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)


class Scaling(InfixBinary):
    fsymbol_print = "."
    fsymbol = "SCALING"

    def __init__(self, s: Term, e: Term):
        super().__init__(s, e)

class Add(AC):
    fsymbol_print = "+"
    fsymbol = "ADD"

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)

class Dot(InfixBinary):
    fsymbol_print = "·"
    fsymbol = "DOT"

    def __init__(self, e1: Term, e2: Term):
        super().__init__(e1, e2)

class Tensor(InfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "TENSOR"

    def __init__(self, e1: Term, e2: Term):
        super().__init__(e1, e2)