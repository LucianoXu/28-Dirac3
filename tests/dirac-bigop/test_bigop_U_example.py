from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import dirac_U_bigop_delta_parse as parse, dirac_U_bigop_delta_trs as trs, juxt, sumeq


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
        assert norm_a == norm_b
