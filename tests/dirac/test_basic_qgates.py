
from diracdec import *

from diracdec import dirac_delta_parse as parse, dirac_delta_trs as trs


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
        b = sub(parse(''' "I" SCRO Z '''))
        assert trs.normalize(a) == trs.normalize(b)

        a = sub(parse(''' Y MLTO X '''))
        b = sub(parse(''' "-I" SCRO Z '''))
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
        a = sub(parse(''' (I2 TSRO X) MLTO (X TSRO I2) '''))
        b = sub(parse(''' X TSRO X'''))
        assert trs.normalize(a) == trs.normalize(b)

def test_CX():
    with wolfram_backend.wolfram_session():
        a = sub(parse(''' CX MLTO CX '''))
        b = sub(parse(''' I2 TSRO I2 '''))
        assert trs.normalize(a) == trs.normalize(b)

        # this term can be a little time consuming
        a = sub(parse(''' (I2 TSRO H) MLTO CZ MLTO (I2 TSRO H)'''))
        b = sub(parse(''' CX '''))
        assert trs.normalize(a) == trs.normalize(b)

def test_simple_circ():
    with wolfram_backend.wolfram_session():
        a = parse(''' (A TSRO I2) MLTO CX MLTO (X TSRO I2) MLTO (X TSRO I2) MLTO CX MLTO U ''')
        b = parse(''' (A TSRO I2) MLTO (I2 TSRO I2) MLTO U ''')

        assert trs.normalize(sub(a)) == trs.normalize(sub(b))