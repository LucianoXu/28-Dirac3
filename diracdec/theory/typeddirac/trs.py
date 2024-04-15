
'''
all the rewriting rules for Dirac notation
'''

from __future__ import annotations

from typing import Type

from ..trs import *
from .syntax import *

from .parser_build import parser, parse



#####################################################################
# typing rules

type_checker = TypeChecker([])

type_checker.append(
    TypingRule(
        "TYPING-CADD",
        lhs = parse("(a : CS) CADD (b : CS)"),
        rhs = parse("(a : CS) CADD (b : CS) : CS")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-CMUL",
        lhs = parse("(a : CS) CMUL (b : CS)"),
        rhs = parse("(a : CS) CMUL (b : CS) : CS")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-C0",
        lhs = parse("C0"),
        rhs = parse("C0 : CS")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-C1",
        lhs = parse("C1"),
        rhs = parse("C1 : CS")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-CADJ",
        lhs = parse("CADJ(a : CS)"),
        rhs = parse("CADJ(a : CS) : CS")
    )
)


type_checker.append(
    TypingRule(
        "TYPING-COMPLEX",
        lhs = parse("C(c : CS)"),
        rhs = parse("C(c : CS) : S")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-PAIR",
        lhs = parse("PAIR(x : T1, y : T2)"),
        rhs = parse("PAIR(x : T1, y : T2) : T1 ^ T2")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-FIRST",
        lhs = parse("FST(x : T1 ^ T2)"),
        rhs = parse("FST(x : T1 ^ T2) : T1")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-SECOND",
        lhs = parse("SND(x : T1 ^ T2)"),
        rhs = parse("SND(x : T1 ^ T2) : T2")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-DELTA",
        lhs = parse("DELTA(x : T, y : T)"),
        rhs = parse("DELTA(x : T, y : T) : S")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-0S",
        lhs = parse("0S"),
        rhs = parse("0S : S")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-0K",
        lhs = parse("0K(T)"),
        rhs = parse("0K(T) : K(T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-0B",
        lhs = parse("0B(T)"),
        rhs = parse("0B(T) : B(T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-0O",
        lhs = parse("0O(T1, T2)"),
        rhs = parse("0O(T1, T2) : O(T1, T2)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-1S",
        lhs = parse("1S"),
        rhs = parse("1S : S")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-1O",
        lhs = parse("1O(T)"),
        rhs = parse("1O(T) : O(T, T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-KET",
        lhs = parse("|x : T>"),
        rhs = parse("|x : T> : K(T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-BRA",
        lhs = parse("<x : T|"),
        rhs = parse("<x : T| : B(T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-ADJS",
        lhs = parse("ADJ(x : S)"),
        rhs = parse("ADJ(x : S) : S")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-ADJK",
        lhs = parse("ADJ(x : K(T))"),
        rhs = parse("ADJ(x : K(T)) : B(T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-ADJB",
        lhs = parse("ADJ(x : B(T))"),
        rhs = parse("ADJ(x : B(T)) : K(T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-ADJO",
        lhs = parse("ADJ(x : O(T1, T2))"),
        rhs = parse("ADJ(x : O(T1, T2)) : O(T2, T1)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-MUL",
        lhs = parse("(x : S) * (y : S)"),
        rhs = parse("(x : S) * (y : S) : S")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-SCLK",
        lhs = parse("(x : S) . (k : K(T))"),
        rhs = parse("(x : S) . (k : K(T)) : K(T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-SCLB",
        lhs = parse("(x : S) . (b : B(T))"),
        rhs = parse("(x : S) . (b : B(T)) : B(T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-SCLO",
        lhs = parse("(x : S) . (o : O(T1, T2))"),
        rhs = parse("(x : S) . (o : O(T1, T2)) : O(T1, T2)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-ADDS",
        lhs = parse("(x : S) + (y : S)"),
        rhs = parse("(x : S) + (y : S) : S")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-ADDK",
        lhs = parse("(x : K(T)) + (y : K(T))"),
        rhs = parse("(x : K(T)) + (y : K(T)) : K(T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-ADDB",
        lhs = parse("(x : B(T)) + (y : B(T))"),
        rhs = parse("(x : B(T)) + (y : B(T)) : B(T)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-ADDO",
        lhs = parse("(x : O(T1, T2)) + (y : O(T1, T2))"),
        rhs = parse("(x : O(T1, T2)) + (y : O(T1, T2)) : O(T1, T2)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-DOTBK",
        lhs = parse("(b : B(T)) @ (k : K(T))"),
        rhs = parse("(b : B(T)) @ (k : K(T)) : S")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-DOTOK",
        lhs = parse("(o : O(T1, T2)) @ (k : K(T2))"),
        rhs = parse("(o : O(T1, T2)) @ (k : K(T2)) : K(T1)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-DOTBO",
        lhs = parse("(b : B(T1)) @ (o : O(T1, T2))"),
        rhs = parse("(b : B(T1)) @ (o : O(T1, T2)) : B(T2)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-DOTOO",
        lhs = parse("(o1 : O(T1, T2)) @ (o2 : O(T2, T3))"),
        rhs = parse("(o1 : O(T1, T2)) @ (o2 : O(T2, T3)) : O(T1, T3)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-TSRKB",
        lhs = parse("(k : K(T1)) & (b : B(T2))"),
        rhs = parse("(k : K(T1)) & (b : B(T2)) : O(T1, T2)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-TSRKK",
        lhs = parse("(k1 : K(T1)) & (k2 : K(T2))"),
        rhs = parse("(k1 : K(T1)) & (k2 : K(T2)) : K(T1 ^ T2)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-TSRBB",
        lhs = parse("(b1 : B(T1)) & (b2 : B(T2))"),
        rhs = parse("(b1 : B(T1)) & (b2 : B(T2)) : B(T1 ^ T2)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-TSROO",
        lhs = parse("(o1 : O(X1, X2)) & (o2 : O(Y1, Y2))"),
        rhs = parse("(o1 : O(X1, X2)) & (o2 : O(Y1, Y2)) : O(X1 ^ Y1, X2 ^ Y2)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-TSROK",
        lhs = parse("(o : O(T1, T2)) & (k : K(X))"),
        rhs = parse("(o : O(T1, T2)) & (k : K(X)) : O(T1 ^ X, T2)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-TSRKO",
        lhs = parse("(k : K(X)) & (o : O(T1, T2))"),
        rhs = parse("(k : K(X)) & (o : O(T1, T2)) : O(X ^ T1, T2)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-TSROB",
        lhs = parse("(o : O(T1, T2)) & (b : B(X))"),
        rhs = parse("(o : O(T1, T2)) & (b : B(X)) : O(T1, T2 ^ X)")
    )
)

type_checker.append(
    TypingRule(
        "TYPING-TSRBO",
        lhs = parse("(b : B(X)) & (o : O(T1, T2))"),
        rhs = parse("(b : B(X)) & (o : O(T1, T2)) : O(T1, X ^ T2)")
    )
)


######################################################################
# typed rewriting

# typed trs
typed_trs = TypedTRS(type_checker, [])


#########################
# Complex Scalar Avatar
# 

typed_trs.append_canonical(
    "CS-1",
    lhs = parse("C0 CADD (a : CS)"),
    rhs = parse("a : CS"),
)

typed_trs.append_canonical(
    "CS-2",
    lhs = parse("C0 CMUL (a : CS)"),
    rhs = parse("C0"),
)

typed_trs.append_canonical(
    "CS-3",
    lhs = parse("C1 CMUL (a : CS)"),
    rhs = parse("a : CS"),
)

typed_trs.append_canonical(
    "CS-4",
    lhs = parse("(a : CS) CMUL ((b : CS) CADD (c : CS))"),
    rhs = parse("((a : CS) CMUL (b : CS)) CADD ((a : CS) CMUL (c : CS))"),
)

typed_trs.append_canonical(
    "CS-5",
    lhs = parse("CADJ(C0)"),
    rhs = parse("C0"),
)

typed_trs.append_canonical(
    "CS-6",
    lhs = parse("CADJ(C1)"),
    rhs = parse("C1"),
)

typed_trs.append_canonical(
    "CS-7",
    lhs = parse("CADJ((a : CS) CADD (b : CS))"),
    rhs = parse("CADJ(a : CS) CADD CADJ(b : CS)"),
)

typed_trs.append_canonical(
    "CS-8",
    lhs = parse("CADJ((a : CS) CMUL (b : CS))"),
    rhs = parse("CADJ(a : CS) CMUL CADJ(b : CS)"),
)

typed_trs.append_canonical(
    "CS-9",
    lhs = parse("CADJ(CADJ(a : CS))"),
    rhs = parse("a : CS"),
)

# ################
# # Scalar Sort
# #

# typed_trs.append_canonical(
#     "SCR-1",
#     lhs = parse("C(C0) + (s : S)"),
#     rhs = parse("s : S")
# )

# typed_trs.append(
#     CanonicalRule(
#         "SCR-2",
#         lhs = parse("C(a : CS) + C(b : CS)"),
#         rhs = parse("C((a : CS) CADD (b : CS))")
#     )
# )

# typed_trs.append_canonical(
#     "SCR-3",
#     lhs = parse("(s : S) + (s : S)"),
#     rhs = parse("C(C1 CADD C1) * (s : S)")
# )

# typed_trs.append_canonical(
#     "SCR-4",
#     lhs = parse("C(a : CS) * (s : S) + (s : S)"),
#     rhs = parse("C(C1 CADD (a : CS)) * (s : S)")
# )

# typed_trs.append_canonical(
#     "SCR-5",
#     lhs = parse("C(a : CS) * (s : S) + C(b : CS) * (s : S)"),
#     rhs = parse("C((a : CS) CADD (b : CS)) * (s : S)")
# )

# typed_trs.append_canonical(
#     "SCR-6",
#     lhs = parse("C(C0) * (s : S)"),
#     rhs = parse("C(C0)")
# )

# typed_trs.append_canonical(
#     "SCR-7",
#     lhs = parse("C(C1) * (s : S)"),
#     rhs = parse("s : S")
# )

# typed_trs.append_canonical(
#     "SCR-8",
#     lhs = parse("C(a : CS) * C(b : CS)"),
#     rhs = parse("C((a : CS) CMUL (b : CS))")
# )

# typed_trs.append_canonical(
#     "SCR-9",
#     lhs = parse("(s1 : S) * ((s2 : S) + (s3 : S))"),
#     rhs = parse("(s1 : S) * (s2 : S) + (s1 : S) * (s3 : S)")
# )

# typed_trs.append_canonical(
#     "SCR-10",
#     lhs = parse("ADJ(C(a : CS))"),
#     rhs = parse("C(CADJ(a : CS))")
# )

# typed_trs.append(
#     CanonicalRule(
#         "SCR-11",
#         lhs = parse("ADJ(DELTA(x : T, y : T))"),
#         rhs = parse("DELTA(x : T, y : T)")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "SCR-12",
#         lhs = parse("ADJ((x : S) + (y : S))"),
#         rhs = parse("ADJ(x : S) + ADJ(y : S)")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "SCR-13",
#         lhs = parse("ADJ((x : S) * (y : S))"),
#         rhs = parse("ADJ(x : S) * ADJ(y : S)")
#     )
# )
# typed_trs.append(
#     CanonicalRule(
#         "SCR-14",
#         lhs = parse("ADJ(ADJ(s : S))"),
#         rhs = parse("s : S")
#     )
# )





# typed_trs.append(
#     CanonicalRule(
#         "BASE-FST",
#         lhs = parse("FST(PAIR(x : T1, y : T2))"),
#         rhs = parse("x : T1")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "BASE-SND",
#         lhs = parse("SND(PAIR(x : T1, y : T2))"),
#         rhs = parse("y : T2")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "BASE-PAIR",
#         lhs = parse("PAIR(FST(p : T1 ^ T2), SND(p : T1 ^ T2))"),
#         rhs = parse("p : T1 ^ T2")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DELTA-1",
#         lhs = parse("DELTA(u : U ^ V, PAIR(x : U, y : V))"),
#         rhs = parse("DELTA(FST(u : U ^ V), x : U) * DELTA(SND(u : U ^ V), y : V)")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DELTA-2",
#         lhs = parse("DELTA(FST(u : U ^ V), FST(v : U ^ V)) * DELTA(SND(u : U ^ V), SND(v : U ^ V))"),
#         rhs = parse("DELTA(u : U ^ V, v : U ^ V)")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "ADJS-1",
#         lhs = parse("ADJ(0S)"),
#         rhs = parse("0S")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "ADJS-2",
#         lhs = parse("ADJ(1S)"),
#         rhs = parse("1S")
#     )
# )




# typed_trs.append(
#     CanonicalRule(
#         "ADJS_7",
#         lhs = parse("ADJ((b : B(T)) @ (k : K(T)))"),
#         rhs = parse("ADJ(k : K(T)) @ ADJ(b : B(T))")
#     )
# )


# typed_trs.append(
#     CanonicalRule(
#         "DOTBK-1",
#         lhs = parse("0B(T) @ (k : K(T))"),
#         rhs = parse("0S")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOTBK-2",
#         lhs = parse("(b : B(T)) @ 0K(T)"),
#         rhs = parse("0S")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOTBK-3",
#         lhs = parse("((s : S) . (b : B(T))) @ (k : K(T))"),
#         rhs = parse("(s : S) * ((b : B(T)) @ (k : K(T)))")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOTBK-4",
#         lhs = parse("(b : B(T)) @ ((s : S) . (k : K(T)))"),
#         rhs = parse("(s : S) * ((b : B(T)) @ (k : K(T)))")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOTBK-5",
#         lhs = parse("((b1 : B(T)) + (b2 : B(T))) @ (k : K(T))"),
#         rhs = parse("((b1 : B(T)) @ (k : K(T))) + ((b2 : B(T)) @ (k : K(T)))")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOTBK-6",
#         lhs = parse("(b : B(T)) @ ((k1 : K(T)) + (k2 : K(T)))"),
#         rhs = parse("((b : B(T)) @ (k1 : K(T))) + ((b : B(T)) @ (k2 : K(T)))")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOTBK-7",
#         lhs = parse("<s : T| @ |t : T>"),
#         rhs = parse("DELTA(s : T, t : T)")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOTBK-8",
#         lhs = parse("(b1 : B(T1)) & (b2 : B(T2)) @ |s : T1 ^ T2>"),
#         rhs = parse("((b1 : B(T1)) @ | FST(s : T1 ^ T2) >) * ((b2 : B(T2)) @ | SND(s : T1 ^ T2) >)")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOTBK-9",
#         lhs = parse("< s : T1 ^ T2| @ (k1 : K(T1)) & (k2 : K(T2))"),
#         rhs = parse("(< FST(s : T1 ^ T2) | @ (k1 : K(T1))) * (< SND(s : T1 ^ T2) | @ (k2 : K(T2)))")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOTBK-10",
#         lhs = parse("(b1 : B(T1)) & (b2 : B(T2)) @ (k1 : K(T1)) & (k2 : K(T2))"),
#         rhs = parse("((b1 : B(T1)) @ (k1 : K(T1))) * ((b2 : B(T2)) @ (k2 : K(T2)))")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOT-SORT-1",
#         lhs = parse("((a : B(T1)) @ (b : O(T1, T2))) @ (c : K(T2))"),
#         rhs = parse("(a : B(T1)) @ ((b : O(T1, T2)) @ (c : K(T2)))")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOT-SORT-2",
#         lhs = parse(
#             '''
#               < s : U ^ V | 
#               @ (
#                     (
#                         (o1 : O(U, W)) & 
#                         (o2 : O(V, R))
#                     ) @ (k : K(W ^ R))
#               )
#               '''        
#         ),
#         rhs = parse("(< FST(s : U ^ V) | @ (o1 : O(U, W))) & (< SND(s : U ^ V) | @ (o2 : O(V, R))) @ (k : K(W ^ R))")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "DOT-SORT-3",
#         lhs = parse(
#             '''
#               (b1 : B(U)) & (b2 : B(V))
#               @ (
#                     (
#                         (o1 : O(U, W)) & 
#                         (o2 : O(V, R))
#                     ) @ (k : K(W ^ R))
#               )
#               '''        
#         ),
#         rhs = parse("((b1 : B(U)) @ (o1 : O(U, W))) & ((b2 : B(V)) @ (o2 : O(V, R))) @ (k : K(W ^ R))")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "ADJ-0K",
#         lhs = parse("ADJ(0K(T))"),
#         rhs = parse("0B(T)")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "ADJ-0B",
#         lhs = parse("ADJ(0B(T))"),
#         rhs = parse("0K(T)")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "ADJ-0O",
#         lhs = parse("ADJ(0O(T1, T2))"),
#         rhs = parse("0O(T2, T1)")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "ADJ-1O",
#         lhs = parse("ADJ(1O(T))"),
#         rhs = parse("1O(T)")
#     )
# )

# typed_trs.append(
#     CanonicalRule(
#         "ADJ-SCAL",
#         lhs = parse("ADJ((s : S) . (d : K(T)))"),
#         rhs = parse("ADJ(s : S) . ADJ(d : K(T))")
#     )
# )



