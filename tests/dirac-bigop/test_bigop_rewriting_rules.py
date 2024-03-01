
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
# sum-distribution
        
def test_SUM_ELIM_1():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, "0") ''')
        b = parse(''' "0" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SUM_ELIM_2():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, 0K) ''')
        b = parse(''' 0K ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, 0B) ''')
        b = parse(''' 0B ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, 0O) ''')
        b = parse(''' 0O ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_ELIM_3():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, DELTA(i, s)) ''')
        b = parse(''' "1" ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, DELTA(i, i)) ''')
        b = parse(''' "1" ''')
        assert trs.normalize(a) != trs.normalize(b)

        a = parse(''' SUM(i, SUM(j, DELTA(i, i))) ''')
        b = parse(''' SUM(j, "1") ''')
        assert trs.normalize(a) != trs.normalize(b)

def test_SUM_ELIM_4():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, DELTA(i, s) MLTS S1 MLTS i) ''')
        b = parse(''' S1 MLTS s ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, DELTA(i, s) MLTS "i - s") ''')
        b = parse(''' "0" ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, DELTA(i, s) MLTS "i - s") ''')
        b = parse(''' "0" ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, SUM(j, DELTA(i, s) MLTS "i - s")) ''')
        b = parse(''' SUM(j, "0") ''')
        assert trs.normalize(a) == trs.normalize(b)



def test_SUM_ELIM_5():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, DELTA(i, s) SCRK KET(i)) ''')
        b = parse(''' KET(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, DELTA(i, s) SCRB BRA(i)) ''')
        b = parse(''' BRA(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, DELTA(i, s) SCRO (KET(i) OUTER BRA(i))) ''')
        b = parse(''' KET(s) OUTER BRA(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, SUM(j, DELTA(i, s) SCRO (KET(i) OUTER BRA(i)))) ''')
        b = parse(''' SUM(j, KET(s) OUTER BRA(s)) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_ELIM_6():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, (DELTA(i, s) MLTS S1 MLTS S2) SCRK KET(i)) ''')
        b = parse(''' (S1 MLTS S2) SCRK KET(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, (DELTA(i, s) MLTS S1 MLTS S2) SCRB BRA(i)) ''')
        b = parse(''' (S1 MLTS S2) SCRB BRA(s) ''')
        assert trs.normalize(a) == trs.normalize(b)
        
        a = parse(''' SUM(i, (DELTA(i, s) MLTS S1 MLTS S2) SCRO (KET(i) OUTER BRA(i))) ''')
        b = parse(''' (S1 MLTS S2) SCRO (KET(s) OUTER BRA(s)) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, SUM(j, (DELTA(i, s) MLTS S1 MLTS S2) SCRO (KET(i) OUTER BRA(i)))) ''')
        b = parse(''' SUM(j, (S1 MLTS S2) SCRO (KET(s) OUTER BRA(s))) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SUM_DIST_1():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, A) MLTS B MLTS C ''')
        b = parse(''' SUM(i, A MLTS B MLTS C) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, A) MLTS B MLTS i ''')
        b = parse(''' SUM(x, A MLTS B MLTS i) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SUM_DIST_2():
    with wolfram_backend.wolfram_session():
        a = parse(''' CONJS(SUM(i, A)) ''')
        b = parse(''' SUM(i, CONJS(A)) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_DIST_3():
    with wolfram_backend.wolfram_session():
        a = parse(''' ADJK(SUM(i, A)) ''')
        b = parse(''' SUM(i, ADJK(A)) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' ADJB(SUM(i, A)) ''')
        b = parse(''' SUM(i, ADJB(A)) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' ADJO(SUM(i, A)) ''')
        b = parse(''' SUM(i, ADJO(A)) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_DIST_4():
    with wolfram_backend.wolfram_session():
        a = parse(''' TRANK(SUM(i, A)) ''')
        b = parse(''' SUM(i, TRANK(A)) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' TRANB(SUM(i, A)) ''')
        b = parse(''' SUM(i, TRANB(A)) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' TRANO(SUM(i, A)) ''')
        b = parse(''' SUM(i, TRANO(A)) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SUM_DIST_5():
    with wolfram_backend.wolfram_session():
        a = parse(''' S0 SCRK SUM(i, A) ''')
        b = parse(''' SUM(i, S0 SCRK A) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' S0 SCRB SUM(i, A) ''')
        b = parse(''' SUM(i, S0 SCRB A) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' S0 SCRO SUM(i, A) ''')
        b = parse(''' SUM(i, S0 SCRO A) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_DIST_6():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, S0) SCRK X ''')
        b = parse(''' SUM(i, S0 SCRK X) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, S0) SCRB X ''')
        b = parse(''' SUM(i, S0 SCRB X) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, S0) SCRO X ''')
        b = parse(''' SUM(i, S0 SCRO X) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SUM_DIST_7():
    with wolfram_backend.wolfram_session():
        a = parse(r'''SUM(x, B0) DOT K0''')
        b = parse(r'''SUM(x, B0 DOT K0)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''SUM(x, O0) MLTK K0''')
        b = parse(r'''SUM(x, O0 MLTK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''SUM(x, B0) MLTB O0''')
        b = parse(r'''SUM(x, B0 MLTB O0)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''SUM(x, O1) MLTO O2''')
        b = parse(r'''SUM(x, O1 MLTO O2)''')
        assert trs.normalize(a) == trs.normalize(b)

        # check variable renaming
        a = parse(r'''SUM(x, B0) DOT x''')
        b = parse(r'''SUM(y, B0 DOT x)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_DIST_8():
    with wolfram_backend.wolfram_session():
        a = parse(r'''B0 DOT SUM(x, K0)''')
        b = parse(r'''SUM(x, B0 DOT K0)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''O0 MLTK SUM(x, K0)''')
        b = parse(r'''SUM(x, O0 MLTK K0)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''B0 MLTB SUM(x, O0)''')
        b = parse(r'''SUM(x, B0 MLTB O0)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''O1 MLTO SUM(x, O2)''')
        b = parse(r'''SUM(x, O1 MLTO O2)''')
        assert trs.normalize(a) == trs.normalize(b)

        # check variable renaming
        a = parse(r'''x DOT SUM(x, K0)''')
        b = parse(r'''SUM(y, x DOT K0)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_DIST_9():
    with wolfram_backend.wolfram_session():
        a = parse(r'''SUM(x, K1) TSRK K2''')
        b = parse(r'''SUM(x, K1 TSRK K2)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''SUM(x, B1) TSRB B2''')
        b = parse(r'''SUM(x, B1 TSRB B2)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''SUM(x, K0) OUTER B0''')
        b = parse(r'''SUM(x, K0 OUTER B0)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''SUM(x, O1) MLTO O2''')
        b = parse(r'''SUM(x, O1 MLTO O2)''')
        assert trs.normalize(a) == trs.normalize(b)

        # check variable renaming
        a = parse(r'''SUM(x, K0) TSRK x''')
        b = parse(r'''SUM(y, K0 TSRK x)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_DIST_10():
    with wolfram_backend.wolfram_session():
        a = parse(r'''K1 TSRK SUM(x, K2)''')
        b = parse(r'''SUM(x, K1 TSRK K2)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''B1 TSRB SUM(x, B2)''')
        b = parse(r'''SUM(x, B1 TSRB B2)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''K0 OUTER SUM(x, B0)''')
        b = parse(r'''SUM(x, K0 OUTER B0)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''O1 TSRO SUM(x, O2)''')
        b = parse(r'''SUM(x, O1 TSRO O2)''')
        assert trs.normalize(a) == trs.normalize(b)

        # check variable renaming
        a = parse(r'''x TSRK SUM(x, K0)''')
        b = parse(r'''SUM(y, x TSRK K0)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_ADD_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''SUM(i, A) ADDS SUM(j, B) ADDS S0''')
        b = parse(r'''SUM(i, A ADDS B) ADDS S0''')
        assert trs.normalize(a) == trs.normalize(b)
        
        a = parse(r'''SUM(i, A) ADDK SUM(j, B) ADDK K0''')
        b = parse(r'''SUM(i, A ADDK B) ADDK K0''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''SUM(i, A) ADDB SUM(j, B) ADDB B0''')
        b = parse(r'''SUM(i, A ADDB B) ADDB B0''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''SUM(i, A) ADDO SUM(j, B) ADDO O0''')
        b = parse(r'''SUM(i, A ADDO B) ADDO O0''')
        assert trs.normalize(a) == trs.normalize(b)

        # check variable renaming
        a = parse(r'''SUM(i, A) ADDS SUM(j, B) ADDS S0 ADDS SUM(k, i)''')
        b = parse(r'''SUM(z, A ADDS B ADDS i) ADDS S0''')
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


###########################################################
# 2-section rewriting to deal with DOT equational theory
        
def test_juxt_rewrite():
    with wolfram_backend.wolfram_session():
        a = parse(''' B0 DOT K0 ''')
        b = parse(''' TRANB(K0) DOT TRANK(B0) ''')
        a_ = trs.normalize(juxt(trs.normalize(a)))
        b_ = trs.normalize(juxt(trs.normalize(b)))
        assert a_ == b_

        a = parse(''' BRA('0') DOT (A MLTK KET('1')) ''')
        b = parse(''' BRA('1') DOT (TRANO(A) MLTK KET('0')) ''')
        a_ = trs.normalize(juxt(trs.normalize(a)))
        b_ = trs.normalize(juxt(trs.normalize(b)))
        assert a_ == b_

        a = parse(''' B1 DOT ((O1 MLTO TRANO(O2)) MLTK TRANK(B2)) ''')
        b = parse(''' B2 DOT ((O2 MLTO TRANO(O1)) MLTK TRANK(B1)) ''')
        a_ = trs.normalize(juxt(trs.normalize(a)))
        b_ = trs.normalize(juxt(trs.normalize(b)))
        assert a_ == b_

def test_sumeq_rewrite():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(a, SUM(b, "a / b")) ''')
        b = parse(''' SUM(b, SUM(a, "a / b")) ''')

        assert not a == b

        a_ = sumeq(trs.normalize(a))
        b_ = sumeq(trs.normalize(b))

        assert a_ == b_

#############################################################
# other tests
        
def test_sum_elim_delta_with_sum_swap():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(a, SUM(b, DELTA(a, x) SCRK KET(PAIR(a, b)))) ''')
        b = parse(''' SUM(b, KET(PAIR(x, b))) ''')
        assert trs.normalize(a) == trs.normalize(b)
