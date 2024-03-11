
from diracdec import *

from diracdec import parse, dirac_trs as trs, label_trs

def test_REG_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' RFST(RPAIR(s, t)) ''')
        b = parse("s")
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_REG_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' RSND(RPAIR(s, t)) ''')
        b = parse("t")
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_REG_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' RPAIR(RFST(s), RSND(s)) ''')
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
        a = parse(r''' SETR(RFST(R)) UNIONR SETR(RSND(R)) ''')
        b = parse(r''' R ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' SETR(RSND(R)) UNIONR SETR(RFST(R)) UNIONR X ''')
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