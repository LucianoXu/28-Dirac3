from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import dirac_bigop_parse as parse

def test_trans():
    with wolfram_backend.wolfram_session():
        a = parse(r''' TRANK(B)''')
        b = KetTrans(TRSVar("B"))
        assert a == b

        a = parse(r''' TRANB(K)''')
        b = BraTrans(TRSVar("K"))
        assert a == b

        a = parse(r''' TRANO(O)''')
        b = OpTrans(TRSVar("O"))
        assert a == b

def test_sum():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SUM(x, x)''')
        b = Sum((TRSVar("x"),), TRSVar("x"))
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