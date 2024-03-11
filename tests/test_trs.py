from diracdec import *
from diracdec.theory.trs import *

from diracdec import parse

def test_bind_alpha_conv():
    a = BindVarTerm(TRSVar("x"), TRSVar("x"))
    b = BindVarTerm(TRSVar("y"), TRSVar("y"))
    assert a == b

    a = BindVarTerm(TRSVar("x"), TRSVar("z"))
    b = BindVarTerm(TRSVar("y"), TRSVar("z"))
    assert a == b

def test_bind_substitute():
    sub = Subst({
        "a" : TRSVar("z"),
    })
    a = BindVarTerm(TRSVar("a"), TRSVar("a"))
    assert sub(a) == a

    a = BindVarTerm(TRSVar("b"), TRSVar("a"))
    b = BindVarTerm(TRSVar("c"), TRSVar("z"))
    assert sub(a) == b


    a = BindVarTerm(TRSVar("z"), TRSVar("a"))
    b = BindVarTerm(TRSVar("y"), TRSVar("z"))
    assert sub(a) == b

