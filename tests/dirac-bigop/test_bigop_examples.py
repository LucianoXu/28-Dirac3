from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import dirac_bigop_delta_parse as parse, dirac_bigop_delta_trs as trs, juxt, sumeq

sub = Subst({
    "ket0" : parse('''KET('0')'''),
    "bra0" : parse('''BRA('0')'''),
    "ket1" : parse('''KET('1')'''),
    "bra1" : parse('''BRA('1')'''),
    "ketP" : parse(''' "Sqrt[1/2]" SCRK (ket0 ADDK ket1) '''),
    "braP" : parse(''' "Sqrt[1/2]" SCRB (bra0 ADDB bra1) '''),
    "ketM" : parse(''' "Sqrt[1/2]" SCRK (ket0 ADDK ("-1" MLTK ket1)) '''),
    "braM" : parse(''' "Sqrt[1/2]" SCRB (bra0 ADDB ("-1" MLTB bra1)) '''),

    "beta00" : parse(''' "Sqrt[1/2]" SCRK ((ket0 TSRK ket0) ADDK (ket1 TSRK ket1))'''),

    "I2" : parse('''(ket0 OUTER bra0) ADDO (ket1 OUTER bra1)'''),

    "Z" : parse('''(ket0 OUTER bra0) ADDO ("-1" SCRO (ket1 OUTER bra1))'''),

    "X" : parse('''(ket0 OUTER bra1) ADDO (ket1 OUTER bra0)'''),

    "Y" : parse('''("-I" SCRO (ket0 OUTER bra1)) ADDO ("I" SCRO (ket1 OUTER bra0))'''),


    "H" : parse(''' "Sqrt[1/2]" SCRO ((ket0 OUTER bra0) ADDO (ket0 OUTER bra1) ADDO (ket1 OUTER bra0) ADDO ("-1" SCRO (ket1 OUTER bra1)))'''),

    "CX": parse(''' ((ket0 TSRK ket0) OUTER (bra0 TSRB bra0))
                ADDO ((ket0 TSRK ket1) OUTER (bra0 TSRB bra1)) 
                ADDO ((ket1 TSRK ket1) OUTER (bra1 TSRB bra0))
                ADDO ((ket1 TSRK ket0) OUTER (bra1 TSRB bra1))'''),

    "CZ": parse(''' ((ket0 TSRK ket0) OUTER (bra0 TSRB bra0))
                ADDO ((ket0 TSRK ket1) OUTER (bra0 TSRB bra1)) 
                ADDO ((ket1 TSRK ket0) OUTER (bra1 TSRB bra0))
                ADDO ("-1" SCRO ((ket1 TSRK ket1) OUTER (bra1 TSRB bra1)))'''),

}).get_idempotent()


def test_1():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUMS(a, "a")''')
        sub = Subst({
            "a" : parse(''' "1" '''),
        })
        assert a == sub(a)
        assert hash(a) == hash(sub(a))

def test_alpha_conv_with_Wolfram():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUMS(a, SUMS(b, "a + b")) ''')
        b = parse(''' SUMS(b, SUMS(a, "a + b")) ''')
        assert a == b


def test_ASigma():
    '''
    2-qubit case for 

    `A[T] Sigma[T, S] == A^T[S] Sigma[T, S]`

    Note that the `(I2 TSRO I2)` at the beginning is necessary to decide the space type of A operator.
    '''
    with wolfram_backend.wolfram_session():
        a = sub(parse(r''' (I2 TSRO I2) MLTK ((A TSRO 1O) MLTK ((ket0 TSRK ket0) ADDK (ket1 TSRK ket1)))'''))
        b = sub(parse(r''' (I2 TSRO I2) MLTK ((1O TSRO TRANO(A)) MLTK ((ket0 TSRK ket0) ADDK (ket1 TSRK ket1))) '''))

        norm_a = trs.normalize(a)
        norm_b = trs.normalize(b)

        assert trs.normalize(juxt(norm_a)) == trs.normalize(juxt(norm_b))