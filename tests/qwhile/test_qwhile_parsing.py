from diracdec import *

from qwhile.ast import *
from qwhile import parse


def test_abort():
    with wolfram_backend.wolfram_session():
        a = parse(r''' abort; ''')
        b = Abort()
        assert a == b

        a = parse(r''' abort; abort; ''')
        b = Abort() @ Abort()
        assert a == b

def test_skip():
    with wolfram_backend.wolfram_session():
        a = parse(r''' skip; ''')
        b = Skip()
        assert a == b

        a = parse(r''' skip; skip; ''')
        b = Skip() @ Skip()
        assert a == b


def test_init():
    with wolfram_backend.wolfram_session():
        a = parse(r''' q :=0 ; ''')
        b = Init(Var('q'))
        assert a == b

        a = parse(r''' PAIRR(p, q) :=0 ; ''')
        b = Init(QRegPair(Var('p'), Var('q')))
        assert a == b


def test_unitary():
    with wolfram_backend.wolfram_session():
        a = parse(r''' U[q]; ''')
        b = Unitary(Labelled1(Var('U'), Var('q')))
        assert a == b


def test_if():
    with wolfram_backend.wolfram_session():
        a = parse(r''' if ADJ(ADJ(P[q])) then U; else skip; end; ''')
        b = If(Adj(Adj(Labelled1(Var('P'), Var('q')))), Unitary(Var('U')), Skip())
        assert a == b

def test_while():
    with wolfram_backend.wolfram_session():
        a = parse(r''' while ADJ(ADJ(P[q])) do U; end; ''')
        b = While(Adj(Adj(Labelled1(Var('P'), Var('q')))), Unitary(Var('U')))
        assert a == b

def test_seq():
    with wolfram_backend.wolfram_session():
        a = parse(r''' while ADJ(ADJ(P[q])) do U; end; skip;''')
        b = While(Adj(Adj(Labelled1(Var('P'), Var('q')))), Unitary(Var('U'))) @ Skip()
        assert a == b

        a = parse(r''' abort; abort; abort; abort;''')
        b = Abort() @ (Abort() @ (Abort() @ Abort()))
        assert a == b

        b = Abort() @ (Abort() @ Abort()) @ Abort()
        a = Abort() @ (Abort() @ (Abort() @ Abort()))
        assert a == b
