from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import parse

def test_trans():
    with wolfram_backend.wolfram_session():
        a = parse(r''' TP(B)''')
        b = Transpose(TRSVar("B"))
        assert a == b

        a = parse(r''' TP(K)''')
        b = Transpose(TRSVar("K"))
        assert a == b

        a = parse(r''' TP(O)''')
        b = Transpose(TRSVar("O"))
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
        b = UnionSet(TRSVar("S2"), EmptySet(), TRSVar("S1"))
        assert a == b

        
def test_sums():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SUM(x, T, x)''')
        b = SumS(((TRSVar("x"), TRSVar("T")),), TRSVar("x"))
        assert a != b

        a_ = parse(r''' SUMS(x, T, x)''')
        assert a_ == b

        a = parse(r''' SUMS(x, x)''')
        b = SumS(((TRSVar("x"), UniversalSet()),), TRSVar("x"))
        assert a == b


def test_sum():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SUM(x, T, x)''')
        b = Sum(((TRSVar("x"), TRSVar("T")),), TRSVar("x"))
        assert a == b

        a = parse(r''' SUM(x, x)''')
        b = Sum(((TRSVar("x"), UniversalSet()),), TRSVar("x"))
        assert a == b

def test_abstraction():
    with wolfram_backend.wolfram_session():
        a = parse(r''' FUN x . x ''')
        b = Abstract(TRSVar("x"), TRSVar("x"))
        assert a == b

def test_apply():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A @ B ''')
        b = Apply(TRSVar("A"), TRSVar("B"))
        assert a == b

