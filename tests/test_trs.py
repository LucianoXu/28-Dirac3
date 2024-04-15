from diracdec import *
from diracdec.theory.trs import *

from diracdec import parse

def test_bind_alpha_conv():
    a = BindVarTerm(Var("x"), Var("x"))
    b = BindVarTerm(Var("y"), Var("y"))
    assert a == b

    a = BindVarTerm(Var("x"), Var("z"))
    b = BindVarTerm(Var("y"), Var("z"))
    assert a == b

def test_bind_substitute():
    sub = Subst({
        Var("a") : Var("z"),
    })
    a = BindVarTerm(Var("a"), Var("a"))
    assert sub(a) == a

    a = BindVarTerm(Var("b"), Var("a"))
    b = BindVarTerm(Var("c"), Var("z"))
    assert sub(a) == b


    a = BindVarTerm(Var("z"), Var("a"))
    b = BindVarTerm(Var("y"), Var("z"))
    assert sub(a) == b


def test_typing_mechanism():

    class Add(StdTerm):
        fsymbol_print = '+'
        fsymbol = 'ADD'

        def __init__(self, a: Term, b: Term):
            super().__init__(a, b)
            self.a = a
            self.b = b

        def __str__(self) -> str:
            return str(ParenBlock(HSeqBlock(
                str(self.a), " + ", str(self.b),
                v_align='c'
            )))

        def __repr__(self) -> str:
            return rf'({repr(self.a)} + {repr(self.b)})'

        def tex(self) -> str:
            return rf' \left ( {self.a} + {self.b} \right )'

        def __eq__(self, __value: Term) -> bool:
            return isinstance(__value, Add) and self.a == __value.a and self.b == __value.b

        def size(self) -> int:
            return self.a.size() + self.b.size() + 1

        def variables(self) -> set[Var]:
            return self.a.variables() | self.b.variables()

        def subst(self, sigma: Subst | dict[Var, Term]) -> Term:
            return Add(self.a.subst(sigma), self.b.subst(sigma))
        
    class Sca(TypeTerm, StdTerm):
        fsymbol_print = 'sca'
        fsymbol = 'S'

        def __init__(self):
            super().__init__()

        def tex(self) -> str:
            raise NotImplementedError()
        
        def subst(self, sigma: Subst | dict[Var, Term]) -> TypeTerm:
            return StdTerm.subst(self, sigma) # type: ignore


    class Zero(TypeTerm, StdTerm):
        fsymbol_print = '0'
        fsymbol = 'Z'

        def __init__(self):
            super().__init__()

        def tex(self) -> str:
            raise NotImplementedError()
        
        def subst(self, sigma: Subst | dict[Var, Term]) -> TypeTerm:
            return StdTerm.subst(self, sigma) # type: ignore
    
    type_checker = TypeChecker([])

    type_checker.append(
        TypingRule(
            "TYPING-ADD",
            lhs = Add(Typing(Var('a'), Sca()), Typing(Var('b'), Sca())),
            rhs = Typing(Add(Typing(Var('a'), Sca()), Typing(Var('b'), Sca())), Sca())
        )
    )


    type_checker.append(
        TypingRule(
            "TYPING-ZERO",
            lhs = Zero(),
            rhs = Typing(Zero(), Sca())
        )
    )


    a = Add(Typing(Var('a'), Sca()), Typing(Var('b'), Sca()))
    b = Typing(Add(Typing(Var('a'), Sca()), Typing(Var('b'), Sca())), Sca())
    assert type_checker.normalize(a) == b

    a = Add(Typing(Var('a'), Sca()), Add(Typing(Var('a'), Sca()), Typing(Var('b'), Sca())))
    b = Typing(
            Add(Typing(Var('a'), Sca()), 
                Typing(
                    Add(
                        Typing(Var('a'), Sca()), 
                        Typing(Var('b'), Sca())),
                    Sca()
                    )
                ), 
            Sca()
        )
    assert type_checker.normalize(a) == b

    # typed trs
    trs = TypedTRS(type_checker, [])

    trs.append(
        CanonicalRule(
            "ADD-0",
            lhs = Add(Typing(Var('a'), Sca()), Zero()),
            rhs = Typing(Var('a'), Sca())
        )
    )

    a = Add(Typing(Var('a'), Sca()), Zero())
    checked_a = trs.type_checking(a)
    assert trs.normalize(checked_a, verbose=True) == Typing(Var('a'), Sca())




