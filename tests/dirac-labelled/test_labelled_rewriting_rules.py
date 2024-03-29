
from diracdec import *

from diracdec import parse, dirac_bigop_delta_trs as trs, label_trs

trs = trs + label_trs

def test_REG_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' FSTR(PAIRR(s, t)) ''')
        b = parse("s")
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_REG_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SNDR(PAIRR(s, t)) ''')
        b = parse("t")
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_REG_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' PAIRR(FSTR(s), SNDR(s)) ''')
        b = parse("s")
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S UNIONR ESETR ''')
        b = parse(r''' S ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S UNIONR S UNIONR S ''')
        b = parse(r''' S ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SETR(FSTR(R)) UNIONR SETR(SNDR(R)) ''')
        b = parse(r''' R ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' SETR(SNDR(R)) UNIONR SETR(FSTR(R)) UNIONR X ''')
        b = parse(r''' R UNIONR X''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S0 SUBR ESETR ''')
        b = parse(r''' S0 ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ESETR SUBR S0 ''')
        b = parse(r''' ESETR ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S0 SUBR S0 ''')
        b = parse(r''' ESETR ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S1 UNIONR S2) SUBR X ''')
        b = parse(r''' (S1 SUBR X) UNIONR (S2 SUBR X) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_8():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S1 SUBR (S2 UNIONR S3) ''')
        b = parse(r''' (S1 SUBR S2) SUBR S3 ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_9():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SETR(FSTR(R1)) UNIONR SETR(R1) ''')
        b = parse(r''' SETR(R1) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' SETR(FSTR(PAIRR(R1, X))) UNIONR SETR(PAIRR(R1, R2)) ''')
        b = parse(r''' SETR(PAIRR(R1, R2)) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' SETR(PAIRR(FSTR(R1), R2)) UNIONR SETR(PAIRR(R1, R2)) ''')
        b = parse(r''' SETR(PAIRR(R1, R2)) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_10():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SETR(FSTR(R1)) SUBR SETR(R1) ''')
        b = parse(r''' ESETR ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_RSET_11():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SETR(R1) SUBR SETR(FSTR(R1)) ''')
        b = parse(r''' (SETR(FSTR(R1)) SUBR SETR(FSTR(R1))) UNIONR (SETR(SNDR(R1)) SUBR SETR(FSTR(R1))) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_RSET_12():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SETR(R1) SUBR SETR(R2) ''')
        b = parse(r''' SETR(R1) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


###############################################################
# labelled dirac notation rules
        
def test_TSR_DECOMP_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' KET(PAIR(s, t))[PAIRR(Q, R)] ''')
        b = parse(r''' KET(s)[Q] TSRKL KET(t)[R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_TSR_DECOMP_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' BRA(PAIR(s, t))[PAIRR(Q, R)] ''')
        b = parse(r''' BRA(s)[Q] TSRBL BRA(t)[R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_TSR_DECOMP_3A():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X[PAIRR(Q1, Q2); R] ''')
        b = parse(r''' (0X[Q1; FSTR(R)]) TSROL (0X[Q2; SNDR(R)]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_TSR_DECOMP_3B():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 0X[Q; PAIRR(R1, R2)] ''')
        b = parse(r''' (0X[FSTR(Q); R1]) TSROL (0X[SNDR(Q2); R2]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_TSR_DECOMP_3C():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 1O[PAIRR(Q, R)] ''')
        b = parse(r''' (1O[Q]) TSROL (1O[R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_TSR_DECOMP_3D():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 1O[PAIRR(Q1, Q2); R] ''')
        b = parse(r''' (1O[Q1; FSTR(R)]) TSROL (1O[Q2; SNDR(R)]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_TSR_DECOMP_3E():
    with wolfram_backend.wolfram_session():
        a = parse(r''' 1O[Q; PAIRR(R1, R2)] ''')
        b = parse(r''' (1O[FSTR(Q); R1]) TSROL (1O[SNDR(Q2); R2]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_TSR_DECOMP_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A TSRK B)[PAIRR(Q, R)] ''')
        b = parse(r''' (A[Q] TSRKL B[R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' (A TSRB B)[PAIRR(Q, R)] ''')
        b = parse(r''' (A[Q] TSRBL B[R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' (A TSRO B)[PAIRR(Q, R)] ''')
        b = parse(r''' (A[Q] TSROL B[R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_TSR_DECOMP_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A TSRO B)[PAIRR(Q1, Q2); R] ''')
        b = parse(r''' (A[Q1; FSTR(R)]) TSROL (B[Q2; SNDR(R)]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_TSR_DECOMP_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A TSRO B)[Q; PAIRR(R1, R2)] ''')
        b = parse(r''' (A[FSTR(Q); R1]) TSROL (B[SNDR(Q); R2]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_TSR_COMP_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[FSTR(Q); FSTR(R)]) TSROL (B[SNDR(Q); SNDR(R)]) ''')
        b = parse(r''' (A TSRO B)[Q; R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_TSR_COMP_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[FSTR(Q)]) TSRKL (B[SNDR(Q)]) ''')
        b = parse(r''' (A TSRK B)[Q] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' (A[FSTR(Q)]) TSRBL (B[SNDR(Q)]) ''')
        b = parse(r''' (A TSRB B)[Q] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' (A[FSTR(Q)]) TSROL (B[SNDR(Q)]) ''')
        b = parse(r''' (A TSRO B)[Q] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_DOT_TSR_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[Q;R]) MLTOL (B[S;T]) ''')
        b = parse(r''' (A[Q;R]) TSROL (B[S;T]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_LIFT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(A[R]) ''')
        b = parse(r''' (ADJ(A))[R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ADJ(A[Q; R]) ''')
        b = parse(r''' (ADJ(A))[Q; R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_LIFT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S SCR A)[R] ''')
        b = parse(r''' S SCR (A[R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S SCR A)[Q; R] ''')
        b = parse(r''' S SCR (A[Q; R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A ADD B)[R] ADD X ''')
        b = parse(r''' (A[R]) ADD (B[R]) ADD X ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A ADD B)[Q; R] ADD X ''')
        b = parse(r''' (A[Q; R]) ADD (B[Q; R]) ADD X ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_LIFT_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A ADD A ''')
        b = parse(r''' "2" SCR A ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_8():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ("a" SCR A) ADD A ''')
        b = parse(r''' ("a" ADDS "1") SCR A ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_LIFT_9():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ("a" SCR A) ADD ("b" SCR A) ''')
        b = parse(r''' ("a" ADDS "b") SCR A ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_LIFT_10():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[Q; R]) MLTOL (B[R; S]) ''')
        b = parse(r''' (A MLTO B)[Q; S] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_LIFT_11():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[Q; R]) MLTOL (B[R]) ''')
        b = parse(r''' (A MLTO B)[Q; R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_12():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[Q]) MLTOL (B[Q; R]) ''')
        b = parse(r''' (A MLTO B)[Q; R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_13():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[Q; R]) MLTKL (B[R]) ''')
        b = parse(r''' (A MLTK B)[Q] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_14():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[Q]) MLTBL (B[Q; R]) ''')
        b = parse(r''' (A MLTB B)[R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_15():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[R]) MLTKL (B[R]) ''')
        b = parse(r''' (A MLTK B)[R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' (A[R]) MLTBL (B[R]) ''')
        b = parse(r''' (A MLTB B)[R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' (A[R]) MLTOL (B[R]) ''')
        b = parse(r''' (A MLTO B)[R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_16():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[R]) DOTL (B[R]) ''')
        b = parse(r''' A DOT B ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_LIFT_17():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (K0 OUTER B0)[R] ''')
        b = parse(r''' (K0[R]) OUTERL (B0[R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_LIFT_18():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (K0 OUTER B0)[Q; R] ''')
        b = parse(r''' (K0[Q]) OUTERL (B0[R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_OPT_EXT_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A[R; R] ''')
        b = parse(r''' A[R] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_OPT_EXT_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[R]) MLTOL (B[PAIRR(R, Q)]) ''')
        b = parse(r''' ((A TSRO 1O) MLTO B)[PAIRR(R, Q)] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' (A[SNDR(R)]) MLTOL (B[PAIRR(R, Q)]) ''')
        b = parse(r''' (((1O TSRO A) TSRO 1O) MLTO B)[PAIRR(R, Q)] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_OPT_EXT_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B[PAIRR(R, Q)]) MLTOL (A[R]) ''')
        b = parse(r''' (B MLTO (A TSRO 1O))[PAIRR(R, Q)] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' (B[PAIRR(R, Q)]) MLTOL (A[SNDR(R)])''')
        b = parse(r''' (B MLTO ((1O TSRO A) TSRO 1O))[PAIRR(R, Q)] ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_SUM_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SUM(x, T, A)[R] ''')
        b = parse(r''' SUM(x, T, A[R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_SUM_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SUM(x, T, A)[Q; R] ''')
        b = parse(r''' SUM(x, T, A[Q; R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)



def test_LABEL_SUM_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SUMS(i, USET, BRA(i)[R]) DOTL (KET('0')[R]) ''')
        b = parse(r''' SUMS(i, USET, (BRA(i)[R]) DOTL (KET('0')[R])) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_SUM_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' BRA('0')[R] DOTL SUMS(i, USET, KET(i)[R]) ''')
        b = parse(r''' SUMS(i, USET, BRA('0')[R] DOTL KET(i)[R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

# def test_LABEL_SUM_5():
#     with wolfram_backend.wolfram_session():
#         a = parse(r''' SUM(i, T, KET(i)) TSRK KET(j) ''')
#         b = parse(r''' SUM(i, T, KET(PAIR(i, j))) ''')
#         assert label_trs.normalize(a) == label_trs.normalize(b)

# def test_LABEL_SUM_6():
#     with wolfram_backend.wolfram_session():
#         a = parse(r''' BRA(j)[R] TSRBL SUM(i, T, BRA(i)[Q]) ''')
#         b = parse(r''' SUM(i, T, (BRA(j) TSRB BRA(i))[PAIRR(R, Q)]) ''')
#         assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_TEMP_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A[R] MLTOL (B[PAIRR(R, Q)] TSROL X) ''')
        b = parse(r''' (A[R] MLTOL B[PAIRR(R, Q)]) TSROL X ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_TEMP_1O():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A[R] MLTOL (K[PAIRR(R, Q)] OUTERL X) ''')
        b = parse(r''' (A[R] MLTKL K[PAIRR(R, Q)]) OUTERL X ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_TEMP_1B():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (Y TSRBL B[R]) MLTBL (K[R] OUTERL X) ''')
        b = parse(r''' (B DOT K) SCR (Y TSRBL X) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_TEMP_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (B[PAIRR(R, Q)] TSROL X) MLTOL A[R] ''')
        b = parse(r''' (B[PAIRR(R, Q)] MLTOL A[R]) TSROL X ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_LABEL_TEMP_2O():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (X OUTERL B[PAIRR(R, Q)]) MLTOL A[R] ''')
        b = parse(r''' X OUTERL (B[PAIRR(R, Q)] MLTBL A[R]) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_TEMP_2B():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (X OUTERL B[R]) MLTKL (K[R] TSRKL Y) ''')
        b = parse(r''' (B DOT K) SCR (X TSRKL Y) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_TEMP_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A[R] DOT (B[R] TSRKL X) ''')
        b = parse(r''' (A[R] DOT B[R]) SCR X ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_TEMP_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A[R] TSRBL X) DOT B[R] ''')
        b = parse(r''' (A[R] DOT B[R]) SCR X ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_LABEL_TEMP_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A MLTOL B) MLTOL C ''')
        b = parse(r''' A MLTOL (B MLTOL C) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' SUM(i, (A MLTOL B) MLTOL C) ''')
        b = parse(r''' SUM(i, A MLTOL (B MLTOL C)) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)