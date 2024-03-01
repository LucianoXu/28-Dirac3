from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import dirac_bigop_delta_parse as parse, dirac_bigop_delta_trs as trs, juxt, sumeq

with wolfram_backend.wolfram_session():
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
        a = parse(''' SUM(a, "a")''')
        sub = Subst({
            "a" : parse(''' "1" '''),
        })
        assert a == sub(a)
        assert hash(a) == hash(sub(a))

def test_sum_swap():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(a, SUM(b, KET(PAIR(a, b)))) ''')
        b = parse(''' SUM(b, SUM(a, KET(PAIR(b, a)))) ''')
        assert a == b

def test_alpha_conv_with_Wolfram():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(a, SUM(b, "a + b")) ''')
        b = parse(''' SUM(b, SUM(a, "a + b")) ''')
        assert a == b



def test_QCQI_Theorem_4_1_with_abstraction():
    with wolfram_backend.wolfram_session():
        # define the rotation gates
        sub_rot = Subst({
            "Rz" : sub(parse(''' FUN beta . ( ("Cos[beta/2]" SCRO I2) ADDO ("- Sin[beta/2] I" SCRO Z) )''')),
            "Ry" : sub(parse(''' FUN gamma . ( ("Cos[gamma/2]" SCRO I2) ADDO ("- Sin[gamma/2] I" SCRO Y) )''')),
        })

        # get the idempotent operation
        new_sub = sub_rot.composite(sub).get_idempotent()

        a = new_sub(parse(''' "Exp[I a]" SCRO ((Rz @ beta) MLTO (Ry @ gamma) MLTO (Rz @ delta)) '''))

        b = new_sub(parse(''' ("Exp[I (a - beta/2 - delta/2)] Cos[gamma/2]" SCRO (ket0 OUTER bra0))
            ADDO ("- Exp[I (a - beta/2 + delta/2)] Sin[gamma/2]" SCRO (ket0 OUTER bra1)) 
            ADDO ("Exp[I (a + beta/2 - delta/2)] Sin[gamma/2]" SCRO (ket1 OUTER bra0))
            ADDO ("Exp[I (a + beta/2 + delta/2)] Cos[gamma/2]" SCRO (ket1 OUTER bra1))'''))

        norm_a = trs.normalize(sub(a))
        norm_b = trs.normalize(sub(b))
        assert wolU(norm_a) == wolU(norm_b)


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


def test_ASigma_bigop():
    '''

    `A[T] Sigma[T, S] == A^T[S] Sigma[T, S]`

    Note that the `SUM(i, KET(i) OUTER BRA(i))` at the beginning is necessary to decide the space type of A operator.
    '''
    with wolfram_backend.wolfram_session():
        a = parse(''' 
                        (
                            (
                                SUM(i, KET(i) OUTER BRA(i)) TSRO 1O
                            ) 
                            MLTO (A TSRO 1O)
                        ) 
                        MLTK 
                        (
                            SUM(i, KET(PAIR(i, i)))
                        ) 
                    ''')

        b = parse(''' 
                        (
                            (1O TSRO SUM(i, KET(i) OUTER BRA(i))) MLTO (1O TSRO TRANO(A))
                        ) 
                        MLTK 
                        (
                            SUM(i, KET(PAIR(i, i)))
                        ) 
                    ''')

        norm_a = trs.normalize(a)
        norm_b = trs.normalize(b)

        assert trs.normalize(juxt(sumeq(norm_a))) == trs.normalize(juxt(sumeq(norm_b)))

def test_choi():
    with wolfram_backend.wolfram_session():
        sub = Subst({
            "choi" : parse(r''' 
            FUN A . SUM(i, 
                        SUM(j, 
                            (BRA(i) DOT (A MLTK KET(j)))
                            SCRK KET(PAIR(i,j))
                        )    
                    ) ''')
        }).get_idempotent()

        a = sub(parse(r'''choi @ (KET('a') OUTER BRA('b'))'''))
        b = parse(r''' KET(PAIR('a', 'b')) ''')

        assert trs.normalize(a) == trs.normalize(b)

def test_unchoi():
    with wolfram_backend.wolfram_session():
        sub = Subst({
            "unchoi" : parse(r'''
            FUN A . SUM(i,
                        SUM(j,
                            (BRA(PAIR(i, j)) DOT A)
                            SCRO (KET(i) OUTER BRA(j))
                            )
                    )''')
        }).get_idempotent()

        a = sub(parse(r'''unchoi @ (KET(PAIR('a', 'b')))'''))
        b = parse(r'''KET('a') OUTER BRA('b')''')

        assert trs.normalize(a) == trs.normalize(b)

def test_choi_unchoi():
    with wolfram_backend.wolfram_session():
        sub = Subst({
        "choi" : parse(r''' 
        FUN A . SUM(i, 
                    SUM(j, 
                        (BRA(i) DOT (A MLTK KET(j)))
                        SCRK KET(PAIR(i,j))
                    )    
                ) '''),
        "unchoi" : parse(r'''
        FUN A . SUM(i,
                    SUM(j,
                        (BRA(PAIR(i, j)) DOT A)
                        SCRO (KET(i) OUTER BRA(j))
                        )
                )''')
        }).get_idempotent()

        a = sub(parse(r'''FUN A . unchoi @ (choi @ A) '''))
        b = parse(r'''FUN A . A''')

        assert trs.normalize(a) == trs.normalize(b)
