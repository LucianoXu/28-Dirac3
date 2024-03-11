
from diracdec import *
from diracdec.theory.dirac import *
from diracdec import parse

def test_1():
    with wolfram_backend.wolfram_session():
        a = ScalarAdd(TRSVar('A'), TRSVar('B'), TRSVar('A'))
        b = ScalarAdd(TRSVar('A'), TRSVar('A'), TRSVar('B'))
        assert a == b


def test_2():
    with wolfram_backend.wolfram_session():
        a = ScalarAdd(TRSVar('A'), TRSVar('A'), TRSVar('B'))
        b = ScalarMlt(TRSVar('A'), TRSVar('A'), TRSVar('B'))
        assert a != b

def test_subst_idempotent():
    with wolfram_backend.wolfram_session():
        sub = Subst({
            "ket0" : parse('''KET('0')'''),
            "bra0" : parse('''BRA('0')'''),
            "ket1" : parse('''KET('1')'''),
            "bra1" : parse('''BRA('1')'''),
            "I2" : parse('''(ket0 OUTER bra0) ADD (ket1 OUTER bra1)'''),
            "Z" : parse('''(ket0 OUTER bra0) ADD ("-1" SCR (ket1 OUTER bra1))'''),
        })

        sub_idempotent = sub.get_idempotent()
        assert sub_idempotent["I2"] == parse('''(KET('0') OUTER BRA('0')) ADD (KET('1') OUTER BRA('1'))''')




