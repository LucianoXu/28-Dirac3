

from diracdec import *


# these tests are based on wolfram engine for complex and basis
def test_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''CONJS("0" ADDS "0" ADDS CONJS(CONJS("0"))) ADDS "0"''')
        b = parse(r'''CONJS("0")''')

        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_BASIS_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' FST(PAIR('x', 't')) ''')
        b = parse(r''' 'x' ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

        a = parse(r''' FST(PAIR(PAIR(x, y), 't')) ''')
        b = parse(r''' PAIR(x, y) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_BASIS_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SND(PAIR('x', 't')) ''')
        b = parse(r''' 't' ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

        a = parse(r''' SND(PAIR(PAIR(x, y), 't')) ''')
        b = parse(r''' 't' ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_BASIS_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' PAIR(FST(p), SND(p)) ''')
        b = parse(r''' p ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)


def test_DELTA_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' DELTA(u, PAIR(s, t)) ''')
        b = parse(r''' DELTA(FST(u), s) MLTS DELTA(SND(u), t) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_DELTA_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' DELTA(FST(u), FST(v)) MLTS DELTA(SND(u), SND(v)) ''')
        b = parse(r''' DELTA(u, v) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

        a = parse(r''' DELTA(FST(u), FST(v)) MLTS DELTA(SND(u), SND(v)) MLTS "2" ''')
        b = parse(r''' DELTA(u, v) MLTS "2" ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)



def test_SCR_COMPLEX_9():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a MLTS (b ADDS c) ''')
        b = parse(r''' (a MLTS b) ADDS (a MLTS c) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

        a = parse(r''' "x" MLTS ((a MLTS "2.2") ADDS ("3.2" MLTS b)) ''')
        b = parse(r''' ("x" MLTS a MLTS "2.2") ADDS ("x" MLTS "3.2" MLTS b) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)


def test_SCR_COMPLEX_10():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS("x") ''')
        b = parse(r''' "Conjugate[x]" ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

        
        a = parse(r''' CONJS("I") ''')
        b = parse(r''' "-I" ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)


def test_SCR_COMPLEX_11():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(DELTA("x", "y")) ''')
        b = parse(r''' DELTA("x", "y") ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)


def test_SCR_COMPLEX_12():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(a ADDS b) ''')
        b = parse(r''' CONJS(a) ADDS CONJS(b) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

        a = parse(r''' CONJS("I" ADDS b ADDS "3") ''')
        b = parse(r''' CONJS(b) ADDS "3 - I" ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_COMPLEX_13():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(a MLTS b MLTS c) ''')
        b = parse(r''' CONJS(a) MLTS CONJS(b) MLTS CONJS(c)''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

        a = parse(r''' CONJS("I" MLTS b MLTS "3") ''')
        b = parse(r''' CONJS(b) MLTS "- 3 I" ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_COMPLEX_14():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(CONJS(a)) ''')
        b = parse(r''' a ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

        a = parse(r''' CONJS(CONJS(CONJS(CONJS(CONJS(a))))) ''')
        b = parse(r''' CONJS(a) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_COMPLEX_15():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(B DOT K) ''')
        b = parse(r''' ADJB(K) DOT ADJK(B) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_DOT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ZEROB DOT K ''')
        b = parse(r''' "0" ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_DOT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B DOT ZEROK ''')
        b = parse(r''' "0" ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_DOT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S SCRB B) DOT K ''')
        b = parse(r''' S MLTS (B DOT K) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_DOT_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B DOT (S SCRK K)''')
        b = parse(r''' S MLTS (B DOT K) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_DOT_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B1 ADDB B2 ADDB B3) DOT K''')
        b = parse(r''' (B1 DOT K) ADDS (B2 DOT K) ADDS (B3 DOT K) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_DOT_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B DOT (K1 ADDK K2 ADDK K3)''')
        b = parse(r''' (B DOT K1) ADDS (B DOT K2) ADDS (B DOT K3) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_DOT_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (BRA(s) DOT KET(t)) ''')
        b = parse(r''' DELTA(s, t) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

        a = parse(r''' (BRA("0") DOT KET("1")) ''')
        b = parse(r''' DELTA("1", "0") ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_DOT_8():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B1 TSRB B2) DOT KET(t) ''')
        b = parse(r''' (B1 DOT KET(FST(t))) MLTS (B2 DOT KET(SND(t))) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_DOT_9():
    with wolfram_backend.wolfram_session():
        a = parse(r''' BRA(s) DOT (K1 TSRK K2) ''')
        b = parse(r''' (BRA(FST(s)) DOT K1) MLTS (BRA(SND(s)) DOT K2) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_DOT_10():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B1 TSRB B2) DOT (K1 TSRK K2) ''')
        b = parse(r''' (B1 DOT K1) MLTS (B2 DOT K2) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_SORT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B MLTB O) DOT K ''')
        b = parse(r''' B DOT (O MLTK K) ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_SORT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' BRA(s) DOT ((O1 TSRO O2) MLTK K0) ''')
        b = parse(r''' ((BRA(FST(s)) MLTB O1) TSRB (BRA(SND(s)) MLTB O2)) DOT K0 ''')
        assert diractrs.normalize(a) == diractrs.normalize(b)

def test_SCR_SORT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B1 TSRB B2) DOT ((O1 TSRO O2) MLTK K0) ''')
        b = parse(r''' ((B1 MLTB O1) TSRB (B2 MLTB O2)) DOT K0''')
        assert diractrs.normalize(a) == diractrs.normalize(b)