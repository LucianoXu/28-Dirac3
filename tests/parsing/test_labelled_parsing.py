from diracdec import *
from diracdec.theory.dirac_labelled import *
from diracdec import parse


def test_qreg():
    with wolfram_backend.wolfram_session():
        a = parse(r''' RPAIR(s, t) ''')
        b = QRegPair(TRSVar('s'), TRSVar('t'))
        assert a == b

        a = parse(r''' RFST(s) ''')
        b = QRegFst(TRSVar('s'))
        assert a == b

        a = parse(r''' RSND(s) ''')
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


