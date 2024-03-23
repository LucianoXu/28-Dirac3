'''
Equip a type system for term rewriting.
'''
from __future__ import annotations
import sys

from abc import ABC, abstractmethod
from typing import Callable, TextIO, Sequence, Type

from diracdec.theory.trs import Rule, Subst, Term, Var
from .trs import AC, TRS, BindVarTerm, MultiBindTerm, StdTerm, new_var, canonical_rewrite
from diracdec.backends.formprint import *

class TypeTerm(Term):
    '''
    The term that represent a type.
    '''
    fsymbol_print = 'type-term'
    fsymbol = 'TYPE-TERM'
    ...

    @abstractmethod
    def subst(self, sigma: Subst | dict[Var, Term]) -> TypeTerm:
        raise NotImplementedError()

class Typing(Term):
    '''
    The symbol that represents a typing relation.
    '''
    fsymbol_print = 'typing'
    fsymbol = 'TYPING'

    def __init__(self, term: Term, type: TypeTerm):

        assert not isinstance(term, Typing), "the term should not be typed already"

        self.term = term
        self.type = type

    def __str__(self) -> str:
        return str(ParenBlock(HSeqBlock(
            str(self.term), " : ", str(self.type),
            v_align='c'
        )))
    
    def __repr__(self) -> str:
        return rf'({repr(self.term)} : {repr(self.type)})'
    
    def tex(self) -> str:
        return rf' \left ( {self.term} : {self.type} \right )'
    
    def __eq__(self, __value: Term) -> bool:
        return isinstance(__value, Typing) and self.term == __value.term and self.type == __value.type

    def size(self) -> int:
        return self.term.size() + self.type.size() + 1
    
    def variables(self) -> set[Var]:
        return self.term.variables() | self.type.variables()
    
    def subst(self, sigma: Subst | dict[Var, Term]) -> Typing:
        return type(self)(self.term.subst(sigma), self.type.subst(sigma))
    
class FunType(TypeTerm):
    '''
    The term that represents a function type.
    '''
    fsymbol_print = 'fun-type'
    fsymbol = 'FUN-TYPE'

    def __init__(self, arg_type: TypeTerm, ret_type: TypeTerm):
        self.arg_type = arg_type
        self.ret_type = ret_type

    def __str__(self) -> str:
        return str(ParenBlock(HSeqBlock(
            str(self.arg_type), " -> ", str(self.ret_type),
            v_align='c'
        )))
    
    def __repr__(self) -> str:
        return rf'({repr(self.arg_type)} -> {repr(self.ret_type)})'

    def tex(self) -> str:
        return rf' \left ( {self.arg_type} \rightarrow {self.ret_type} \right )'
    
    def __eq__(self, __value: Term) -> bool:
        return isinstance(__value, FunType) and self.arg_type == __value.arg_type and self.ret_type == __value.ret_type
    
    def size(self) -> int:
        return self.arg_type.size() + self.ret_type.size() + 1
    
    def variables(self) -> set[Var]:
        return self.arg_type.variables() | self.ret_type.variables()
    
    def subst(self, sigma: Subst | dict[Var, Term]) -> Term:
        return type(self)(self.arg_type.subst(sigma), self.ret_type.subst(sigma))


class TypingMatching:
    '''
    A matching for type checking
    '''
    def __init__(self, ineqs : List[Tuple[Term, Term]]):
        self.ineqs = ineqs

    def __str__(self) -> str:
        
        return "{" + ", ".join([f"{lhs} ≲? {rhs}" for lhs, rhs in self.ineqs]) + "}"
    
    @property
    def variables(self) -> set[Var]:
        res = set()
        for lhs, rhs in self.ineqs:
            res |= lhs.variables() | rhs.variables()
        return res        
    

    def solve(self) -> Subst | None:
        return self.solve_matching(self.ineqs)

    @staticmethod
    def solve_matching(ineqs: List[Tuple[Term, Term]]) -> Subst | None:

        subst : dict[Var, Term] = {}

        while len(ineqs) > 0:
            lhs, rhs = ineqs[0]

            if isinstance(lhs, Var):
                if lhs in subst.keys():
                    if Subst(subst)(lhs) == rhs:
                        ineqs = ineqs[1:]
                        continue
                    else:
                        return None
                else:
                    subst[lhs] = rhs
                    ineqs = ineqs[1:]
                    continue

            # being function constructions
            elif isinstance(lhs, StdTerm):
                if isinstance(rhs, Var):
                    return None
            
                elif isinstance(rhs, StdTerm):
                    if type(lhs) == type(rhs):
                        ineqs = ineqs[1:]
                        for i in range(len(lhs.args)):
                            ineqs.append((lhs.args[i], rhs.args[i]))
                        continue

                    else:
                        return None
                    
                    
                else:
                    return None

            elif isinstance(rhs, Typing):
                if type(lhs) == type(rhs):
                    assert isinstance(lhs, Typing)
                    ineqs = ineqs[1:]
                    ineqs.append((lhs.term, rhs.term))
                    ineqs.append((lhs.type, rhs.type))
                    continue

                else:
                    return None                    
                
            # if there are terms outside the term rewriting system
            else:
                if lhs == rhs:
                    ineqs = ineqs[1:]
                    continue
                else:
                    return None
                    
        return Subst(subst)


    @staticmethod
    def single_match(lhs : Term, rhs : Term) -> Subst | None:
        return TypingMatching.solve_matching([(lhs, rhs)])
    

def canonical_typing(rule: TypingRule, trs: TRS, term: Term) -> Term|None:
    
    assert isinstance(rule.lhs, Term)
    assert isinstance(rule.rhs, Typing)

    subst = TypingMatching.single_match(rule.lhs, term)
    if subst is None:
        return None
    else:
        return subst(rule.rhs)

class TypingRule(Rule):
    '''
    A well-formed typing rule is a rewriting rule satisfy certain conditions:
    - LHS: leading symbol is not a typing symbol, while the parameters starts with typing symbols.
    - RHS: leading symbol is a typing symbol, and the term does not start with typing symbol.
    '''
    def __init__(self, 
                 rule_name: str,
                 lhs: Term|str,
                 rhs: Typing|str,
                 rewrite_method : Callable[[TypingRule, TRS, Term], Term|None] = canonical_typing,
                 rule_repr: str|None = None):

        # check whether the rule is well-formed
        if isinstance(lhs, Term):
            assert not isinstance(lhs, Typing), "the LHS should not be typed already"

            if isinstance(lhs, StdTerm):
                assert all(isinstance(arg, Typing) for arg in lhs.args), "the LHS parameters should start with typed terms"
            
            # type inferrence of AC symbol does not go into the canonical treatment by unifcation, because we want the typing to be flattened, and the well typed conditions needs to be checked across all parameters.
            if isinstance(lhs, AC):
                raise NotImplementedError("AC is not supported yet.")
        
        if isinstance(rhs, TypeTerm):
            assert isinstance(rhs, Typing), "the RHS should be a typing symbol"
        
        self.rule_name = rule_name
        self.lhs = lhs
        self.rhs = rhs
        self.rewrite_method = rewrite_method
        self.rule_repr = rule_repr

    def subst(self, sigma: Subst | dict[Var, Term]) -> TypingRule:
        new_lhs = self.lhs.subst(sigma) if isinstance(self.lhs, Term) else self.lhs
        new_rhs = self.rhs.subst(sigma) if isinstance(self.rhs, Typing) else self.rhs
        return type(self)(self.rule_name, new_lhs, new_rhs, self.rewrite_method, self.rule_repr)


class TypeChecker(TRS):
    '''
    TypeChecker is a special kind of term rewriting system.
    The typing rules are rewriting rules, and type checking infers the types of each term by iteratively apply the typing rule.
    '''
    def __init__(self, rules: Sequence[Rule]):
        super().__init__(rules)


    def subst(self, sigma : Subst) -> TypeChecker:
        '''
        Apply the substitution on the TRS. Return the result.
        '''
        new_rules = []
        for rule in self.rules:
            new_rules.append(rule.subst(sigma))

        res = TypeChecker(new_rules)
        res.set_rule_seq(self.rule_seq_name)
        return res
    
    def normalize(self, 
            term: Term, 
            verbose: bool = False, 
            stream: TextIO = sys.stdout, 
            step_limit: int | None = None) -> Term:
        '''
        Conduct the type checking and inferrence.
        '''

        # check the variable conincidence
        renamed_trs = self.avoid_vars(term.variables())

        current_term = term          

        step=0
        while True:

            # check whether the step limit is reached
            step += 1
            if step_limit is not None and step > step_limit:
                break

            if verbose:
                stream.write(f"== STEP {step} ==\n")
                stream.write("Current Term:\n")
                stream.write(str(current_term)+"\n\n")
                
            # check whether rewrite rules are applicable
            new_term = renamed_trs.rewrite_typing(None, current_term, verbose, stream) # type: ignore

            if new_term is None:
                if verbose:
                    stream.write("Type Checking & Inferrence Finished.\n")
                break
            
            current_term = new_term

        # check the final term
        if not isinstance(current_term, Typing):
            raise ValueError("The term is not well-typed.")

        return current_term

    def rewrite_typing(self, parent: Term | None, term: Term, verbose: bool = False, stream: TextIO = sys.stdout) -> Term | None:
        '''
        Typing rules will only apply on untyped terms.
        '''

        if isinstance(term, StdTerm):
            # try to rewrite the subterms
            for i in range(len(term.args)):
                new_subterm = self.rewrite_typing(term, term.args[i], verbose, stream)
                if new_subterm is not None:
                    return type(term)(*term.args[:i], new_subterm, *term.args[i+1:])
                
        elif isinstance(term, BindVarTerm):
            new_body = self.rewrite_typing(term, term.body, verbose, stream)
            if new_body is not None:
                # risk exists: term.bind_var may collide with new_body
                # but normal rewriting rules should not cause this problem because there are no free variables on the RHS
                return type(term)(term.bind_var, new_body)
            
        elif isinstance(term, MultiBindTerm):
            new_body = self.rewrite_typing(term, term.body, verbose, stream)
            if new_body is not None:
                return type(term)(term.bind_vars, new_body)
            
        elif isinstance(term, Typing):
            new_term = self.rewrite_typing(term, term.term, verbose, stream)
            if new_term is not None:
                return Typing(new_term, term.type)


        # try to rewrite the term using the rules
        if not isinstance(parent, Typing):
            for rule in self.rule_seq:
                new_term = rule.rewrite_method(rule, self, term)
                if new_term is not None:
                    # output information
                    if verbose:
                        stream.write(str(
                            FrameBlock(
                            HSeqBlock(str(term), ' -> ', str(new_term), v_align='c'),
                            caption=f"apply {rule.rule_name}"
                            )
                            ) + "\n\n")
                    return new_term
            
            return None    


