from diracdec.theory.typeddirac import *

def test_parsing():
    pass


def test_typing_pair():
    a = parse("PAIR((a : X), (b : Y))")
    typed = parse("(PAIR((a : X), (b : Y)) : (X ^ Y))")
    assert type_checker.normalize(a) == typed

def test_typing_first():
    a = parse("FST((a : (X ^ Y)))")
    typed = parse("(FST((a : (X ^ Y))) : X)")
    assert type_checker.normalize(a) == typed

def test_typing_second():
    a = parse("SND((a : (X ^ Y)))")
    typed = parse("(SND((a : (X ^ Y))) : Y)")
    assert type_checker.normalize(a) == typed

def test_typing_delta():
    a = parse("DELTA((a : X), (b : X))")
    typed = parse("(DELTA((a : X), (b : X)) : S)")
    assert type_checker.normalize(a) == typed

def test_typing_0S():
    a = parse("0S")
    typed = parse("(0S : S)")
    assert type_checker.normalize(a) == typed

def test_typing_0K():
    a = parse("0K(X)")
    typed = parse("(0K(X) : K(X))")
    assert type_checker.normalize(a) == typed

def test_typing_0B():
    a = parse("0B(X)")
    typed = parse("(0B(X) : B(X))")
    assert type_checker.normalize(a) == typed

def test_typing_0O():
    a = parse("0O(X, Y)")
    typed = parse("(0O(X, Y) : O(X, Y))")
    assert type_checker.normalize(a) == typed

def test_typing_1S():
    a = parse("1S")
    typed = parse("(1S : S)")
    assert type_checker.normalize(a) == typed

def test_typing_1O():
    a = parse("1O(X)")
    typed = parse("(1O(X) : O(X, X))")
    assert type_checker.normalize(a) == typed

def test_typing_ket():
    a = parse("|x : X>")
    typed = parse("|x : X> : K(X)")
    assert type_checker.normalize(a) == typed

def test_typing_bra():
    a = parse("<x : X|")
    typed = parse("<x : X| : B(X)")
    assert type_checker.normalize(a) == typed

def test_typing_adjs():
    a = parse("ADJ(x : S)")
    typed = parse("ADJ(x : S) : S")
    assert type_checker.normalize(a) == typed

def test_typing_adjk():
    a = parse("ADJ(x : K(X))")
    typed = parse("ADJ(x : K(X)) : B(X)")
    assert type_checker.normalize(a) == typed

def test_typing_adjb():
    a = parse("ADJ(x : B(X))")
    typed = parse("ADJ(x : B(X)) : K(X)")
    assert type_checker.normalize(a) == typed

def test_typing_adjo():
    a = parse("ADJ(x : O(X, Y))")
    typed = parse("ADJ(x : O(X, Y)) : O(Y, X)")
    assert type_checker.normalize(a) == typed

def test_typing_mul():
    a = parse("(x : S) * (y : S)")
    typed = parse("(x : S) * (y : S) : S")
    assert type_checker.normalize(a) == typed

    a = parse("(x : S) * (y : S) * (z : S)")
    typed = parse("(x : S) * (y : S)  * (z : S) : S")
    assert type_checker.normalize(a) == typed

def test_typing_sclk():
    a = parse("(x : S) . (y : K(X))")
    typed = parse("(x : S) . (y : K(X)) : K(X)")
    assert type_checker.normalize(a) == typed

def test_typing_sclb():
    a = parse("(x : S) . (y : B(X))")
    typed = parse("(x : S) . (y : B(X)) : B(X)")
    assert type_checker.normalize(a) == typed

def test_typing_sclo():
    a = parse("(x : S) . (y : O(X, Y))")
    typed = parse("(x : S) . (y : O(X, Y)) : O(X, Y)")
    assert type_checker.normalize(a) == typed

def test_typing_adds():
    a = parse("(x : S) + (y : S)")
    typed = parse("(x : S) + (y : S) : S")
    assert type_checker.normalize(a) == typed

def test_typing_addk():
    a = parse("(x : K(X)) + (y : K(X))")
    typed = parse("(x : K(X)) + (y : K(X)) : K(X)")
    assert type_checker.normalize(a) == typed

def test_typing_addb():
    a = parse("(x : B(X)) + (y : B(X))")
    typed = parse("(x : B(X)) + (y : B(X)) : B(X)")
    assert type_checker.normalize(a) == typed

def test_typing_addo():
    a = parse("(x : O(X, Y)) + (y : O(X, Y))")
    typed = parse("(x : O(X, Y)) + (y : O(X, Y)) : O(X, Y)")
    assert type_checker.normalize(a) == typed

def test_typing_dotbk():
    a = parse("(b : B(T)) @ (k : K(T))")
    typed = parse("(b : B(T)) @ (k : K(T)) : S")
    assert type_checker.normalize(a) == typed

def test_typing_dotok():
    a = parse("(o : O(T1, T2)) @ (k : K(T2))")
    typed = parse("(o : O(T1, T2)) @ (k : K(T2)) : K(T1)")
    assert type_checker.normalize(a) == typed

def test_typing_dotbo():
    a = parse("(b : B(T1)) @ (o : O(T1, T2))")
    typed = parse("(b : B(T1)) @ (o : O(T1, T2)) : B(T2)")
    assert type_checker.normalize(a) == typed

def test_typing_dotoo():
    a = parse("(o1 : O(T1, T2)) @ (o2 : O(T2, T3))")
    typed = parse("(o1 : O(T1, T2)) @ (o2 : O(T2, T3)) : O(T1, T3)")
    assert type_checker.normalize(a) == typed

def test_typing_tsrkb():
    a = parse("(k : K(T1)) & (b : B(T2))")
    typed = parse("(k : K(T1)) & (b : B(T2)) : O(T1, T2)")
    assert type_checker.normalize(a) == typed

def test_typing_tsrkk():
    a = parse("(k1 : K(T1)) & (k2 : K(T2))")
    typed = parse("(k1 : K(T1)) & (k2 : K(T2)) : K(T1 ^ T2)")
    assert type_checker.normalize(a) == typed

def test_typing_tsrbb():
    a = parse("(b1 : B(T1)) & (b2 : B(T2))")
    typed = parse("(b1 : B(T1)) & (b2 : B(T2)) : B(T1 ^ T2)")
    assert type_checker.normalize(a) == typed

def test_typing_tsroo():
    a = parse("(o1 : O(X1, X2)) & (o2 : O(Y1, Y2))")
    typed = parse("(o1 : O(X1, X2)) & (o2 : O(Y1, Y2)) : O(X1 ^ Y1, X2 ^ Y2)")
    assert type_checker.normalize(a) == typed

def test_typing_tsrok():
    a = parse("(o : O(X1, X2)) & (k : K(Y))")
    typed = parse("(o : O(X1, X2)) & (k : K(Y)) : O(X1 ^ Y, X2)")
    assert type_checker.normalize(a) == typed

def test_typing_tsrko():
    a = parse("(k : K(Y)) & (o : O(X1, X2))")
    typed = parse("(k : K(Y)) & (o : O(X1, X2)) : O(Y ^ X1, X2)")
    assert type_checker.normalize(a) == typed

def test_typing_tsrob():
    a = parse("(o : O(X1, X2)) & (b : B(Y))")
    typed = parse("(o : O(X1, X2)) & (b : B(Y)) : O(X1, X2 ^ Y)")
    assert type_checker.normalize(a) == typed

def test_typing_tsrbo():
    a = parse("(b : B(Y)) & (o : O(X1, X2))")
    typed = parse("(b : B(Y)) & (o : O(X1, X2)) : O(X1, Y ^ X2)")
    assert type_checker.normalize(a) == typed

