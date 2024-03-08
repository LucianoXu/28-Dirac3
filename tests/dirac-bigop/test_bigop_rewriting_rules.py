
from diracdec import *

from diracdec import dirac_bigop_parse as parse, dirac_bigop_trs as trs

def test_TRANS_UNI_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(0X)''')
        b = parse(r'''0X''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_UNI_2():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(ADJ(X0))''')
        b = parse(r'''ADJ(TP(X0))''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_UNI_3():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(TP(X0))''')
        b = parse(r'''X0''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_UNI_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(S0 SCR X0)''')
        b = parse(r'''S0 SCR TP(X0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_UNI_5():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(X1 ADD X2 ADD X3)''')
        b = parse(r'''TP(X1) ADD TP(X2) ADD TP(X3)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_TRANS_KET_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(BRA(s))''')
        b = parse(r'''KET(s)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''TP(BRA('a - a'))''')
        b = parse(r'''KET('0')''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_KET_2():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(B0 MLTB O0)''')
        b = parse(r'''TP(O0) MLTK TP(B0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_KET_3():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(B1 TSRB B2)''')
        b = parse(r'''TP(B1) TSRK TP(B2)''')
        assert trs.normalize(a) == trs.normalize(b)


def test_TRANS_BRA_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(KET(s))''')
        b = parse(r'''BRA(s)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''TP(KET('a - a'))''')
        b = parse(r'''BRA('0')''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_BRA_2():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(O0 MLTK K0)''')
        b = parse(r'''TP(K0) MLTB TP(O0)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_BRA_3():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(K1 TSRK K2)''')
        b = parse(r'''TP(K1) TSRB TP(K2)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_OPT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(1O)''')
        b = parse(r'''1O''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_OPT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(K0 OUTER B0)''')
        b = parse(r'''TP(B0) OUTER TP(K0)''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r'''TP(KET('s') OUTER BRA('t'))''')
        b = parse(r'''KET('t') OUTER BRA('s')''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_OPT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(O1 MLTO O2)''')
        b = parse(r'''TP(O2) MLTO TP(O1)''')
        assert trs.normalize(a) == trs.normalize(b)

def test_TRANS_OPT_4():
    with wolfram_backend.wolfram_session():
        a = parse(r'''TP(O1 TSRO O2)''')
        b = parse(r'''TP(O1) TSRO TP(O2)''')
        assert trs.normalize(a) == trs.normalize(b)

###########################################################
# sum-distribution
        
def test_SUM_ELIM_1():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUMS(i, "0") ''')
        b = parse(''' "0" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SUM_ELIM_2():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, 0X) ''')
        b = parse(''' 0X ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_ELIM_3():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUMS(i, DELTA(i, s)) ''')
        b = parse(''' "1" ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUMS(i, DELTA(i, i)) ''')
        b = parse(''' "1" ''')
        assert trs.normalize(a) != trs.normalize(b)

        a = parse(''' SUMS(i, SUMS(j, DELTA(i, i))) ''')
        b = parse(''' SUMS(j, "1") ''')
        assert trs.normalize(a) != trs.normalize(b)

def test_SUM_ELIM_4():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUMS(i, DELTA(i, s) MLTS S1 MLTS i) ''')
        b = parse(''' S1 MLTS s ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUMS(i, DELTA(i, s) MLTS "i - s") ''')
        b = parse(''' "0" ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUMS(i, SUMS(j, DELTA(i, s) MLTS "i - s")) ''')
        b = parse(''' SUMS(j, "0") ''')
        assert trs.normalize(a) == trs.normalize(b)



def test_SUM_ELIM_5():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, DELTA(i, s) SCR KET(i)) ''')
        b = parse(''' KET(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, DELTA(i, s) SCR BRA(i)) ''')
        b = parse(''' BRA(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, DELTA(i, s) SCR (KET(i) OUTER BRA(i))) ''')
        b = parse(''' KET(s) OUTER BRA(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, SUM(j, DELTA(i, s) SCR (KET(i) OUTER BRA(i)))) ''')
        b = parse(''' SUM(j, KET(s) OUTER BRA(s)) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_ELIM_6():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, (DELTA(i, s) MLTS S1 MLTS S2) SCR KET(i)) ''')
        b = parse(''' (S1 MLTS S2) SCR KET(s) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, (DELTA(i, s) MLTS S1 MLTS S2) SCR BRA(i)) ''')
        b = parse(''' (S1 MLTS S2) SCR BRA(s) ''')
        assert trs.normalize(a) == trs.normalize(b)
        
        a = parse(''' SUM(i, (DELTA(i, s) MLTS S1 MLTS S2) SCR (KET(i) OUTER BRA(i))) ''')
        b = parse(''' (S1 MLTS S2) SCR (KET(s) OUTER BRA(s)) ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(''' SUM(i, SUM(j, (DELTA(i, s) MLTS S1 MLTS S2) SCR (KET(i) OUTER BRA(i)))) ''')
        b = parse(''' SUM(j, (S1 MLTS S2) SCR (KET(s) OUTER BRA(s))) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SUM_DIST_1():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUMS(i, A) MLTS B MLTS C ''')
        b = parse(''' SUMS(i, A MLTS C MLTS B) ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_SUM_DIST_2():
    with wolfram_backend.wolfram_session():
        a = parse(''' CONJS(SUMS(i, A)) ''')
        b = parse(''' SUMS(i, CONJS(A)) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_DIST_3():
    with wolfram_backend.wolfram_session():
        a = parse(''' ADJ(SUM(i, A)) ''')
        b = parse(''' SUM(i, ADJ(A)) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_DIST_4():
    with wolfram_backend.wolfram_session():
        a = parse(''' TP(SUM(i, A)) ''')
        b = parse(''' SUM(i, TP(A)) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_DIST_5():
    with wolfram_backend.wolfram_session():
        a = parse(''' S0 SCR SUM(i, A) ''')
        b = parse(''' SUM(i, S0 SCR A) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_SUM_DIST_6():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUMS(i, S0) SCR X ''')
        b = parse(''' SUM(i, S0 SCR X) ''')
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
        a = parse(r'''SUMS(i, A) ADDS SUMS(j, B) ADDS S0''')
        b = parse(r'''SUMS(i, A ADDS B) ADDS S0''')
        assert trs.normalize(a) == trs.normalize(b)
        
        a = parse(r'''SUM(i, A) ADD SUM(j, B) ADD K0''')
        b = parse(r'''SUM(i, A ADD B) ADD K0''')
        assert trs.normalize(a) == trs.normalize(b)

        # check variable renaming
        a = parse(r'''SUMS(i, A) ADDS SUMS(j, B) ADDS S0 ADDS SUMS(k, i)''')
        b = parse(r'''SUMS(z, A ADDS B ADDS i) ADDS S0''')
        assert trs.normalize(a) == trs.normalize(b)

##################################
        

def test_SUM_ELIM_7():
    with wolfram_backend.wolfram_session():
        a = parse('''SUM(i, (BRA(i) DOT K0) SCR KET(i))''')
        b = parse('''K0''')
        assert entry_trs.normalize(trs.normalize(a)) == entry_trs.normalize(trs.normalize(b))

def test_SUM_ELIM_8():
    with wolfram_backend.wolfram_session():
        a = parse('''SUM(i, (B0 DOT KET(i)) SCR BRA(i))''')
        b = parse('''B0''')
        assert entry_trs.normalize(trs.normalize(a)) == entry_trs.normalize(trs.normalize(b))

def test_SUM_ELIM_9():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, SUM(j, (BRA(i) DOT (A MLTK KET(j))) SCR (KET(i) OUTER BRA(j)) )) ''')
        b = parse('''A''')
        assert entry_trs.normalize(trs.normalize(a)) == entry_trs.normalize(trs.normalize(b))

        a = parse(''' SUM(j, SUM(i, (BRA(i) DOT (A MLTK KET(j))) SCR (KET(i) OUTER BRA(j)) )) ''')
        b = parse('''A''')
        assert entry_trs.normalize(trs.normalize(a)) == entry_trs.normalize(trs.normalize(b))

def test_SUM_ELIM_10():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, SUM(j, (BRA(j) DOT (A MLTK KET(i))) SCR (KET(i) OUTER BRA(j)) )) ''')
        b = parse('''TP(A)''')
        assert entry_trs.normalize(trs.normalize(a)) == entry_trs.normalize(trs.normalize(b))

        a = parse(''' SUM(j, SUM(i, (BRA(i) DOT (A MLTK KET(j))) SCR (KET(j) OUTER BRA(i)) )) ''')
        b = parse('''TP(A)''')
        assert entry_trs.normalize(trs.normalize(a)) == entry_trs.normalize(trs.normalize(b))

#########################
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
        b = parse(''' TP(K0) DOT TP(B0) ''')
        a_ = trs.normalize(juxt(trs.normalize(a)))
        b_ = trs.normalize(juxt(trs.normalize(b)))
        assert a_ == b_

        a = parse(''' BRA('0') DOT (A MLTK KET('1')) ''')
        b = parse(''' BRA('1') DOT (TP(A) MLTK KET('0')) ''')
        a_ = trs.normalize(juxt(trs.normalize(a)))
        b_ = trs.normalize(juxt(trs.normalize(b)))
        assert a_ == b_

        a = parse(''' B1 DOT ((O1 MLTO TP(O2)) MLTK TP(B2)) ''')
        b = parse(''' B2 DOT ((O2 MLTO TP(O1)) MLTK TP(B1)) ''')
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
        a = parse(''' SUM(a, SUM(b, DELTA(a, x) SCR KET(PAIR(a, b)))) ''')
        b = parse(''' SUM(b, KET(PAIR(x, b))) ''')
        assert trs.normalize(a) == trs.normalize(b)
