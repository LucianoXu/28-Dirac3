# from wolframclient.evaluation import WolframLanguageSession
# from wolframclient.language import wl, wlexpr
# session = WolframLanguageSession()

# print(session.evaluate(wlexpr('Range[5]')))
# session.terminate()

from diracdec import *
from diracdec import parse as parse, dirac_bigop_delta_trs as trs, label_trs

from diracdec.theory.trs import *

trs = trs + label_trs

from qwhile import parse, forward_trs
from qwhile.forward import CfgSet


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
    ))

type_checker.append(
    TypingRule(
        "TYPING-ZERO",
        lhs = Zero(),
        rhs = Typing(Zero(), Sca())
    )
)

trs = TypedTRS(type_checker, [])

trs.append(
    CanonicalRule(
        "ADD-0",
        lhs = Add(Typing(Var('a'), Sca()), Zero()),
        rhs = Typing(Var('a'), Sca())
    )
)


if __name__ == "__main__":
    with wolfram_backend.wolfram_session():

        # a = Add(Typing(Var('a'), Sca()), Zero())
        # checked_a = trs.type_checking(a)
        # trs.normalize(checked_a, verbose=True)

        # print(trs.ordered_str())


        # a = Add(Typing(Var('a'), Sca()), Var('a'))
        # checked_a = trs.type_checking(a)
        # trs.normalize(checked_a, verbose=True)

        a = parse(r''' < q :=0 ; , rho > ''')
        b = parse(r''' < HALT , SUM(i, (KET('0') OUTER BRA(i))[q] MLTOL rho MLTOL (KET(i) OUTER BRA('0'))[q]) > ''')
        print(forward_trs.normalize(a))
        print(forward_trs.normalize(b))



