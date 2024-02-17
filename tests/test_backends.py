from diracdec import *


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