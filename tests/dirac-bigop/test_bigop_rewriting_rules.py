
from diracdec import *

from diracdec import dirac_bigop_parse as parse, dirac_bigop_trs as trs

def test_KET_TRANS_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANK(0B)''')
        b = parse(r'''0K''')
        assert trs.normalize(a) == trs.normalize(b)


def test_KET_TRANS_2():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANK(BRA(s))''')
        b = parse(r'''KET(s)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''TRANK(BRA('a - a'))''')
        b = parse(r'''KET('0')''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TRANS_3():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANK(ADJB(K0))''')
        b = parse(r'''ADJK(TRANB(K0))''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TRANS_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANK(TRANB(K0))''')
        b = parse(r'''K0''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TRANS_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANK(S0 SCRB B0)''')
        b = parse(r'''S0 SCRK TRANK(B0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TRANS_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANK(B1 ADDB B2 ADDB B3)''')
        b = parse(r'''TRANK(B1) ADDK TRANK(B2) ADDK TRANK(B3)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_KET_TRANS_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANK(B0 MLTB O0)''')
        b = parse(r'''TRANO(O0) MLTK TRANK(B0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TRANS_8():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANK(B1 TSRB B2)''')
        b = parse(r'''TRANK(B1) TSRK TRANK(B2)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_BRA_TRANS_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANB(0K)''')
        b = parse(r'''0B''')
        assert trs.normalize(a) == trs.normalize(b)


def test_BRA_TRANS_2():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANB(KET(s))''')
        b = parse(r'''BRA(s)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''TRANB(KET('a - a'))''')
        b = parse(r'''BRA('0')''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TRANS_3():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANB(ADJK(B0))''')
        b = parse(r'''ADJB(TRANK(B0))''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TRANS_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANB(TRANK(B0))''')
        b = parse(r'''B0''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TRANS_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANB(S0 SCRK K0)''')
        b = parse(r'''S0 SCRB TRANB(K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TRANS_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANB(K1 ADDK K2 ADDK K3)''')
        b = parse(r'''TRANB(K1) ADDB TRANB(K2) ADDB TRANB(K3)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_BRA_TRANS_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANB(O0 MLTK K0)''')
        b = parse(r'''TRANB(K0) MLTB TRANO(O0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TRANS_8():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANB(K1 TSRK K2)''')
        b = parse(r'''TRANB(K1) TSRB TRANB(K2)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_OPT_TRANS_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANO(0O)''')
        b = parse(r'''0O''')
        assert trs.normalize(a) == trs.normalize(b)


def test_OPT_TRANS_2():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANO(1O)''')
        b = parse(r'''1O''')
        assert trs.normalize(a) == trs.normalize(b)


def test_OPT_TRANS_3():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANO(K0 OUTER B0)''')
        b = parse(r'''TRANK(B0) OUTER TRANB(K0)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''TRANO(KET('s') OUTER BRA('t'))''')
        b = parse(r'''KET('t') OUTER BRA('s')''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TRANS_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANO(ADJO(O0))''')
        b = parse(r'''ADJO(TRANO(O0))''')
        assert trs.normalize(a) == trs.normalize(b)
        
def test_OPT_TRANS_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANO(TRANO(O0))''')
        b = parse(r'''O0''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TRANS_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANO(S0 SCRO O0)''')
        b = parse(r'''S0 SCRO TRANO(O0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TRANS_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANO(O1 ADDO O2 ADDO O3)''')
        b = parse(r'''TRANO(O1) ADDO TRANO(O2) ADDO TRANO(O3)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_OPT_TRANS_8():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANO(O1 MLTO O2)''')
        b = parse(r'''TRANO(O2) MLTO TRANO(O1)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TRANS_9():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TRANO(O1 TSRO O2)''')
        b = parse(r'''TRANO(O1) TSRO TRANO(O2)''')
        assert trs.normalize(a) == trs.normalize(b)

###########################################################
# beta reduction

def test_BETA_REDUCTION():
    with wolfram_backend.wolfram_session():
        a = parse(''' (FUN x.A) @ a''')
        b = parse(''' A ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' (FUN x.x) @ a''')
        b = parse(''' a ''')
        assert trs.normalize(a) == trs.normalize(b)