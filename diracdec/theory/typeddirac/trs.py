
'''
all the rewriting rules for Dirac notation
'''

from __future__ import annotations

from typing import Type

from ..trs import *
from .syntax import *

from .parser_build import parser, parse

typing_trs = TypeChecker([])

typing_trs.append(
    TypingRule(
        "TYPING-PAIR",
        lhs = parse("PAIR(x : T1, y : T2)"),
        rhs = parse("PAIR(x : T1, y : T2) : T1 ^ T2")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-FIRST",
        lhs = parse("FST(x : T1 ^ T2)"),
        rhs = parse("FST(x : T1 ^ T2) : T1")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-SECOND",
        lhs = parse("SND(x : T1 ^ T2)"),
        rhs = parse("SND(x : T1 ^ T2) : T2")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-DELTA",
        lhs = parse("DELTA(x : T, y : T)"),
        rhs = parse("DELTA(x : T, y : T) : S")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-0S",
        lhs = parse("0S"),
        rhs = parse("0S : S")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-0K",
        lhs = parse("0K(T)"),
        rhs = parse("0K(T) : K(T)")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-0B",
        lhs = parse("0B(T)"),
        rhs = parse("0B(T) : B(T)")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-0O",
        lhs = parse("0O(T1, T2)"),
        rhs = parse("0O(T1, T2) : O(T1, T2)")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-1S",
        lhs = parse("1S"),
        rhs = parse("1S : S")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-1O",
        lhs = parse("1O(T)"),
        rhs = parse("1O(T) : O(T, T)")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-KET",
        lhs = parse("|x : T>"),
        rhs = parse("|x : T> : K(T)")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-BRA",
        lhs = parse("<x : T|"),
        rhs = parse("<x : T| : B(T)")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-ADJS",
        lhs = parse("ADJ(x : S)"),
        rhs = parse("ADJ(x : S) : S")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-ADJK",
        lhs = parse("ADJ(x : K(T))"),
        rhs = parse("ADJ(x : K(T)) : B(T)")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-ADJB",
        lhs = parse("ADJ(x : B(T))"),
        rhs = parse("ADJ(x : B(T)) : K(T)")
    )
)

typing_trs.append(
    TypingRule(
        "TYPING-ADJO",
        lhs = parse("ADJ(x : O(T1, T2))"),
        rhs = parse("ADJ(x : O(T1, T2)) : O(T2, T1)")
    )
)

# typing_trs.append(
#     TypingRule(
#         "TYPING-MUL",
#         lhs = parse("(x : S) * (y : S)"),
#         rhs = parse("(x : S) * (y : S) : S")
#     )
# )


