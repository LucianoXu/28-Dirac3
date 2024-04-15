from diracdec.theory.typeddirac import *

####################################################
# rewriting

def test_rule_base_fst():
    a = parse("FST(PAIR(x : T1, y : T2))")
    b = parse("x : T1")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_base_snd():
    a = parse("SND(PAIR(x : T1, y : T2))")
    b = parse("y : T2")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_base_pair():
    a = parse("PAIR(FST(p : T1 ^ T2), SND(p : T1 ^ T2))")
    b = parse("p : (T1 ^ T2)")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_delta_1():
    a = parse("DELTA(u : U ^ V, PAIR(x : U, y : V))")
    b = parse("DELTA(FST(u : U ^ V), x : U) * DELTA(SND(u : U ^ V), y : V)")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_delta_2():
    a = parse("DELTA(FST(u : U ^ V), FST(v : U ^ V)) * DELTA(SND(u : U ^ V), SND(v : U ^ V))")
    b = parse("DELTA(u : U ^ V, v : U ^ V)")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_adjs_1():
    a = parse("ADJ(0S)")
    b = parse("0S")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_adjs_2():
    a = parse("ADJ(1S)")
    b = parse("1S")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_adjs_3():
    a = parse("ADJ(DELTA(x : T, y : T))")
    b = parse("DELTA(x : T, y : T)")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_adj_adj():
    a = parse("ADJ(ADJ(x : T))")
    b = parse("x : T")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_adjs_5():
    a = parse("ADJ((x : S) + (y : S))")
    b = parse("ADJ(x : S) + ADJ(y : S)")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_adjs_6():
    a = parse("ADJ((x : S) * (y : S))")
    b = parse("ADJ(x : S) * ADJ(y : S)")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_adjs_7():
    a = parse("ADJ((b : B(T)) @ (k : K(T)))")
    b = parse("ADJ(k : K(T)) @ ADJ(b : B(T))")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dotbk_1():
    a = parse("0B(T) @ (k : K(T))")
    b = parse("0S")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dotbk_2():
    a = parse("(b : B(T)) @ 0K(T)")
    b = parse("0S")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dotbk_3():
    a = parse("((s : S) . (b : B(T))) @ (k : K(T))")
    b = parse("(s : S) . ((b : B(T)) @ (k : K(T)))")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dotbk_4():
    a = parse("(b : B(T)) @ ((s : S) . (k : K(T)))")
    b = parse("(s : S) . ((b : B(T)) @ (k : K(T)))")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dotbk_5():
    a = parse("((b1 : B(T)) + (b2 : B(T))) @ (k : K(T))")
    b = parse("((b1 : B(T)) @ (k : K(T))) + ((b2 : B(T)) @ (k : K(T)))")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dotbk_6():
    a = parse("(b : B(T)) @ ((k1 : K(T)) + (k2 : K(T)))")
    b = parse("((b : B(T)) @ (k1 : K(T))) + ((b : B(T)) @ (k2 : K(T)))")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dotbk_7():
    a = parse("<s : T| @ |t : T>")
    b = parse("DELTA(s : T, t : T)")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dotbk_8():
    a = parse("(b1 : B(T1)) & (b2 : B(T2)) @ |s : T1 ^ T2>")
    b = parse("((b1 : B(T1)) @ | FST(s : T1 ^ T2) >) * ((b2 : B(T2)) @ | SND(s : T1 ^ T2) >)")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dotbk_9():
    a = parse("< s : T1 ^ T2| @ (k1 : K(T1)) & (k2 : K(T2))")
    b = parse("(< FST(s : T1 ^ T2) | @ (k1 : K(T1))) * (< SND(s : T1 ^ T2) | @ (k2 : K(T2)))")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dotbk_10():
    a = parse("(b1 : B(T1)) & (b2 : B(T2)) @ (k1 : K(T1)) & (k2 : K(T2))")
    b = parse("((b1 : B(T1)) @ (k1 : K(T1))) * ((b2 : B(T2)) @ (k2 : K(T2)))")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)


def test_rule_dot_sort_1():
    a = parse("((a : U) @ (b : V)) @ (c : W)")
    b = parse("(a : U) @ ((b : V) @ (c : W))")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dot_sort_2():
    a = parse(
        '''
          < s : U ^ V | 
          @ (
                (
                    (o1 : O(U, W)) & 
                    (o2 : O(V, R))
                ) @ (k : K(W ^ R))
          )
          '''        
    )
    b = parse("(< FST(s : U ^ V) | @ (o1 : O(U, W))) & (< SND(s : U ^ V) | @ (o2 : O(V, R))) @ (k : K(W ^ R))")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)

def test_rule_dot_sort_3():
    a = parse(
        '''
          (b1 : B(U)) & (b2 : B(V))
          @ (
                (
                    (o1 : O(U, W)) & 
                    (o2 : O(V, R))
                ) @ (k : K(W ^ R))
          )
          '''        
    )
    b = parse("((b1 : B(U)) @ (o1 : O(U, W))) & ((b2 : B(V)) @ (o2 : O(V, R))) @ (k : K(W ^ R))")
    assert typed_trs.normalize(a) == typed_trs.normalize(b)