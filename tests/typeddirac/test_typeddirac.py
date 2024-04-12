from diracdec.theory.typeddirac import *

def test_parsing():
    pass


def test_typing_pair():
    a = parse("PAIR((a : X), (b : Y))")
    typed = parse("(PAIR((a : X), (b : Y)) : (X ^ Y))")
    assert typing_trs.normalize(a) == typed

def test_typing_first():
    a = parse("FST((a : (X ^ Y)))")
    typed = parse("(FST((a : (X ^ Y))) : X)")
    assert typing_trs.normalize(a) == typed

def test_typing_second():
    a = parse("SND((a : (X ^ Y)))")
    typed = parse("(SND((a : (X ^ Y))) : Y)")
    assert typing_trs.normalize(a) == typed

def test_typing_delta():
    a = parse("DELTA((a : X), (b : X))")
    typed = parse("(DELTA((a : X), (b : X)) : S)")
    assert typing_trs.normalize(a) == typed

def test_typing_0S():
    a = parse("0S")
    typed = parse("(0S : S)")
    assert typing_trs.normalize(a) == typed

def test_typing_0K():
    a = parse("0K(X)")
    typed = parse("(0K(X) : K(X))")
    assert typing_trs.normalize(a) == typed

def test_typing_0B():
    a = parse("0B(X)")
    typed = parse("(0B(X) : B(X))")
    assert typing_trs.normalize(a) == typed

def test_typing_0O():
    a = parse("0O(X, Y)")
    typed = parse("(0O(X, Y) : O(X, Y))")
    assert typing_trs.normalize(a) == typed

def test_typing_1S():
    a = parse("1S")
    typed = parse("(1S : S)")
    assert typing_trs.normalize(a) == typed

def test_typing_1O():
    a = parse("1O(X)")
    typed = parse("(1O(X) : O(X, X))")
    assert typing_trs.normalize(a) == typed

def test_typing_ket():
    a = parse("|x : X>")
    typed = parse("|x : X> : K(X)")
    assert typing_trs.normalize(a) == typed

def test_typing_bra():
    a = parse("<x : X|")
    typed = parse("<x : X| : B(X)")
    assert typing_trs.normalize(a) == typed

def test_typing_adjs():
    a = parse("ADJ(x : S)")
    typed = parse("ADJ(x : S) : S")
    assert typing_trs.normalize(a) == typed

def test_typing_adjk():
    a = parse("ADJ(x : K(X))")
    typed = parse("ADJ(x : K(X)) : B(X)")
    assert typing_trs.normalize(a) == typed

def test_typing_adjb():
    a = parse("ADJ(x : B(X))")
    typed = parse("ADJ(x : B(X)) : K(X)")
    assert typing_trs.normalize(a) == typed

def test_typing_adjo():
    a = parse("ADJ(x : O(X, Y))")
    typed = parse("ADJ(x : O(X, Y)) : O(Y, X)")
    assert typing_trs.normalize(a) == typed