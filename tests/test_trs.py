from diracdec import *
from diracdec.theory.trs import *

from diracdec import parse

def test_bind_alpha_conv():
    a = BindVarTerm(Var("x"), Var("x"))
    b = BindVarTerm(Var("y"), Var("y"))
    assert a == b

    a = BindVarTerm(Var("x"), Var("z"))
    b = BindVarTerm(Var("y"), Var("z"))
    assert a == b

def test_bind_substitute():
    sub = Subst({
        "a" : Var("z"),
    })
    a = BindVarTerm(Var("a"), Var("a"))
    assert sub(a) == a

    a = BindVarTerm(Var("b"), Var("a"))
    b = BindVarTerm(Var("c"), Var("z"))
    assert sub(a) == b


    a = BindVarTerm(Var("z"), Var("a"))
    b = BindVarTerm(Var("y"), Var("z"))
    assert sub(a) == b

