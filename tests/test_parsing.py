from diracdec import *



def test_1():
    with wolfram_backend.wolfram_session():
        a = parse(''' 'ss + ss' ''')
        b = parse(''' '2 ss' ''')
        assert a == b
        assert hash(a) == hash(b)
        

def test_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A \ADDS B \ADDS A ''')
        b = ScalarAdd((TRSVar('A'), TRSVar('A'), TRSVar('B')))
        assert a == b
        assert hash(a) == hash(b)

        c = parse(r''' A \MLTS B \MLTS A ''')
        assert a != c
        assert hash(a) != hash(c)

def test_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A \MLTS B \MLTS A ''')
        b = ScalarMlt((TRSVar('A'), TRSVar('A'), TRSVar('B')))
        assert a == b
        assert hash(a) == hash(b)

def test_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A^* ''')
        b = ScalarConj(TRSVar('A'))
        assert a == b
