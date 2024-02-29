from diracdec import *
from diracdec.theory.trs import *

from diracdec import dirac_parse as parse

def test_bind_alpha_conv():
    a = BindVarTerm(TRSVar("x"), TRSVar("x"))
    b = BindVarTerm(TRSVar("y"), TRSVar("y"))
    assert a == b
    assert hash(a) == hash(b)

    a = BindVarTerm(TRSVar("x"), TRSVar("z"))
    b = BindVarTerm(TRSVar("y"), TRSVar("z"))
    assert a == b
    assert hash(a) == hash(b)

def test_bind_substitute():
    sub = Subst({
        "a" : TRSVar("z"),
    })
    a = BindVarTerm(TRSVar("a"), TRSVar("a"))
    assert sub(a) == a

    a = BindVarTerm(TRSVar("b"), TRSVar("a"))
    b = BindVarTerm(TRSVar("c"), TRSVar("z"))
    assert sub(a) == b

def test_multi_bind_eq():
    a = MultiBindTerm((TRSVar('a'), TRSVar('b')), TRSVar('X'))
    b = MultiBindTerm((TRSVar('b'), TRSVar('a')), TRSVar('X'))
    assert a == b
    assert hash(a) == hash(b)


    a = MultiBindTerm((TRSVar('a'), TRSVar('b')), TRSVar('a'))
    b = MultiBindTerm((TRSVar('b'), TRSVar('a')), TRSVar('a'))
    assert a == b
    assert hash(a) == hash(b)
