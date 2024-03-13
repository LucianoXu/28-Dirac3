from diracdec import *
from diracdec.theory.dirac import *
from diracdec import parse

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
        a = parse(r'''0X''')
        b = Zero()
        assert a == b

        a = parse(r''' KET(s) ''')
        b = KetBase(TRSVar('s'))
        assert a == b

        a = parse(r''' ADJ(s) ''')
        b = Adj(TRSVar('s'))
        assert a == b
        
        a = parse(r''' S SCR K ''')
        b = Scal(TRSVar('S'), TRSVar('K'))
        assert a == b

        a = parse(r''' K1 ADD K2 ADD K3 ''')
        b = Add(TRSVar('K1'), TRSVar('K2'), TRSVar('K3'))
        assert a == b

        a = parse(r''' O MLTK K ''')
        b = KetApply(TRSVar('O'), TRSVar('K'))
        assert a == b

        a = parse(r''' K1 TSR K2 ''')
        b = Tensor(TRSVar('K1'), TRSVar('K2'))
        assert a == b

def test_basic_B():
    with wolfram_backend.wolfram_session():
        a = parse(r'''0X''')
        b = Zero()
        assert a == b

        a = parse(r''' BRA(s) ''')
        b = BraBase(TRSVar('s'))
        assert a == b

        a = parse(r''' ADJ(s) ''')
        b = Adj(TRSVar('s'))
        assert a == b
        
        a = parse(r''' S SCR B ''')
        b = Scal(TRSVar('S'), TRSVar('B'))
        assert a == b

        a = parse(r''' B1 ADD B2 ADD B3 ''')
        b = Add(TRSVar('B1'), TRSVar('B2'), TRSVar('B3'))
        assert a == b

        a = parse(r''' B MLTB O ''')
        b = BraApply(TRSVar('B'), TRSVar('O'))
        assert a == b

        a = parse(r''' B1 TSR B2 ''')
        b = Tensor(TRSVar('B1'), TRSVar('B2'))
        assert a == b

def test_basic_O():
    with wolfram_backend.wolfram_session():
        a = parse(r'''0X''')
        b = Zero()
        assert a == b

        a = parse(r''' 1O ''')
        b = OpOne()
        assert a == b

        a = parse(r''' K OUTER B ''')
        b = OpOuter(TRSVar('K'), TRSVar('B'))
        assert a == b

        a = parse(r''' ADJ(O)''')
        b = Adj(TRSVar('O'))
        assert a == b
        
        a = parse(r''' S SCR O ''')
        b = Scal(TRSVar('S'), TRSVar('O'))
        assert a == b

        a = parse(r''' O1 ADD O2 ADD O3 ''')
        b = Add(TRSVar('O1'), TRSVar('O2'), TRSVar('O3'))
        assert a == b

        a = parse(r''' O1 MLTO O2 ''')
        b = OpApply(TRSVar('O1'), TRSVar('O2'))
        assert a == b

        a = parse(r''' O1 TSR O2 ''')
        b = Tensor(TRSVar('O1'), TRSVar('O2'))
        assert a == b

def test_subst():
    with wolfram_backend.wolfram_session():
        a = parse(r'''{
            s : KET(a);
            t : BRA(b);
        }''')
        b = Subst({
            "s" : KetBase(TRSVar('a')),
            "t" : BraBase(TRSVar('b')),
        })
        assert a == b
