from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import parse

def test_trans():
    with wolfram_backend.wolfram_session():
        a = parse(r''' TP(B)''')
        b = Transpose(Var("B"))
        assert a == b

        a = parse(r''' TP(K)''')
        b = Transpose(Var("K"))
        assert a == b

        a = parse(r''' TP(O)''')
        b = Transpose(Var("O"))
        assert a == b


#####################################
# set

def test_set():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ESET ''')
        b = EmptySet()
        assert a == b

        a = parse(r''' USET ''')
        b = UniversalSet()
        assert a == b

        a = parse(r''' S1 UNION S2 UNION ESET''')
        b = UnionSet(Var("S2"), EmptySet(), Var("S1"))
        assert a == b

        
def test_sums():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SUM(x, T, x)''')
        b = SumS(((Var("x"), Var("T")),), Var("x"))
        assert a != b

        a_ = parse(r''' SUMS(x, T, x)''')
        assert a_ == b

        a = parse(r''' SUMS(x, x)''')
        b = SumS(((Var("x"), UniversalSet()),), Var("x"))
        assert a == b


def test_sum():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SUM(x, T, x)''')
        b = Sum(((Var("x"), Var("T")),), Var("x"))
        assert a == b

        a = parse(r''' SUM(x, x)''')
        b = Sum(((Var("x"), UniversalSet()),), Var("x"))
        assert a == b

def test_abstraction():
    with wolfram_backend.wolfram_session():
        a = parse(r''' FUN x . x ''')
        b = Abstract(Var("x"), Var("x"))
        assert a == b

def test_apply():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A @ B ''')
        b = Apply(Var("A"), Var("B"))
        assert a == b

