

from diracdec import *

from diracdec import dirac_parse as parse, dirac_trs as trs

def test_ATOMIC_BASE():
    with wolfram_backend.wolfram_session():
        a = parse(''' 'HoldForm[Sum[(1/2)^i, {i,1,Infinity}] a + a]' ''')
        b = parse(''' '2 a' ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_COP_SCALAR():
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



def test_SCR_COP_9():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a MLTS (b ADDS c) ''')
        b = parse(r''' (a MLTS b) ADDS (a MLTS c) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' "x" MLTS ((a MLTS "2.2") ADDS ("3.2" MLTS b)) ''')
        b = parse(r''' ("x" MLTS a MLTS "2.2") ADDS ("x" MLTS "3.2" MLTS b) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SCR_COP_10():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS("x") ''')
        b = parse(r''' "Conjugate[x]" ''')
        assert trs.normalize(a) == trs.normalize(b)

        
        a = parse(r''' CONJS("I") ''')
        b = parse(r''' "-I" ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SCR_COP_11():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(DELTA("x", "y")) ''')
        b = parse(r''' DELTA("x", "y") ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SCR_COP_12():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(a ADDS b) ''')
        b = parse(r''' CONJS(a) ADDS CONJS(b) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' CONJS("I" ADDS b ADDS "3") ''')
        b = parse(r''' CONJS(b) ADDS "3 - I" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_COP_13():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(a MLTS b MLTS c) ''')
        b = parse(r''' CONJS(a) MLTS CONJS(b) MLTS CONJS(c)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' CONJS("I" MLTS b MLTS "3") ''')
        b = parse(r''' CONJS(b) MLTS "- 3 I" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_COP_14():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(CONJS(a)) ''')
        b = parse(r''' a ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' CONJS(CONJS(CONJS(CONJS(CONJS(a))))) ''')
        b = parse(r''' CONJS(a) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_COP_15():
    with wolfram_backend.wolfram_session():
        a = parse(r''' CONJS(B DOT K) ''')
        b = parse(r''' ADJ(K) DOT ADJ(B) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X DOT K ''')
        b = parse(r''' "0" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B DOT 0X ''')
        b = parse(r''' "0" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S SCR B) DOT K ''')
        b = parse(r''' S MLTS (B DOT K) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B DOT (S SCR K)''')
        b = parse(r''' S MLTS (B DOT K) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B1 ADD B2 ADD B3) DOT K''')
        b = parse(r''' (B1 DOT K) ADDS (B2 DOT K) ADDS (B3 DOT K) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_DOT_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B DOT (K1 ADD K2 ADD K3)''')
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

#######################################################
# for unified symbols


def test_ADJ_UNI_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(0X) ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_UNI_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(ADJ(X))''')
        b = parse(r''' X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_UNI_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(S0 SCR X0)''')
        b = parse(r''' CONJS(S0) SCR ADJ(X0) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_ADJ_UNI_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(X1 ADD X2 ADD X3) ''')
        b = parse(r''' ADJ(X1) ADD ADJ(X2) ADD ADJ(X3)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_ADJ_KET_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(BRA(s)) ''')
        b = parse(r''' KET(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' ADJ(BRA('1 + 1')) ''')
        b = parse(r''' KET('2') ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_KET_2():
    with wolfram_backend.wolfram_session():
        a = parse(r'''ADJ(B MLTB O)''')
        b = parse(r'''ADJ(O) MLTK ADJ(B)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_KET_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(B1 TSRB B2) ''')
        b = parse(r''' ADJ(B1) TSRK ADJ(B2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_BRA_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(KET(s)) ''')
        b = parse(r''' BRA(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' ADJ(KET('1 + 1')) ''')
        b = parse(r''' BRA('2') ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_BRA_2():
    with wolfram_backend.wolfram_session():
        a = parse(r'''ADJ(O MLTK K)''')
        b = parse(r'''ADJ(K) MLTB ADJ(O)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_BRA_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(K1 TSRK K2) ''')
        b = parse(r''' ADJ(K1) TSRB ADJ(K2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_OPT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(1O) ''')
        b = parse(r''' 1O ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_OPT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(K0 OUTER B0) ''')
        b = parse(r''' ADJ(B0) OUTER ADJ(K0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_OPT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r'''ADJ(O1 MLTO O2)''')
        b = parse(r'''ADJ(O2) MLTO ADJ(O1)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADJ_OPT_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(O1 TSRO O2) ''')
        b = parse(r''' ADJ(O1) TSRO ADJ(O2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' "0" SCR X0 ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' "1" SCR X0 ''')
        b = parse(r''' X0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a SCR 0X ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' a SCR (b SCR X) ''')
        b = parse(r''' (a MLTS b) SCR X ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' "a" SCR ("b" SCR X) ''')
        b = parse(r''' "a b" SCR X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SCR_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S0 SCR (X1 ADD X2 ADD X3) ''')
        b = parse(r''' (S0 SCR X1) ADD (S0 SCR X2) ADD (S0 SCR X3) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADD_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X ADD X ADD 0X ''')
        b = parse(r''' X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADD_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' X ADD X ''')
        b = parse(r''' "2" SCR X ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' K ADD K ADD K ''')
        b = parse(r''' "3" SCR K''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADD_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S0 SCR K0) ADD K0 ''')
        b = parse(r''' (S0 ADDS "1") SCR K0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_ADD_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S1 SCR K0) ADD (S2 SCR K0) ''')
        b = parse(r''' (S1 ADDS S2) SCR K0 ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' (S0 SCR K0) ADD (S0 SCR K0) ''')
        b = parse(r''' (S0 MLTS "2") SCR K0 ''')
        assert trs.normalize(a) == trs.normalize(b)

#######################################################
# for ket

def test_KET_MLT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X MLTK K ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O MLTK 0X ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 1O MLTK K0 ''')
        b = parse(r''' K0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(S0 SCR O0) MLTK K0''')
        b = parse(r'''S0 SCR (O0 MLTK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''O0 MLTK (S0 SCR K0)''')
        b = parse(r'''S0 SCR (O0 MLTK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(O1 ADD O2 ADD O3) MLTK K0''')
        b = parse(r'''(O1 MLTK K0) ADD (O2 MLTK K0) ADD (O3 MLTK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''O0 MLTK (K1 ADD K2 ADD K3)''')
        b = parse(r'''(O0 MLTK K1) ADD (O0 MLTK K2) ADD (O0 MLTK K3)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_8():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(K1 OUTER B0) MLTK K2''')
        b = parse(r'''(B0 DOT K2) SCR K1''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_9():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(O1 MLTO O2) MLTK K0''')
        b = parse(r'''O1 MLTK (O2 MLTK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_10():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(O1 TSRO O2) MLTK ((O1p TSRO O2p) MLTK K0)''')
        b = parse(r'''((O1 MLTO O1p) TSRO (O2 MLTO O2p)) MLTK K0''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_11():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(O1 TSRO O2) MLTK KET(t)''')
        b = parse(r'''(O1 MLTK KET(FST(t))) TSRK (O2 MLTK KET(SND(t)))''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_MLT_12():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(O1 TSRO O2) MLTK (K1 TSRK K2)''')
        b = parse(r'''(O1 MLTK K1) TSRK (O2 MLTK K2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X TSRK K ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K TSRK 0X ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' KET(s) TSRK KET(t) ''')
        b = parse(r''' KET(PAIR(s, t)) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(S0 SCR K1) TSRK K2''')
        b = parse(r'''S0 SCR (K1 TSRK K2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''K1 TSRK (S0 SCR K2)''')
        b = parse(r'''S0 SCR (K1 TSRK K2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(K1 ADD K2 ADD K3) TSRK K0''')
        b = parse(r'''(K1 TSRK K0) ADD (K2 TSRK K0) ADD (K3 TSRK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_KET_TSR_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''K1 TSRK (K2 ADD K3 ADD K4)''')
        b = parse(r'''(K1 TSRK K2) ADD (K1 TSRK K3) ADD (K1 TSRK K4)''')
        assert trs.normalize(a) == trs.normalize(b)

#######################################################
# for bra

def test_BRA_MLT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B MLTB 0X ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X MLTB O ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B0 MLTB 1O ''')
        b = parse(r''' B0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B0 MLTB (S0 SCR O0)''')
        b = parse(r'''S0 SCR (B0 MLTB O0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(S0 SCR B0) MLTB O0''')
        b = parse(r'''S0 SCR (B0 MLTB O0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B0 MLTB (O1 ADD O2 ADD O3)''')
        b = parse(r'''(B0 MLTB O1) ADD (B0 MLTB O2) ADD (B0 MLTB O3)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(B1 ADD B2 ADD B3) MLTB O0''')
        b = parse(r'''(B1 MLTB O0) ADD (B2 MLTB O0) ADD (B3 MLTB O0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_8():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B1 MLTB (K1 OUTER B2)''')
        b = parse(r'''(B1 DOT K1) SCR B2''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_9():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B0 MLTB (O1 MLTO O2)''')
        b = parse(r'''(B0 MLTB O1) MLTB O2''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_10():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(B0 MLTB (O1 TSRO O2)) MLTB (O1p TSRO O2p)''')
        b = parse(r'''B0 MLTB ((O1 MLTO O1p) TSRO (O2 MLTO O2p))''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_11():
    with wolfram_backend.wolfram_session():
        a = parse(r'''BRA(t) MLTB (O1 TSRO O2)''')
        b = parse(r'''(BRA(FST(t)) MLTB O1) TSRB (BRA(SND(t)) MLTB O2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_MLT_12():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(B1 TSRB B2) MLTB (O1 TSRO O2)''')
        b = parse(r'''(B1 MLTB O1) TSRB (B2 MLTB O2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X TSRB B ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' B TSRB 0X ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' BRA(s) TSRB BRA(t) ''')
        b = parse(r''' BRA(PAIR(s, t)) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(S0 SCR B1) TSRB B2''')
        b = parse(r'''S0 SCR (B1 TSRB B2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B1 TSRB (S0 SCR B2)''')
        b = parse(r'''S0 SCR (B1 TSRB B2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_6():
    with wolfram_backend.wolfram_session():
        a = parse(r'''(B1 ADD B2 ADD B3) TSRB B0''')
        b = parse(r'''(B1 TSRB B0) ADD (B2 TSRB B0) ADD (B3 TSRB B0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_BRA_TSR_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B1 TSRB (B2 ADD B3 ADD B4)''')
        b = parse(r'''(B1 TSRB B2) ADD (B1 TSRB B3) ADD (B1 TSRB B4)''')
        assert trs.normalize(a) == trs.normalize(b)

#######################################################
# for operator

def test_OPT_OUTER_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X OUTER B0 ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K0 OUTER 0X ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S0 SCR K0) OUTER B0 ''')
        b = parse(r''' S0 SCR (K0 OUTER B0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K0 OUTER (S0 SCR B0) ''')
        b = parse(r''' S0 SCR (K0 OUTER B0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (K1 ADD K2 ADD K3) OUTER B0 ''')
        b = parse(r''' (K1 OUTER B0) ADD (K2 OUTER B0) ADD (K3 OUTER B0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_OUTER_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' K0 OUTER (B1 ADD B2 ADD B3) ''')
        b = parse(r''' (K0 OUTER B1) ADD (K0 OUTER B2) ADD (K0 OUTER B3) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X MLTO O0 ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O0 MLTO 0X ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 1O MLTO O0 ''')
        b = parse(r''' O0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O0 MLTO 1O ''')
        b = parse(r''' O0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (K0 OUTER B0) MLTO O0 ''')
        b = parse(r''' K0 OUTER (B0 MLTB O0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O0 MLTO (K0 OUTER B0) ''')
        b = parse(r''' (O0 MLTK K0) OUTER B0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S0 SCR O1) MLTO O2 ''')
        b = parse(r''' S0 SCR (O1 MLTO O2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_8():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O1 MLTO (S0 SCR O2) ''')
        b = parse(r''' S0 SCR (O1 MLTO O2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_9():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (O1 ADD O2 ADD O3) MLTO O0 ''')
        b = parse(r''' (O1 MLTO O0) ADD (O2 MLTO O0) ADD (O3 MLTO O0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_10():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O0 MLTO (O1 ADD O2 ADD O3) ''')
        b = parse(r''' (O0 MLTO O1) ADD (O0 MLTO O2) ADD (O0 MLTO O3) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_11():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (O1 MLTO O2) MLTO O3 ''')
        b = parse(r''' O1 MLTO (O2 MLTO O3) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_12():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (O1 TSRO O2) MLTO (O1p TSRO O2p) ''')
        b = parse(r''' (O1 MLTO O1p) TSRO (O2 MLTO O2p) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_MLT_13():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (O1 TSRO O2) MLTO ((O1p TSRO O2p) MLTO O0) ''')
        b = parse(r''' ((O1 MLTO O1p) TSRO (O2 MLTO O2p)) MLTO O0 ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X TSRO O ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O TSRO 0X ''')
        b = parse(r''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (K1 OUTER B1) TSRO (K2 OUTER B2) ''')
        b = parse(r''' (K1 TSRK K2) OUTER (B1 TSRB B2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S0 SCR O1) TSRO O2 ''')
        b = parse(r''' S0 SCR (O1 TSRO O2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O1 TSRO (S0 SCR O2) ''')
        b = parse(r''' S0 SCR (O1 TSRO O2) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (O1 ADD O2 ADD O3) TSRO O0 ''')
        b = parse(r''' (O1 TSRO O0) ADD (O2 TSRO O0) ADD (O3 TSRO O0) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_OPT_TSR_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' O1 TSRO (O2 ADD O3 ADD O4) ''')
        b = parse(r''' (O1 TSRO O2) ADD (O1 TSRO O3) ADD (O1 TSRO O4) ''')
        assert trs.normalize(a) == trs.normalize(b)