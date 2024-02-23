

from diracdec import *

from diracdec import dirac_parse as parse, dirac_trs as trs

def test_ATOMIC_BASE():
    with wolfram_backend.wolfram_session():
        a = parse(''' 'HoldForm[Sum[(1/2)^i, {i,1,Infinity}] a + a]' ''')
        b = parse(''' '2 a' ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_COMPLEX_SCALAR():
    with wolfram_backend.wolfram_session():
        a = parse(''' "HoldForm[Sum[(1/2)^i, {i,1,Infinity}] a + a]" ''')
        b = parse(''' "2 a" ''')
        assert trs.normalize(a) == trs.normalize(b)




def test_BASIS_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' FST(PAIR('x', 't')) ''')
        b = parse(r''' 'x' ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' FST(PAIR(PAIR(x, y), 't')) ''')
        b = parse(r''' PAIR(x, y) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BASIS_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SND(PAIR('x', 't')) ''')
        b = parse(r''' 't' ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' SND(PAIR(PAIR(x, y), 't')) ''')
        b = parse(r''' 't' ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BASIS_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' PAIR(FST(p), SND(p)) ''')
        b = parse(r''' p ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_DELTA_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' DELTA(u, PAIR(s, t)) ''')
        b = parse(r''' DELTA(FST(u), s) MLTS DELTA(SND(u), t) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_DELTA_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' DELTA(FST(u), FST(v)) MLTS DELTA(SND(u), SND(v)) ''')
        b = parse(r''' DELTA(u, v) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' DELTA(FST(u), FST(v)) MLTS DELTA(SND(u), SND(v)) MLTS "2" ''')
        b = parse(r''' DELTA(u, v) MLTS "2" ''')
        assert trs.normalize(a) == trs.normalize(b)



def test_SCR_COMPLEX_9():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a MLTS (b ADDS c) ''')
        b = parse(r''' (a MLTS b) ADDS (a MLTS c) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' "x" MLTS ((a MLTS "2.2") ADDS ("3.2" MLTS b)) ''')
        b = parse(r''' ("x" MLTS a MLTS "2.2") ADDS ("x" MLTS "3.2" MLTS b) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SCR_COMPLEX_10():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS("x") ''')
        b = parse(r''' "Conjugate[x]" ''')
        assert trs.normalize(a) == trs.normalize(b)

        
        a = parse(r''' CONJS("I") ''')
        b = parse(r''' "-I" ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SCR_COMPLEX_11():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(DELTA("x", "y")) ''')
        b = parse(r''' DELTA("x", "y") ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SCR_COMPLEX_12():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(a ADDS b) ''')
        b = parse(r''' CONJS(a) ADDS CONJS(b) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' CONJS("I" ADDS b ADDS "3") ''')
        b = parse(r''' CONJS(b) ADDS "3 - I" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_COMPLEX_13():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(a MLTS b MLTS c) ''')
        b = parse(r''' CONJS(a) MLTS CONJS(b) MLTS CONJS(c)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' CONJS("I" MLTS b MLTS "3") ''')
        b = parse(r''' CONJS(b) MLTS "- 3 I" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_COMPLEX_14():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(CONJS(a)) ''')
        b = parse(r''' a ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' CONJS(CONJS(CONJS(CONJS(CONJS(a))))) ''')
        b = parse(r''' CONJS(a) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_COMPLEX_15():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(B DOT K) ''')
        b = parse(r''' ADJB(K) DOT ADJK(B) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0B DOT K ''')
        b = parse(r''' "0" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B DOT 0K ''')
        b = parse(r''' "0" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S SCRB B) DOT K ''')
        b = parse(r''' S MLTS (B DOT K) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B DOT (S SCRK K)''')
        b = parse(r''' S MLTS (B DOT K) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B1 ADDB B2 ADDB B3) DOT K''')
        b = parse(r''' (B1 DOT K) ADDS (B2 DOT K) ADDS (B3 DOT K) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B DOT (K1 ADDK K2 ADDK K3)''')
        b = parse(r''' (B DOT K1) ADDS (B DOT K2) ADDS (B DOT K3) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (BRA(s) DOT KET(t)) ''')
        b = parse(r''' DELTA(s, t) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' (BRA("0") DOT KET("1")) ''')
        b = parse(r''' DELTA("1", "0") ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_8():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B1 TSRB B2) DOT KET(t) ''')
        b = parse(r''' (B1 DOT KET(FST(t))) MLTS (B2 DOT KET(SND(t))) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_9():
    with wolfram_backend.wolfram_session():
        a = parse(r''' BRA(s) DOT (K1 TSRK K2) ''')
        b = parse(r''' (BRA(FST(s)) DOT K1) MLTS (BRA(SND(s)) DOT K2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_10():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B1 TSRB B2) DOT (K1 TSRK K2) ''')
        b = parse(r''' (B1 DOT K1) MLTS (B2 DOT K2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_SORT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B MLTB O) DOT K ''')
        b = parse(r''' B DOT (O MLTK K) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_SORT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' BRA(s) DOT ((O1 TSRO O2) MLTK K0) ''')
        b = parse(r''' ((BRA(FST(s)) MLTB O1) TSRB (BRA(SND(s)) MLTB O2)) DOT K0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_SORT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B1 TSRB B2) DOT ((O1 TSRO O2) MLTK K0) ''')
        b = parse(r''' ((B1 MLTB O1) TSRB (B2 MLTB O2)) DOT K0''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADJ_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJK(0B) ''')
        b = parse(r''' 0K ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADJ_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJK(BRA(s)) ''')
        b = parse(r''' KET(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' ADJK(BRA('1 + 1')) ''')
        b = parse(r''' KET('2') ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADJ_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJK(ADJB(K))''')
        b = parse(r''' K ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADJ_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJK(S0 SCRB B0)''')
        b = parse(r''' CONJS(S0) SCRK ADJK(B0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADJ_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJK(B1 ADDB B2 ADDB B3) ''')
        b = parse(r''' ADJK(B1) ADDK ADJK(B2) ADDK ADJK(B3)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADJ_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''ADJK(B MLTB O)''')
        b = parse(r'''ADJO(O) MLTK ADJK(B)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADJ_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJK(B1 TSRB B2) ''')
        b = parse(r''' ADJK(B1) TSRK ADJK(B2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_SCAL_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' "0" SCRK K0 ''')
        b = parse(r''' 0K ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_SCAL_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' "1" SCRK K0 ''')
        b = parse(r''' K0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_SCAL_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a SCRK 0K ''')
        b = parse(r''' 0K ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_SCAL_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a SCRK (b SCRK K) ''')
        b = parse(r''' (a MLTS b) SCRK K ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' "a" SCRK ("b" SCRK K) ''')
        b = parse(r''' "a b" SCRK K ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_SCAL_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S0 SCRK (K1 ADDK K2 ADDK K3) ''')
        b = parse(r''' (S0 SCRK K1) ADDK (S0 SCRK K2) ADDK (S0 SCRK K3) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADD_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0K ADDK K ADDK 0K ''')
        b = parse(r''' K ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADD_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K ADDK K ''')
        b = parse(r''' "2" SCRK K ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' K ADDK K ADDK K ''')
        b = parse(r''' "3" SCRK K''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADD_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S0 SCRK K0) ADDK K0 ''')
        b = parse(r''' (S0 ADDS "1") SCRK K0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_ADD_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S1 SCRK K0) ADDK (S2 SCRK K0) ''')
        b = parse(r''' (S1 ADDS S2) SCRK K0 ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' (S0 SCRK K0) ADDK (S0 SCRK K0) ''')
        b = parse(r''' (S0 MLTS "2") SCRK K0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0O MLTK K ''')
        b = parse(r''' 0K ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O MLTK 0K ''')
        b = parse(r''' 0K ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 1O MLTK K0 ''')
        b = parse(r''' K0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(S0 SCRO O0) MLTK K0''')
        b = parse(r'''S0 SCRK (O0 MLTK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''O0 MLTK (S0 SCRK K0)''')
        b = parse(r'''S0 SCRK (O0 MLTK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(O1 ADDO O2 ADDO O3) MLTK K0''')
        b = parse(r'''(O1 MLTK K0) ADDK (O2 MLTK K0) ADDK (O3 MLTK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''O0 MLTK (K1 ADDK K2 ADDK K3)''')
        b = parse(r'''(O0 MLTK K1) ADDK (O0 MLTK K2) ADDK (O0 MLTK K3)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_8():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(K1 OUTER B0) MLTK K2''')
        b = parse(r'''(B0 DOT K2) SCRK K1''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_9():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(O1 MLTO O2) MLTK K0''')
        b = parse(r'''O1 MLTK (O2 MLTK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_10():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(O1 TSRO O2) MLTK ((O1p TSRO O2p) MLTK K0)''')
        b = parse(r'''((O1 MLTO O1p) TSRO (O2 MLTO O2p)) MLTK K0''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_11():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(O1 TSRO O2) MLTK KET(t)''')
        b = parse(r'''(O1 MLTK KET(FST(t))) TSRK (O2 MLTK KET(SND(t)))''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MUL_12():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(O1 TSRO O2) MLTK (K1 TSRK K2)''')
        b = parse(r'''(O1 MLTK K1) TSRK (O2 MLTK K2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0K TSRK K ''')
        b = parse(r''' 0K ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K TSRK 0K ''')
        b = parse(r''' 0K ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' KET(s) TSRK KET(t) ''')
        b = parse(r''' KET(PAIR(s, t)) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(S0 SCRK K1) TSRK K2''')
        b = parse(r'''S0 SCRK (K1 TSRK K2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''K1 TSRK (S0 SCRK K2)''')
        b = parse(r'''S0 SCRK (K1 TSRK K2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(K1 ADDK K2 ADDK K3) TSRK K0''')
        b = parse(r'''(K1 TSRK K0) ADDK (K2 TSRK K0) ADDK (K3 TSRK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''K1 TSRK (K2 ADDK K3 ADDK K4)''')
        b = parse(r'''(K1 TSRK K2) ADDK (K1 TSRK K3) ADDK (K1 TSRK K4)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_BRA_ADJ_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJB(0K) ''')
        b = parse(r''' 0B ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_ADJ_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJB(KET(s)) ''')
        b = parse(r''' BRA(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' ADJB(KET('1 + 1')) ''')
        b = parse(r''' BRA('2') ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_ADJ_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJB(ADJK(B))''')
        b = parse(r''' B ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_ADJ_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJB(S0 SCRK K0)''')
        b = parse(r''' CONJS(S0) SCRB ADJB(K0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_ADJ_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJB(K1 ADDK K2 ADDK K3) ''')
        b = parse(r''' ADJB(K1) ADDB ADJB(K2) ADDB ADJB(K3)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_ADJ_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''ADJB(O MLTK K)''')
        b = parse(r'''ADJB(K) MLTB ADJO(O)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_ADJ_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJB(K1 TSRK K2) ''')
        b = parse(r''' ADJB(K1) TSRB ADJB(K2) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_BRA_SCAL_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' "0" SCRB B0 ''')
        b = parse(r''' 0B ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_SCAL_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' "1" SCRB B0 ''')
        b = parse(r''' B0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_SCAL_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a SCRB 0B ''')
        b = parse(r''' 0B ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_SCAL_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a SCRB (b SCRB B) ''')
        b = parse(r''' (a MLTS b) SCRB B ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' "a" SCRB ("b" SCRB B) ''')
        b = parse(r''' "a b" SCRB B ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_SCAL_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S0 SCRB (B1 ADDB B2 ADDB B3) ''')
        b = parse(r''' (S0 SCRB B1) ADDB (S0 SCRB B2) ADDB (S0 SCRB B3) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_BRA_ADD_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0B ADDB B ADDB 0B ''')
        b = parse(r''' B ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_ADD_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B ADDB B ''')
        b = parse(r''' "2" SCRB B ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' B ADDB B ADDB B ''')
        b = parse(r''' "3" SCRB B''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_ADD_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S0 SCRB B0) ADDB B0 ''')
        b = parse(r''' (S0 ADDS "1") SCRB B0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_ADD_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S1 SCRB B0) ADDB (S2 SCRB B0) ''')
        b = parse(r''' (S1 ADDS S2) SCRB B0 ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' (S0 SCRB B0) ADDB (S0 SCRB B0) ''')
        b = parse(r''' (S0 MLTS "2") SCRB B0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B MLTB 0O ''')
        b = parse(r''' 0B ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0B MLTB O ''')
        b = parse(r''' 0B ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B0 MLTB 1O ''')
        b = parse(r''' B0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B0 MLTB (S0 SCRO O0)''')
        b = parse(r'''S0 SCRB (B0 MLTB O0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(S0 SCRB B0) MLTB O0''')
        b = parse(r'''S0 SCRB (B0 MLTB O0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B0 MLTB (O1 ADDO O2 ADDO O3)''')
        b = parse(r'''(B0 MLTB O1) ADDB (B0 MLTB O2) ADDB (B0 MLTB O3)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(B1 ADDB B2 ADDB B3) MLTB O0''')
        b = parse(r'''(B1 MLTB O0) ADDB (B2 MLTB O0) ADDB (B3 MLTB O0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_8():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B1 MLTB (K1 OUTER B2)''')
        b = parse(r'''(B1 DOT K1) SCRB B2''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_9():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B0 MLTB (O1 MLTO O2)''')
        b = parse(r'''(B0 MLTB O1) MLTB O2''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_10():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(B0 MLTB (O1 TSRO O2)) MLTB (O1p TSRO O2p)''')
        b = parse(r'''B0 MLTB ((O1 MLTO O1p) TSRO (O2 MLTO O2p))''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_11():
    with wolfram_backend.wolfram_session():
        a = parse(r'''BRA(t) MLTB (O1 TSRO O2)''')
        b = parse(r'''(BRA(FST(t)) MLTB O1) TSRB (BRA(SND(t)) MLTB O2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MUL_12():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(B1 TSRB B2) MLTB (O1 TSRO O2)''')
        b = parse(r'''(B1 MLTB O1) TSRB (B2 MLTB O2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0B TSRB B ''')
        b = parse(r''' 0B ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B TSRB 0B ''')
        b = parse(r''' 0B ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' BRA(s) TSRB BRA(t) ''')
        b = parse(r''' BRA(PAIR(s, t)) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(S0 SCRB B1) TSRB B2''')
        b = parse(r'''S0 SCRB (B1 TSRB B2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B1 TSRB (S0 SCRB B2)''')
        b = parse(r'''S0 SCRB (B1 TSRB B2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(B1 ADDB B2 ADDB B3) TSRB B0''')
        b = parse(r'''(B1 TSRB B0) ADDB (B2 TSRB B0) ADDB (B3 TSRB B0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B1 TSRB (B2 ADDB B3 ADDB B4)''')
        b = parse(r'''(B1 TSRB B2) ADDB (B1 TSRB B3) ADDB (B1 TSRB B4)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0K OUTER B0 ''')
        b = parse(r''' 0O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K0 OUTER 0B ''')
        b = parse(r''' 0O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S0 SCRK K0) OUTER B0 ''')
        b = parse(r''' S0 SCRO (K0 OUTER B0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K0 OUTER (S0 SCRB B0) ''')
        b = parse(r''' S0 SCRO (K0 OUTER B0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (K1 ADDK K2 ADDK K3) OUTER B0 ''')
        b = parse(r''' (K1 OUTER B0) ADDO (K2 OUTER B0) ADDO (K3 OUTER B0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K0 OUTER (B1 ADDB B2 ADDB B3) ''')
        b = parse(r''' (K0 OUTER B1) ADDO (K0 OUTER B2) ADDO (K0 OUTER B3) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADJ_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJO(0O) ''')
        b = parse(r''' 0O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADJ_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJO(1O) ''')
        b = parse(r''' 1O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADJ_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJO(K0 OUTER B0) ''')
        b = parse(r''' ADJK(B0) OUTER ADJB(K0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADJ_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJO(ADJO(O0)) ''')
        b = parse(r''' O0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADJ_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''ADJO(S0 SCRO O0)''')
        b = parse(r'''CONJS(S0) SCRO ADJO(O0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADJ_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJO(O1 ADDO O2 ADDO O3) ''')
        b = parse(r''' ADJO(O1) ADDO ADJO(O2) ADDO ADJO(O3)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADJ_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''ADJO(O1 MLTO O2)''')
        b = parse(r'''ADJO(O2) MLTO ADJO(O1)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADJ_8():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJO(O1 TSRO O2) ''')
        b = parse(r''' ADJO(O1) TSRO ADJO(O2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_SCAL_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' "0" SCRO O0 ''')
        b = parse(r''' 0O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_SCAL_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' "1" SCRO O0 ''')
        b = parse(r''' O0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_SCAL_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a SCRO 0O ''')
        b = parse(r''' 0O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_SCAL_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a SCRO (b SCRO O) ''')
        b = parse(r''' (a MLTS b) SCRO O ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' "a" SCRO ("b" SCRO O) ''')
        b = parse(r''' "a b" SCRO O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_SCAL_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S0 SCRO (O1 ADDO O2 ADDO O3) ''')
        b = parse(r''' (S0 SCRO O1) ADDO (S0 SCRO O2) ADDO (S0 SCRO O3) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADD_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0O ADDO O ADDO 0O ''')
        b = parse(r''' O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADD_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O ADDO O ''')
        b = parse(r''' "2" SCRO O''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADD_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S0 SCRO O0) ADDO O0 ''')
        b = parse(r''' (S0 ADDS "1") SCRO O0 ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' ("a-1" SCRO O0) ADDO O0 ''')
        b = parse(r''' "a" SCRO O0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_ADD_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(S1 SCRO O0) ADDO (S2 SCRO O0)''')
        b = parse(r'''(S1 ADDS S2) SCRO O0''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0O MLTO O0 ''')
        b = parse(r''' 0O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O0 MLTO 0O ''')
        b = parse(r''' 0O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 1O MLTO O0 ''')
        b = parse(r''' O0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O0 MLTO 1O ''')
        b = parse(r''' O0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (K0 OUTER B0) MLTO O0 ''')
        b = parse(r''' K0 OUTER (B0 MLTB O0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O0 MLTO (K0 OUTER B0) ''')
        b = parse(r''' (O0 MLTK K0) OUTER B0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S0 SCRO O1) MLTO O2 ''')
        b = parse(r''' S0 SCRO (O1 MLTO O2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_8():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O1 MLTO (S0 SCRO O2) ''')
        b = parse(r''' S0 SCRO (O1 MLTO O2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_9():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (O1 ADDO O2 ADDO O3) MLTO O0 ''')
        b = parse(r''' (O1 MLTO O0) ADDO (O2 MLTO O0) ADDO (O3 MLTO O0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_10():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O0 MLTO (O1 ADDO O2 ADDO O3) ''')
        b = parse(r''' (O0 MLTO O1) ADDO (O0 MLTO O2) ADDO (O0 MLTO O3) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_11():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (O1 MLTO O2) MLTO O3 ''')
        b = parse(r''' O1 MLTO (O2 MLTO O3) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_12():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (O1 TSRO O2) MLTO (O1p TSRO O2p) ''')
        b = parse(r''' (O1 MLTO O1p) TSRO (O2 MLTO O2p) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MUL_13():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (O1 TSRO O2) MLTO ((O1p TSRO O2p) MLTO O0) ''')
        b = parse(r''' ((O1 MLTO O1p) TSRO (O2 MLTO O2p)) MLTO O0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0O TSRO O ''')
        b = parse(r''' 0O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O TSRO 0O ''')
        b = parse(r''' 0O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (K1 OUTER B1) TSRO (K2 OUTER B2) ''')
        b = parse(r''' (K1 TSRK K2) OUTER (B1 TSRB B2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S0 SCRO O1) TSRO O2 ''')
        b = parse(r''' S0 SCRO (O1 TSRO O2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O1 TSRO (S0 SCRO O2) ''')
        b = parse(r''' S0 SCRO (O1 TSRO O2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (O1 ADDO O2 ADDO O3) TSRO O0 ''')
        b = parse(r''' (O1 TSRO O0) ADDO (O2 TSRO O0) ADDO (O3 TSRO O0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O1 TSRO (O2 ADDO O3 ADDO O4) ''')
        b = parse(r''' (O1 TSRO O2) ADDO (O1 TSRO O3) ADDO (O1 TSRO O4) ''')
        assert trs.normalize(a) == trs.normalize(b)