
from diracdec import *

from diracdec import parse, dirac_delta_trs as trs


with wolfram_backend.wolfram_session():
    sub = Subst({
        "ket0" : parse('''KET('0')'''),
        "bra0" : parse('''BRA('0')'''),
        "ket1" : parse('''KET('1')'''),
        "bra1" : parse('''BRA('1')'''),
        "ketP" : parse(''' "Sqrt[1/2]" SCR (ket0 ADD ket1) '''),
        "braP" : parse(''' "Sqrt[1/2]" SCR (bra0 ADD bra1) '''),
        "ketM" : parse(''' "Sqrt[1/2]" SCR (ket0 ADD ("-1" MLTK ket1)) '''),
        "braM" : parse(''' "Sqrt[1/2]" SCR (bra0 ADD ("-1" MLTB bra1)) '''),

        "beta00" : parse(''' "Sqrt[1/2]" SCR ((ket0 TSR ket0) ADD (ket1 TSR ket1))'''),

        "I2" : parse('''(ket0 OUTER bra0) ADD (ket1 OUTER bra1)'''),

        "Z" : parse('''(ket0 OUTER bra0) ADD ("-1" SCR (ket1 OUTER bra1))'''),

        "X" : parse('''(ket0 OUTER bra1) ADD (ket1 OUTER bra0)'''),

        "Y" : parse('''("-I" SCR (ket0 OUTER bra1)) ADD ("I" SCR (ket1 OUTER bra0))'''),


        "H" : parse(''' "Sqrt[1/2]" SCR ((ket0 OUTER bra0) ADD (ket0 OUTER bra1) ADD (ket1 OUTER bra0) ADD ("-1" SCR (ket1 OUTER bra1)))'''),

        "CX": parse(''' ((ket0 TSR ket0) OUTER (bra0 TSR bra0))
                    ADD ((ket0 TSR ket1) OUTER (bra0 TSR bra1)) 
                    ADD ((ket1 TSR ket1) OUTER (bra1 TSR bra0))
                    ADD ((ket1 TSR ket0) OUTER (bra1 TSR bra1))'''),

        "CZ": parse(''' ((ket0 TSR ket0) OUTER (bra0 TSR bra0))
                    ADD ((ket0 TSR ket1) OUTER (bra0 TSR bra1)) 
                    ADD ((ket1 TSR ket0) OUTER (bra1 TSR bra0))
                    ADD ("-1" SCR ((ket1 TSR ket1) OUTER (bra1 TSR bra1)))'''),

    }).get_idempotent()

def test_XYZ():
    with wolfram_backend.wolfram_session():
        a = sub(parse(''' X MLTO X '''))
        b = sub(parse(''' I2 '''))
        assert trs.normalize(a) == trs.normalize(b)

        a = sub(parse(''' Y MLTO Y '''))
        b = sub(parse(''' I2 '''))
        assert trs.normalize(a) == trs.normalize(b)

        a = sub(parse(''' Z MLTO Z '''))
        b = sub(parse(''' I2 '''))
        assert trs.normalize(a) == trs.normalize(b)

        a = sub(parse(''' X MLTO Y '''))
        b = sub(parse(''' "I" SCR Z '''))
        assert trs.normalize(a) == trs.normalize(b)

        a = sub(parse(''' Y MLTO X '''))
        b = sub(parse(''' "-I" SCR Z '''))
        assert trs.normalize(a) == trs.normalize(b)

def test_Hadamard():
    with wolfram_backend.wolfram_session():
        a = sub(parse(''' H MLTO H'''))
        b = sub(parse(''' I2 '''))
        assert trs.normalize(a) == trs.normalize(b)

        a = sub(parse(''' H MLTK ketP'''))
        b = sub(parse(''' ket0 '''))
        assert trs.normalize(a) == trs.normalize(b)

def test_cylinder_ext():
    with wolfram_backend.wolfram_session():
        a = sub(parse(''' (I2 TSR X) MLTO (X TSR I2) '''))
        b = sub(parse(''' X TSR X'''))
        assert trs.normalize(a) == trs.normalize(b)

def test_CX():
    with wolfram_backend.wolfram_session():
        a = sub(parse(''' CX MLTO CX '''))
        b = sub(parse(''' I2 TSR I2 '''))
        assert trs.normalize(a) == trs.normalize(b)

        # this term can be a little time consuming
        a = sub(parse(''' (I2 TSR H) MLTO CZ MLTO (I2 TSR H)'''))
        b = sub(parse(''' CX '''))
        assert trs.normalize(a) == trs.normalize(b)


def test_QCQI_Theorem_4_1():
    '''
    QCQI, Theorem 4.1
    '''
    with wolfram_backend.wolfram_session():

        # define the rotation gates
        sub_rot = Subst({
            "Rzbeta" : sub(parse(''' ("Cos[beta/2]" SCR I2) ADD ("- Sin[beta/2] I" SCR Z) ''')),
            "Rygamma" : sub(parse(''' ("Cos[gamma/2]" SCR I2) ADD ("- Sin[gamma/2] I" SCR Y) ''')),
            "Rzdelta" : sub(parse(''' ("Cos[delta/2]" SCR I2) ADD ("- Sin[delta/2] I" SCR Z) ''')),
        })

        # get the idempotent operation
        new_sub = sub_rot.composite(sub).get_idempotent()

        # RHS - rotations
        a = new_sub(parse(''' "Exp[I a]" SCR (Rzbeta MLTO Rygamma MLTO Rzdelta) '''))
        # LHS - U
        b = new_sub(parse(''' ("Exp[I (a - beta/2 - delta/2)] Cos[gamma/2]" SCR (ket0 OUTER bra0))
            ADD ("- Exp[I (a - beta/2 + delta/2)] Sin[gamma/2]" SCR (ket0 OUTER bra1)) 
            ADD ("Exp[I (a + beta/2 - delta/2)] Sin[gamma/2]" SCR (ket1 OUTER bra0))
            ADD ("Exp[I (a + beta/2 + delta/2)] Cos[gamma/2]" SCR (ket1 OUTER bra1))'''))
        
        norm_a = trs.normalize(sub(a), alg = "inner_most")
        norm_b = trs.normalize(sub(b), alg = "inner_most")
        assert wolU(norm_a) == wolU(norm_b)



def test_simple_circ():
    with wolfram_backend.wolfram_session():
        a = parse(''' (A TSR I2) MLTO CX MLTO (X TSR I2) MLTO (X TSR I2) MLTO CX MLTO U ''')
        b = parse(''' (A TSR I2) MLTO (I2 TSR I2) MLTO U ''')

        assert trs.normalize(sub(a)) == trs.normalize(sub(b))