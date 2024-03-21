from diracdec import *

from qwhile import parse, forward_trs
from qwhile.forward import CfgSet


def test_OP_SEM_SKIP():
    with wolfram_backend.wolfram_session():
        a = parse(r''' < skip; , rho > ''')
        b = parse(r''' < HALT, rho > ''')
        assert forward_trs.normalize(a) == forward_trs.normalize(b)

def test_OP_SEM_ABORT():
    with wolfram_backend.wolfram_session():
        a = parse(r''' < abort; , rho > ''')
        b = parse(r''' < HALT , 0X > ''')
        assert forward_trs.normalize(a) == forward_trs.normalize(b)

def test_OP_SEM_INIT():
    with wolfram_backend.wolfram_session():
        a = parse(r''' < q :=0 ; , rho > ''')
        b = parse(r''' < HALT , SUM(i, (KET('0') OUTER BRA(i))[q] MLTOL rho MLTOL (KET(i) OUTER BRA('0'))[q]) > ''')
        assert forward_trs.normalize(a) == forward_trs.normalize(b)


def test_OP_SEM_UNITARY():
    with wolfram_backend.wolfram_session():
        a = parse(r''' < U; , rho > ''')
        b = parse(r''' < HALT , U MLTOL rho MLTOL ADJ(U) > ''')
        assert forward_trs.normalize(a) == forward_trs.normalize(b)

def test_OP_SEM_IF():
    with wolfram_backend.wolfram_session():
        a = parse(''' < if P then s1 else s2 end; , rho > ''')
        b = CfgSet(
            parse(''' < s1 , P MLTOL rho MLTOL P > '''),
            parse(''' < s2 , (1O ADD ("-1" SCR P)) MLTOL rho MLTOL (1O ADD ("-1" SCR P)) > '''))
        assert forward_trs.normalize(a) == forward_trs.normalize(b)


def test_OP_SEM_WHILE():
    with wolfram_backend.wolfram_session():
        a = parse(''' < while [0] P do S end; , rho > ''')
        b = parse(''' < abort; , rho > ''')
        assert forward_trs.normalize(a) == forward_trs.normalize(b)

        a = parse(''' < while [5] P do S end; , rho > ''')
        b = parse(f''' < if P then S while [4] P do S end; else skip; end; , rho > ''')
        assert forward_trs.normalize(a) == forward_trs.normalize(b)

def test_OP_SEM_SEQ():
    with wolfram_backend.wolfram_session():
        a = parse(''' < skip; skip; , rho > ''')
        b = parse(''' < HALT , rho > ''')
        assert forward_trs.normalize(a) == forward_trs.normalize(b)

def test_OP_SEM_ADD():
    with wolfram_backend.wolfram_session():
        a = CfgSet(parse(''' < HALT , rho1 > '''), parse(''' < HALT ,rho2 > '''))
        b = parse(''' < HALT , rho1 ADD rho2 > ''')
        assert forward_trs.normalize(a) == forward_trs.normalize(b)
