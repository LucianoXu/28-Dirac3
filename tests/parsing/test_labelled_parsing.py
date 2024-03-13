from diracdec import *
from diracdec.theory.dirac_labelled import *
from diracdec import parse


def test_qreg():
    with wolfram_backend.wolfram_session():
        a = parse(r''' PAIRR(s, t) ''')
        b = QRegPair(TRSVar('s'), TRSVar('t'))
        assert a == b

        a = parse(r''' FSTR(s) ''')
        b = QRegFst(TRSVar('s'))
        assert a == b

        a = parse(r''' SNDR(s) ''')
        b = QRegSnd(TRSVar('s'))
        assert a == b


def test_qregset():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ESETR ''')
        b = EmptyRSet()
        assert a == b

        a = parse(r''' SETR(x) ''')
        b = RegRSet(TRSVar('x'))
        assert a == b

        a = parse(r''' x UNIONR y UNIONR z ''')
        b = UnionRSet(TRSVar('x'), TRSVar('y'), TRSVar('z'))
        assert a == b

        a = parse(r''' x SUBR y ''')
        b = SubRSet(TRSVar('x'), TRSVar('y'))
        assert a == b

def test_labelled1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' X[r] ''')
        b = Labelled1(TRSVar("X"), TRSVar("r"))
        assert a == b

        a = parse(r''' X[PAIRR(r1, r2)] ''')
        b = Labelled1(TRSVar("X"), QRegPair(TRSVar("r1"), TRSVar("r2")))
        assert a == b

def test_labelled2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' X[r1; r2] ''')
        b = Labelled2(TRSVar("X"), TRSVar("r1"), TRSVar("r2"))
        assert a == b

        a = parse(r''' X[PAIRR(r1, r2); FSTR(x)] ''')
        b = Labelled2(TRSVar("X"), QRegPair(TRSVar("r1"), TRSVar("r2")), QRegFst(TRSVar("x")))
        assert a == b

def test_tensorL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' X1[r2] TSRL X0[r1] ''')
        b = TensorL(
            Labelled1(TRSVar("X1"), TRSVar("r2")), 
            Labelled1(TRSVar('X0'), TRSVar('r1')))
        assert a == b