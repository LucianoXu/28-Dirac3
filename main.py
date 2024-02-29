
from diracdec import *

from diracdec.components.wolfram_simple import *

from diracdec import dirac_bigop_delta_parse as parse, dirac_bigop_delta_trs as trs, juxt, sumeq

from diracdec import dirac_cime2_file

if __name__ == "__main__":
    with wolfram_backend.wolfram_session():
        sub = Subst({
            "ket0" : parse('''KET('0')'''),
            "bra0" : parse('''BRA('0')'''),
            "ket1" : parse('''KET('1')'''),
            "bra1" : parse('''BRA('1')'''),

            "I2" : parse('''(ket0 OUTER bra0) ADDO (ket1 OUTER bra1)'''),

            "Z" : parse('''(ket0 OUTER bra0) ADDO ("-1" SCRO (ket1 OUTER bra1))'''),

            "X" : parse('''(ket0 OUTER bra1) ADDO (ket1 OUTER bra0)'''),

            "Y" : parse('''("-I" SCRO (ket0 OUTER bra1)) ADDO ("I" SCRO (ket1 OUTER bra0))'''),

            "ketP" : parse(''' "Sqrt[1/2]" SCRK (ket0 ADDK ket1) '''),

            "braP" : parse(''' "Sqrt[1/2]" SCRB (bra0 ADDB bra1) '''),

            "ketM" : parse(''' "Sqrt[1/2]" SCRK (ket0 ADDK ("-1" MLTK ket1)) '''),

            "braM" : parse(''' "Sqrt[1/2]" SCRB (bra0 ADDB ("-1" MLTB bra1)) '''),

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


######################`#######################
    with wolfram_backend.wolfram_session():

        a = parse(''' SUM(a, "a")''')
        sub = Subst({
            "a" : parse(''' "1" '''),
        })
        
        print(a)
        print(sub(a))
        # print(trs.normalize(b))

        exit(0)

        new_sub = Subst({
            "a" : parse(''' "1" '''),
        })

        a = parse(''' (FUN x . x) @ "1"''')
        
        print(repr(a))
        print(trs.normalize(a))