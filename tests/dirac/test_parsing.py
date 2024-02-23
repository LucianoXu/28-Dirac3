from diracdec import *
from diracdec.theory.dirac import *
from diracdec import dirac_parse as parse

def test_basic_base():
    with wolfram_backend.wolfram_session():
        a = parse(r''' PAIR(s, t) ''')
        b = BasePair(TRSVar('s'), TRSVar('t'))
        assert a == b

        a = parse(r''' FST(s) ''')
        b = BaseFst(TRSVar('s'))
        assert a == b

        a = parse(r''' SND(s) ''')
        b = BaseSnd(TRSVar('s'))
        assert a == b

def test_basic_S():
    with wolfram_backend.wolfram_session():
        a = parse(r''' DELTA(s, t) ''')
        b = ScalarDelta(TRSVar('s'), TRSVar('t'))
        assert a == b

        a = parse(r''' A ADDS B ''')
        b = ScalarAdd(TRSVar('A'), TRSVar('B'))
        assert a == b

        a = parse(r''' A MLTS B MLTS A ''')
        b = ScalarMlt(TRSVar('A'), TRSVar('A'), TRSVar('B'))
        assert a == b
        
        a = parse(r''' CONJS(A) ''')
        b = ScalarConj(TRSVar('A'))
        assert a == b

        a = parse(r''' A DOT B ''')
        b = ScalarDot(TRSVar('A'), TRSVar('B'))
        assert a == b

def test_basic_K():
    with wolfram_backend.wolfram_session():
        a = parse(r'''0K''')
        b = KetZero()
        assert a == b

        a = parse(r''' KET(s) ''')
        b = KetBase(TRSVar('s'))
        assert a == b

        a = parse(r''' ADJK(s) ''')
        b = KetAdj(TRSVar('s'))
        assert a == b
        
        a = parse(r''' S SCRK K ''')
        b = KetScal(TRSVar('S'), TRSVar('K'))
        assert a == b

        a = parse(r''' K1 ADDK K2 ADDK K3 ''')
        b = KetAdd(TRSVar('K1'), TRSVar('K2'), TRSVar('K3'))
        assert a == b

        a = parse(r''' O MLTK K ''')
        b = KetApply(TRSVar('O'), TRSVar('K'))
        assert a == b

        a = parse(r''' K1 TSRK K2 ''')
        b = KetTensor(TRSVar('K1'), TRSVar('K2'))
        assert a == b

def test_basic_B():
    with wolfram_backend.wolfram_session():
        a = parse(r'''0B''')
        b = BraZero()
        assert a == b

        a = parse(r''' BRA(s) ''')
        b = BraBase(TRSVar('s'))
        assert a == b

        a = parse(r''' ADJB(s) ''')
        b = BraAdj(TRSVar('s'))
        assert a == b
        
        a = parse(r''' S SCRB B ''')
        b = BraScal(TRSVar('S'), TRSVar('B'))
        assert a == b

        a = parse(r''' B1 ADDB B2 ADDB B3 ''')
        b = BraAdd(TRSVar('B1'), TRSVar('B2'), TRSVar('B3'))
        assert a == b

        a = parse(r''' B MLTB O ''')
        b = BraApply(TRSVar('B'), TRSVar('O'))
        assert a == b

        a = parse(r''' B1 TSRB B2 ''')
        b = BraTensor(TRSVar('B1'), TRSVar('B2'))
        assert a == b

def test_basic_O():
    with wolfram_backend.wolfram_session():
        a = parse(r'''0O''')
        b = OpZero()
        assert a == b

        a = parse(r''' 1O ''')
        b = OpOne()
        assert a == b

        a = parse(r''' K OUTER B ''')
        b = OpOuter(TRSVar('K'), TRSVar('B'))
        assert a == b

        a = parse(r''' ADJO(O)''')
        b = OpAdj(TRSVar('O'))
        assert a == b
        
        a = parse(r''' S SCRO O ''')
        b = OpScal(TRSVar('S'), TRSVar('O'))
        assert a == b

        a = parse(r''' O1 ADDO O2 ADDO O3 ''')
        b = OpAdd(TRSVar('O1'), TRSVar('O2'), TRSVar('O3'))
        assert a == b

        a = parse(r''' O1 MLTO O2 ''')
        b = OpApply(TRSVar('O1'), TRSVar('O2'))
        assert a == b

        a = parse(r''' O1 TSRO O2 ''')
        b = OpTensor(TRSVar('O1'), TRSVar('O2'))
        assert a == b