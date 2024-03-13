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

def test_dotL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A DOTL B ''')
        b = ScalarDotL(TRSVar("A"), TRSVar("B"))
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

def test_adjL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJL(X[r1; r2]) ''')
        b = AdjL(Labelled2(TRSVar("X"), TRSVar("r1"), TRSVar("r2")))
        assert a == b

def test_scalL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S SCRL X[r1; r2] ''')
        b = ScalL(TRSVar("S"), Labelled2(TRSVar("X"), TRSVar("r1"), TRSVar("r2")))
        assert a == b

def test_addL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A ADDL X[r1; r2] ADDL B ''')
        b = AddL(TRSVar("A"), Labelled2(TRSVar("X"), TRSVar("r1"), TRSVar("r2")), TRSVar("B"))
        assert a == b


def test_tensorL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' X1[r2] TSRL X0[r1] ''')
        b = TensorL(
            Labelled1(TRSVar("X1"), TRSVar("r2")), 
            Labelled1(TRSVar('X0'), TRSVar('r1')))
        assert a == b

def test_ketapplyL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' X[r1; r2] MLTKL K0[r1] ''')
        b = KetApplyL(
            Labelled2(TRSVar("X"), TRSVar("r1"), TRSVar("r2")), 
            Labelled1(TRSVar('K0'), TRSVar('r1')))
        assert a == b


def test_braapplyL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B0[r1] MLTBL X[r1; r2] ''')
        b = BraApplyL(
            Labelled1(TRSVar("B0"), TRSVar("r1")), 
            Labelled2(TRSVar('X'), TRSVar('r1'), TRSVar("r2")))
        assert a == b


def test_opouterL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K0[r1] OUTERL B0[r1] ''')
        b = OpOuterL(
            Labelled1(TRSVar("K0"), TRSVar("r1")), 
            Labelled1(TRSVar('B0'), TRSVar('r1')))
        assert a == b

def test_opapplyL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O0[r1] MLTOL O1[r1; r2] ''')
        b = OpApplyL(
            Labelled1(TRSVar("O0"), TRSVar("r1")), 
            Labelled2(TRSVar('O1'), TRSVar('r1'), TRSVar("r2")))
        assert a == b