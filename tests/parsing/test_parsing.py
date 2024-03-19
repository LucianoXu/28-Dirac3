from diracdec import *
from diracdec.theory.dirac import *
from diracdec import parse

def test_basic_base():
    with wolfram_backend.wolfram_session():
        a = parse(r''' PAIR(s, t) ''')
        b = BasePair(Var('s'), Var('t'))
        assert a == b

        a = parse(r''' FST(s) ''')
        b = BaseFst(Var('s'))
        assert a == b

        a = parse(r''' SND(s) ''')
        b = BaseSnd(Var('s'))
        assert a == b

def test_basic_S():
    with wolfram_backend.wolfram_session():
        a = parse(r''' DELTA(s, t) ''')
        b = ScalarDelta(Var('s'), Var('t'))
        assert a == b

        a = parse(r''' A ADDS B ''')
        b = ScalarAdd(Var('A'), Var('B'))
        assert a == b

        a = parse(r''' A MLTS B MLTS A ''')
        b = ScalarMlt(Var('A'), Var('A'), Var('B'))
        assert a == b
        
        a = parse(r''' CONJS(A) ''')
        b = ScalarConj(Var('A'))
        assert a == b

        a = parse(r''' A DOT B ''')
        b = ScalarDot(Var('A'), Var('B'))
        assert a == b

def test_basic_K():
    with wolfram_backend.wolfram_session():
        a = parse(r'''0X''')
        b = Zero()
        assert a == b

        a = parse(r''' KET(s) ''')
        b = KetBase(Var('s'))
        assert a == b

        a = parse(r''' ADJ(s) ''')
        b = Adj(Var('s'))
        assert a == b
        
        a = parse(r''' S SCR K ''')
        b = Scal(Var('S'), Var('K'))
        assert a == b

        a = parse(r''' K1 ADD K2 ADD K3 ''')
        b = Add(Var('K1'), Var('K2'), Var('K3'))
        assert a == b

        a = parse(r''' O MLTK K ''')
        b = KetApply(Var('O'), Var('K'))
        assert a == b

        a = parse(r''' K1 TSRK K2 ''')
        b = KetTensor(Var('K1'), Var('K2'))
        assert a == b

def test_basic_B():
    with wolfram_backend.wolfram_session():
        a = parse(r'''0X''')
        b = Zero()
        assert a == b

        a = parse(r''' BRA(s) ''')
        b = BraBase(Var('s'))
        assert a == b

        a = parse(r''' ADJ(s) ''')
        b = Adj(Var('s'))
        assert a == b
        
        a = parse(r''' S SCR B ''')
        b = Scal(Var('S'), Var('B'))
        assert a == b

        a = parse(r''' B1 ADD B2 ADD B3 ''')
        b = Add(Var('B1'), Var('B2'), Var('B3'))
        assert a == b

        a = parse(r''' B MLTB O ''')
        b = BraApply(Var('B'), Var('O'))
        assert a == b

        a = parse(r''' B1 TSRB B2 ''')
        b = BraTensor(Var('B1'), Var('B2'))
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
        b = OpOuter(Var('K'), Var('B'))
        assert a == b

        a = parse(r''' ADJ(O)''')
        b = Adj(Var('O'))
        assert a == b
        
        a = parse(r''' S SCR O ''')
        b = Scal(Var('S'), Var('O'))
        assert a == b

        a = parse(r''' O1 ADD O2 ADD O3 ''')
        b = Add(Var('O1'), Var('O2'), Var('O3'))
        assert a == b

        a = parse(r''' O1 MLTO O2 ''')
        b = OpApply(Var('O1'), Var('O2'))
        assert a == b

        a = parse(r''' O1 TSRO O2 ''')
        b = OpTensor(Var('O1'), Var('O2'))
        assert a == b

def test_subst():
    with wolfram_backend.wolfram_session():
        a = parse(r'''{
            s : KET(a);
            t : BRA(b);
        }''')
        b = Subst({
            "s" : KetBase(Var('a')),
            "t" : BraBase(Var('b')),
        })
        assert a == b
