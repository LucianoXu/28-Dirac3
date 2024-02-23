from diracdec import *

from diracdec import dirac_parse as parse

from diracdec.components.wolfram_cscalar import WolframCScalar
from diracdec.components.wolfram_abase import WolframABase

def test_atomic_base():
    with wolfram_backend.wolfram_session():
        a = parse(''' 'ss + ss' ''')
        b = parse(''' '2 ss' ''')
        assert a == b
        assert hash(a) == hash(b)


def test_complex_scalar():
    with wolfram_backend.wolfram_session():
        a = parse(''' "1.1" ''')
        b = parse(''' "1.1" ''')
        assert a == b
        assert hash(a) == hash(b)


def test_wolfram_cscalar():
    with wolfram_backend.wolfram_session():
        a = WolframCScalar("a + a")
        b = WolframCScalar("3 a - a")
        assert a == b
        assert hash(a) == hash(b)

def test_wolfram_variables():
    with wolfram_backend.wolfram_session():
        a = parse(''' "Sum[(1/2)^x, {x, 1, m}]" ''')
        assert a.variables() == set(["m"])

        a = parse(''' 'Sum[(1/2)^x, {x, 1, m}]' ''')
        assert a.variables() == set(["m"])

        a = parse(''' "HoldForm[Sum[(1/2)^i, {i, 1, Infinity}]]" ''')
        assert a.variables() == set(["i"])

        a = parse(''' 'HoldForm[Sum[(1/2)^i, {i, 1, Infinity}]]' ''')
        assert a.variables() == set(["i"])


def test_wolfram_substitute():
    with wolfram_backend.wolfram_session():
        sub = Subst({
            "a" : parse(''' "1" '''),
            "b" : parse(''' 'a + a' '''),
        })
        a = parse(''' "a" ''')
        b = parse(''' "1" ''')
        assert sub(a) == b

        a = parse(''' 'b - a' ''')
        b = parse(''' 'a' ''')
        assert sub(a) == b