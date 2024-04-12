from diracdec.theory.typeddirac import *

if __name__ == "__main__":

    a = parse("PAIR(PAIR((a : X), (b : Y)), (c : Z))")
    lhs = parse("0K(T)")
    rhs = parse("(0K : K(T))")
    print(repr(a))
    print(typing_trs.normalize(a, verbose=True))