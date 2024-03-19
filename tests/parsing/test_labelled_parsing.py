from diracdec import *
from diracdec.theory.dirac_labelled import *
from diracdec import parse


def test_qreg():
    with wolfram_backend.wolfram_session():
        a = parse(r''' PAIRR(s, t) ''')
        b = QRegPair(Var('s'), Var('t'))
        assert a == b

        a = parse(r''' FSTR(s) ''')
        b = QRegFst(Var('s'))
        assert a == b

        a = parse(r''' SNDR(s) ''')
        b = QRegSnd(Var('s'))
        assert a == b


def test_qregset():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ESETR ''')
        b = EmptyRSet()
        assert a == b

        a = parse(r''' SETR(x) ''')
        b = RegRSet(Var('x'))
        assert a == b

        a = parse(r''' x UNIONR y UNIONR z ''')
        b = UnionRSet(Var('x'), Var('y'), Var('z'))
        assert a == b

        a = parse(r''' x SUBR y ''')
        b = SubRSet(Var('x'), Var('y'))
        assert a == b

def test_dotL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A DOTL B ''')
        b = ScalarDotL(Var("A"), Var("B"))
        assert a == b

def test_labelled1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' X[r] ''')
        b = Labelled1(Var("X"), Var("r"))
        assert a == b

        a = parse(r''' X[PAIRR(r1, r2)] ''')
        b = Labelled1(Var("X"), QRegPair(Var("r1"), Var("r2")))
        assert a == b

def test_labelled2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' X[r1; r2] ''')
        b = Labelled2(Var("X"), Var("r1"), Var("r2"))
        assert a == b

        a = parse(r''' X[PAIRR(r1, r2); FSTR(x)] ''')
        b = Labelled2(Var("X"), QRegPair(Var("r1"), Var("r2")), QRegFst(Var("x")))
        assert a == b

def test_adjL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJL(X[r1; r2]) ''')
        b = AdjL(Labelled2(Var("X"), Var("r1"), Var("r2")))
        assert a == b

def test_scalL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S SCRL X[r1; r2] ''')
        b = ScalL(Var("S"), Labelled2(Var("X"), Var("r1"), Var("r2")))
        assert a == b

def test_addL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A ADDL X[r1; r2] ADDL B ''')
        b = AddL(Var("A"), Labelled2(Var("X"), Var("r1"), Var("r2")), Var("B"))
        assert a == b

def test_ketapplyL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' X[r1; r2] MLTKL K0[r1] ''')
        b = KetApplyL(
            Labelled2(Var("X"), Var("r1"), Var("r2")), 
            Labelled1(Var('K0'), Var('r1')))
        assert a == b

def test_kettensorL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K1[r2] TSRKL K0[r1] ''')
        b = KetTensorL(
            Labelled1(Var("K1"), Var("r2")), 
            Labelled1(Var('K0'), Var('r1')))
        assert a == b


def test_braapplyL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B0[r1] MLTBL X[r1; r2] ''')
        b = BraApplyL(
            Labelled1(Var("B0"), Var("r1")), 
            Labelled2(Var('X'), Var('r1'), Var("r2")))
        assert a == b

def test_bratensorL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B1[r2] TSRBL B0[r1] ''')
        b = BraTensorL(
            Labelled1(Var("B1"), Var("r2")), 
            Labelled1(Var('B0'), Var('r1')))
        assert a == b


def test_opouterL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K0[r1] OUTERL B0[r1] ''')
        b = OpOuterL(
            Labelled1(Var("K0"), Var("r1")), 
            Labelled1(Var('B0'), Var('r1')))
        assert a == b

def test_opapplyL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O0[r1] MLTOL O1[r1; r2] ''')
        b = OpApplyL(
            Labelled1(Var("O0"), Var("r1")), 
            Labelled2(Var('O1'), Var('r1'), Var("r2")))
        assert a == b

def test_optensorL():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O1[r2] TSROL O0[r1] ''')
        b = OpTensorL(
            Labelled1(Var("O1"), Var("r2")), 
            Labelled1(Var('O0'), Var('r1')))
        assert a == b