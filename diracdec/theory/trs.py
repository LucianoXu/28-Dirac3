'''
The architecture of the term rewriting system
'''

from __future__ import annotations
import sys
from typing import Callable, Set, TextIO, Tuple, Any, Dict, List, Sequence, Container, Type

from abc import ABC, abstractmethod

from IPython.core.display import Image

from ..backends.formprint import *
from ..backends import render_tex, render_tex_to_svg


import itertools
from itertools import combinations

def new_var(vars: Container[str|Var], prefix: str = "x") -> Var:
    '''
    return the new variable name that is not in the vars.
    '''
    i = 0
    while prefix + str(i) in vars:
        i += 1
    return Var(prefix + str(i))

def new_var_ls(vars: Container[str|Var], count:int, prefix: str = "x") -> tuple[Var, ...]:
    '''
    return the new variable names that are not in the vars.
    '''
    i = 0
    res = []
    while len(res) < count:
        if prefix + str(i) not in vars:
            res.append(Var(prefix + str(i)))
        i += 1
    return tuple(res)

def seq_content_eq(ls1: Sequence, ls2: Sequence) -> bool:
    '''
    check whether the contents of the sequences are equal up to permutations
    '''
    if len(ls1) != len(ls2):
        return False
    else:
        remain = list(ls2)
        for item in ls1:
            try:
                remain.remove(item)
            except ValueError:
                return False
        return True

class Term(ABC):
    '''
    The abstract class for all terms in the term rewriting system.
    '''
    fsymbol_print = 'term'
    fsymbol = 'TERM'

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        '''
        It is required that equivalence of the repr of two terms is equivalent to that of the terms.
        '''
        pass

    def tex(self) -> str:
        '''
        return the texcode of the term.
        '''
        raise NotImplementedError()

    @abstractmethod
    def __eq__(self, __value: Term) -> bool:
        '''
        This method calculates the equivalence in pure syntactic level.
        '''
        return super().__eq__(__value)
        
    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def variables(self) -> set[Var]:
        pass

    @property
    def is_ground(self) -> bool:
        return len(self.variables()) == 0

    @abstractmethod
    def subst(self, sigma : Subst | dict[Var, Term]) -> Term:
        pass


    #############################################
    # utilities
    def render_tex(self, filename:str|None = None, dpi:int = 300) -> Image:
        '''
        render the term into latex image
        '''
        return render_tex(self.tex(), filename, dpi)
    
    def render_tex_to_svg(self, filename:str) -> None:
        '''
        render the term into latex image as a svg file
        '''
        return render_tex_to_svg(self.tex(), filename)
        

class Var(Term):
    fsymbol_print = "var"
    fsymbol = "VAR"

    def __init__(self, name: str):
        assert isinstance(name, str)
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name
    
    def tex(self) -> str:
        new_name = self.name.replace('_',r'\_')
        return rf" \mathit{{{new_name}}}"
    
    def __eq__(self, other: Var|str) -> bool:
        '''
        Can be compared with Var or str instances
        '''
        if isinstance(other, str):
            return self.name == other
        
        return isinstance(other, Var) and self.name == other.name
    
    def size(self) -> int:
        return 1
    
    def __hash__(self):
        return hash(self.name)
    
    def variables(self) -> set[Var]:
        return {self}
    
    def subst(self, sigma: Subst | dict[Var, Term]) -> Term:
        if isinstance(sigma, Subst):
            sigma = sigma.data
        return self if self.name not in sigma else sigma[self.name]

class StdTerm(Term):
    fsymbol_print = 'std'
    fsymbol = 'STD'
    arity = 0

    def __init__(self, *args: Term):
        self.args = args

    def __str__(self) -> str:
        arg_blocks = []

        if len(self.args) > 0:
            arg_blocks.append(str(self.args[0]))
        for arg in self.args[1:]:
            arg_blocks.append(", ")
            arg_blocks.append(str(arg))

        return str(HSeqBlock(
            self.fsymbol_print,
            ParenBlock(HSeqBlock(*arg_blocks))
            ))

    def __repr__(self) -> str:
        if len(self.args) == 0:
            return self.fsymbol
        return f'{self.fsymbol}({", ".join(map(repr, self.args))})'

    def __eq__(self, other: Term) -> bool:
        if self is other:
            return True
        
        return isinstance(other, type(self)) and self.args == other.args
    
    def __getitem__(self, index) -> Term:
        return self.args[index]
    
    def size(self) -> int:
        '''
        Return the size of the abstract syntax tree.
        '''
        return 1 + sum(arg.size() for arg in self.args)
    
    def variables(self) -> set[Var]:
        '''
        Return a set of (the name of) all variables in this term. (including the bind variables)
        '''
        res = set()
        for arg in self.args:
            res |= arg.variables()
        return res
    
    def subst(self, sigma : Subst | dict[Var, Term]) -> Term:
        
        new_args = tuple(
            arg.subst(sigma) for arg in self.args
        )
        return type(self)(*new_args)

class BindVarTerm(Term):
    fsymbol_print = 'bind'
    fsymbol = 'BIND'

    '''
    The Term with a bind variable
    '''
    def __init__(self, bind_var: Var, body: Term):
        self.bind_var = bind_var
        self.body = body

    def __str__(self) -> str:
        return str(ParenBlock(HSeqBlock(
            self.fsymbol_print,
            " ",
            str(self.bind_var),
            ".",
            str(self.body),
            v_align='c'
        )
        ))
    
    def __repr__(self) -> str:
        return f"{self.fsymbol}[{repr(self.bind_var)}]({repr(self.body)})"
    
    def tex(self) -> str:
        return rf" \left ({self.fsymbol_print}\ {self.bind_var.tex()}.{self.body.tex()} \right )"
    
    def __eq__(self, __value: Term) -> bool:
        '''
        alpha-conversion is considered in the syntactical equivalence of bind variable expressions
        '''
        if self is __value:
            return True
        
        if isinstance(__value, BindVarTerm):
            if self.bind_var == __value.bind_var:
                return self.body == __value.body
            else:
                new_v = new_var(self.variables() | __value.variables() | {self.bind_var, __value.bind_var})
                return self.rename_bind(new_v) == __value.rename_bind(new_v)
        
        else:
            return False
    
    def size(self) -> int:
        return self.body.size() + 2
    
    
    def variables(self) -> set[Var]:
        res = self.body.variables()
        res.discard(self.bind_var)
        return res


    def rename_bind(self, new_v: Var) -> BindVarTerm:
        '''
        rename the bind variable to a new one.
        '''
        assert new_v != self.bind_var
        return type(self)(new_v, self.body.subst({self.bind_var: new_v}))
    
    def avoid_vars(self, var_set: set[Var]) -> BindVarTerm:
        '''
        return the bind variable term which avoids bind variables in var_set
        '''
        if self.bind_var in var_set:
            new_bind_var = new_var(var_set | self.variables())
            return self.rename_bind(new_bind_var)
        
        else:
            return self
    
    def subst(self, sigma: Subst | dict[Var, Term]) -> BindVarTerm:
        '''
        check whether the bind variable appears in sigma.
        change the bind variable if so.
        '''
        if isinstance(sigma, dict):
            sigma = Subst(sigma)

        vset = sigma.domain | sigma.vrange
        avoided_term = self.avoid_vars(vset)
        return type(avoided_term)(avoided_term.bind_var, avoided_term.body.subst(sigma))
        

class MultiBindTerm(Term):
    fsymbol_print = 'multi-bind'
    fsymbol = 'MULBIND'

    '''
    The Term with multiple bind variable 
    (different bind variable order are equivalent)
    '''
    def __new__(cls, bind_vars: Tuple[Var, ...], body: Term):
        if len(bind_vars) == 0:
            return body
        else:
            obj = object.__new__(cls)
            MultiBindTerm.__init__(obj, bind_vars, body)
            return obj

    def __init__(self, bind_vars: Tuple[Var, ...], body: Term):
        # try to flatten
        if isinstance(body, type(self)):
            bind_vars = bind_vars + body.bind_vars
            body = body.body

        self.bind_vars = tuple(bind_vars)
        self.body = body

    def __str__(self) -> str:
        raise NotImplementedError()
        return f"({self.fsymbol_print} {' '.join(map(str,self.bind_vars))}.{self.body})"
    
    def __repr__(self) -> str:
        return f"{self.fsymbol}[{' '.join(map(repr, self.bind_vars))}]({repr(self.body)})"
    
    def tex(self) -> str:
        var_tex = '\\ '.join(map(lambda x: x.tex(), self.bind_vars))
        return rf" \left ({self.fsymbol_print}\ {var_tex}.{self.body.tex()} \right )"
    
    def __eq__(self, __value: Term) -> bool:
        '''
        alpha-conversion is considered in the syntactical equivalence of bind variable expressions
        '''
        if self is __value:
            return True
        
        if isinstance(__value, MultiBindTerm):
            if len(self.bind_vars) != len(__value.bind_vars):
                return False
            
            # first find common bind variable renaming list
            new_vars = new_var_ls(self.variables() | __value.variables() | set(self.bind_vars) | set(__value.bind_vars), len(self.bind_vars))

            self_renamed = self.rename_bind(tuple(v for v in new_vars))

            # try different bind variable sequences
            for perm in itertools.permutations(new_vars):
                other_renamed = __value.rename_bind(tuple(perm))
                if self_renamed.body == other_renamed.body:
                    return True
                
            return False
        
        else:
            return False

    
    def size(self) -> int:
        return self.body.size() + len(self.bind_vars) + 1
    
    
    def variables(self) -> set[Var]:
        res = self.body.variables()
        return res - set(self.bind_vars)


    def rename_bind(self, new_vars: Tuple[Var, ...]) -> MultiBindTerm:
        '''
        rename the bind variables in order
        '''
        assert set(self.bind_vars) & set(new_vars) == set()

        sub_dist = {}
        for i, new_v in enumerate(new_vars):
            sub_dist[self.bind_vars[i].name] = new_v

        return type(self)(new_vars, self.body.subst(Subst(sub_dist)))
    
    def avoid_vars(self, var_set: set[Var]) -> MultiBindTerm:
        '''
        return the bind variable term which avoids bind variables in var_set
        '''
        if len(set(self.bind_vars) & var_set) > 0:
            new_bind_var_ls = new_var_ls(var_set | self.variables(), len(self.bind_vars))
            return self.rename_bind(new_bind_var_ls)
        
        else:
            return self

    def subst(self, sigma: Subst) -> MultiBindTerm:
        '''
        check whether the bind variable appears in sigma.
        change the bind variable if so.
        '''
        vset = sigma.domain | sigma.vrange
        avoided_term = self.avoid_vars(vset)
        return type(self)(avoided_term.bind_vars, avoided_term.body.subst(sigma))


##################################################################
# other specified terms (Commutative, AC, infix binary, ...)
    
class InfixBinary(StdTerm):
    arity = 2
    def __init__(self, L : Term, R : Term):
        super().__init__(L, R)

    def __str__(self) -> str:
        return str(ParenBlock(HSeqBlock(
            str(self.args[0]), self.fsymbol_print, str(self.args[1])
        )))

    def __repr__(self) -> str:
        return f'({repr(self.args[0])} {self.fsymbol} {repr(self.args[1])})'
    
    def subst(self, sigma: Subst) -> Term:
        return super().subst(sigma)
    
class CommBinary(StdTerm):
    '''
    (not infix)
    '''
    arity = 2

    def __init__(self, L : Any, R : Any):
        super().__init__(L, R)

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        
        if isinstance(other, type(self)):
            return seq_content_eq(self.args, other.args)
        
        return False

    def __repr__(self) -> str:
        return f'{self.fsymbol}({repr(self.args[0])}, {repr(self.args[1])})'
    
    def subst(self, sigma: Subst) -> Term:
        return super().subst(sigma)
    
class Assoc(StdTerm):
    arity = 2

    def __new__(cls, *tup: Any):
        '''
        return the element directly when tuple has only one element
        '''
        if len(tup) == 0:
            raise ValueError("The tuple lengh should be at least 1.")
        elif len(tup) == 1:
            return tup[0]
        else:
            obj = object.__new__(cls)
            Assoc.__init__(obj, *tup)
            return obj
        
    def __init__(self, *tup: Any):
        '''
        The method of flatten the tuple of arguments for the associative symbol.
        Assume that the items in tup are already flattened.
        '''

        new_ls = []
        for item in tup:
            if isinstance(item, type(self)):
                new_ls.extend(item.args)
            else:
                new_ls.append(item)

        self.args = tuple(new_ls)

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        
        if isinstance(other, type(self)):
            return self.args == other.args
        
        return False


    def __str__(self) -> str:
        blocks = [str(self.args[0])]
        for arg in self.args[1:]:
            blocks.append(f" {self.fsymbol_print} ")
            blocks.append(str(arg))

        return str(ParenBlock(HSeqBlock(*blocks, v_align='c')))
    
    def __repr__(self) -> str:
        return f'({f" {self.fsymbol} ".join(map(repr, self.args))})'
    
    def tex(self) -> str:
        return rf' \left ({f" {self.fsymbol_print} ".join(map(lambda x: x.tex(), self.args))} \right )'
    
    def subst(self, sigma: Subst) -> Term:
        return type(self)(*tuple(arg.subst(sigma) for arg in self.args))
    
    def remained_terms(self, *idx: int):
        '''
        collect the terms that are not in the idx, and return as a new tuple.
        '''
        return tuple(self.args[i] for i in range(len(self.args)) if i not in idx)

class AC(StdTerm):
    arity = 2

    def __new__(cls, *tup: Any):
        '''
        return the element directly when tuple has only one element
        '''
        if len(tup) == 0:
            raise ValueError("The tuple lengh should be at least 1.")
        elif len(tup) == 1:
            return tup[0]
        else:
            obj = object.__new__(cls)
            AC.__init__(obj, *tup)
            return obj
        
    def __init__(self, *tup: Any):
        '''
        The method of flatten the tuple of arguments for the ac_symbol.
        Assume that the items in tup are already flattened.
        '''

        new_ls = []
        for item in tup:
            if isinstance(item, type(self)):
                new_ls.extend(item.args)
            else:
                new_ls.append(item)

        self.args = tuple(new_ls)

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        
        if isinstance(other, type(self)):
            return seq_content_eq(self.args, other.args)
        
        return False


    def __str__(self) -> str:
        blocks = [str(self.args[0])]
        for arg in self.args[1:]:
            blocks.append(f" {self.fsymbol_print} ")
            blocks.append(str(arg))

        return str(ParenBlock(HSeqBlock(*blocks, v_align='c')))
    
    def __repr__(self) -> str:
        return f'({f" {self.fsymbol} ".join(map(repr, self.args))})'
    
    def tex(self) -> str:
        return rf' \left ({f" {self.fsymbol_print} ".join(map(lambda x: x.tex(), self.args))} \right )'
    
    def subst(self, sigma: Subst) -> Term:
        return type(self)(*tuple(arg.subst(sigma) for arg in self.args))
    
    def remained_terms(self, *idx: int):
        '''
        collect the terms that are not in the idx, and return as a new tuple.
        '''
        return tuple(self.args[i] for i in range(len(self.args)) if i not in idx)

################################################################################
# universal algebra methods

class Subst:
    def __init__(self, data : dict[Var, Term]):
        self.data = data.copy()


    def __call__(self, term : Term) -> Term:
        '''
        Apply the substitution on a term. Return the result.
        '''
        return term.subst(self)
    
    def __contains__(self, idx) -> bool:
        return idx in self.data

    def __getitem__(self, idx) -> Term:
        return self.data[idx]
    
    def __str__(self):
        blocks : List[str|FormBlock] = [' ']
        for key in self.data:
            blocks.append(HSeqBlock(' ', str(key), ' ↦ ', str(self.data[key]), ' '))
            blocks.append(' ')
        return str(FrameBlock(VSeqBlock(*blocks, h_align='l')))
    
    def __eq__(self, other: Subst | dict[Var, Term]) -> bool:
        if self is other:
            return True
        
        if isinstance(other, Subst):
            return self.data == other.data
        
        elif isinstance(other, dict):
            return self.data == other
        
        else:
            return False
    

    ################################################
    # universal algebra methods
    
    @property
    def domain(self) -> set[Var]:
        return set(self.data.keys())
    
    @property
    def vrange(self) -> set[Var]:
        '''
        variable range: the variables occuring in the range
        '''
        res = set()
        for rhs in self.data.values():
            res |= rhs.variables()
        return res
    
    def composite(self, other : Subst | dict[Var, Term]) -> Subst:
        '''
        return the composition `self(other)`.
        The `other` substitution is applied first.
        '''
        if not isinstance(other, Subst):
            other = Subst(other)

        new_data = {}

        for var in other.domain:
            new_data[var] = other[var].subst(self)

        for var in self.domain - other.domain:
            new_data[var] = self[var]

        return Subst(new_data)
    
    @property
    def is_idempotent(self) -> bool:
        '''
        A substitution σ is idempotent if σ = σσ.
        '''
        # This is the equivalent condition for idempotent
        return len(self.domain & self.vrange) == 0
    
    def get_idempotent(self) -> Subst:
        '''
        Return the equivalent substitution to rewrite the term repeatedly until it's fixed
        '''
        res = self
        while not res.is_idempotent:
            res = self.composite(res)

        return res

##################################################################
# matching
# notice: no variable renaming applied here
    
class Matching:
    '''
    A matching problem in the TRS system.
    (No type check.)

    Based on [Term Rewriting and All That] Sec.4.7, and some enhancement about AC

    [find a substitution sigma that sigma(lhs) = rhs]
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
    

    def solve(self) -> list[Subst]:
        subst_res = []
        self.solve_matching(tuple(self.ineqs), {}, subst_res)
        return subst_res

    @staticmethod
    def solve_matching(ineqs: Tuple[Tuple[Term, Term], ...], pre_subst: dict[Var, Term], subst_res: list[Subst]) -> None:

        subst = pre_subst.copy()

        while len(ineqs) > 0:
            lhs, rhs = ineqs[0]

            if isinstance(lhs, Var):
                if lhs in subst.keys():
                    if Subst(subst)(lhs) == rhs:
                        ineqs = ineqs[1:]
                        continue
                    else:
                        return
                else:
                    subst[lhs] = rhs
                    ineqs = ineqs[1:]
                    continue

            # being function constructions
            elif isinstance(lhs, StdTerm):
                if isinstance(rhs, Var):
                    return
            
                elif isinstance(rhs, StdTerm):
                    if type(lhs) == type(rhs):
                        ineqs = ineqs[1:]
                        # check different situations, possibly branch into different cases
                        if isinstance(lhs, CommBinary):
                            Matching.solve_matching(ineqs + ((lhs[0], rhs[0]), (lhs[1], rhs[1])), subst, subst_res)
                            Matching.solve_matching(ineqs + ((lhs[0], rhs[1]), (lhs[1], rhs[0])), subst, subst_res)
                            return

                        if isinstance(lhs, AC):
                            assert isinstance(rhs, AC)
                            
                            # get all possible bipartition of rhs.args
                            bipartitions = []
                            for i in range(1, len(rhs.args)):
                                for comb in combinations(range(len(rhs.args)), i):
                                    bipartitions.append(
                                        (
                                            type(rhs)(rhs.remained_terms(*comb)), 
                                            type(rhs)(rhs.remained_terms(*tuple(i for i in range(len(rhs.args)) if i not in comb)))
                                        )
                                    )
                            
                            for bipartite in bipartitions:
                                Matching.solve_matching(
                                    ineqs + 
                                    (
                                        (lhs.args[0], type(rhs)(*bipartite[0])), 
                                        (type(lhs)(*lhs.remained_terms(0)), type(rhs)(*bipartite[1]))
                                    ), 
                                    subst, subst_res
                                )

                            return
                        
                        if isinstance(lhs, Assoc):
                            raise NotImplementedError()
                        
                        else:
                            for i in range(len(lhs.args)):
                                ineqs = ineqs + ((lhs.args[i], rhs.args[i]),)
                            continue

                    else:
                        return
                    
                else:
                    return
                    
            elif isinstance(lhs, Typing):
                if isinstance(rhs, Typing):
                    ineqs = ineqs[1:] + ((lhs.type, rhs.type), (lhs.term, rhs.term))
                else:
                    return


            # if there are terms outside the term rewriting system
            # also including TypeTerms
            else:
                if lhs == rhs:
                    ineqs = ineqs[1:]
                    continue
                else:
                    return
                    
        subst_res.append(Subst(subst))


    @staticmethod
    def single_match(lhs : Term, rhs : Term) -> list[Subst]:
        subst_res = []
        Matching.solve_matching(((lhs, rhs),), {}, subst_res)
        return subst_res
    
############################################################################
# term rewriting rules
# note that there are different mechanisms for matching the rules and the terms
# for common rules we use normal matching, and for rules with equational theories, we write specified matching algorithms.
# this is a good balance of generality and efficiency.



class Rule:
    def __init__(self, 
                 rule_name: str,
                 lhs: Term|str, 
                 rhs: Term|str,
                 rewrite_method : Callable[[Rule, TRS, Term], Term|None],
                 rule_repr: str|None = None):
        '''
        note: the rewrite_method checks whether the current rule can rewrite the given term (not including subterms)
        '''

        assert isinstance(rule_repr, (str, type(None))), "The rule_repr should be a string or None."
    
        self.rule_name = rule_name
        self.lhs = lhs
        self.rhs = rhs
        self.rewrite_method = rewrite_method
        self.rule_repr = rule_repr

    def __str__(self) -> str:
        return str(HSeqBlock(
            f"(* {self.rule_name} *)", 
            " ", 
            str(self.lhs), 
            ' -> ', 
            str(self.rhs),
            ' ;',
            v_align='c'))

    def __repr__(self) -> str:
        if self.rule_repr is not None:
            return self.rule_repr
        
        str_lhs = self.lhs if isinstance(self.lhs, str) else repr(self.lhs)
        str_rhs = self.rhs if isinstance(self.rhs, str) else repr(self.rhs)
        return f'(* {self.rule_name} *)\t\t{str_lhs} -> {str_rhs} ;'
    
    def subst(self, sigma : Subst|dict[Var, Term]) -> Rule:
        if isinstance(sigma, dict):
            sigma = Subst(sigma)

        new_lhs = self.lhs.subst(sigma) if isinstance(self.lhs, Term) else self.lhs
        new_rhs = self.rhs.subst(sigma) if isinstance(self.rhs, Term) else self.rhs
        return Rule(
            self.rule_name, 
            new_lhs, 
            new_rhs, 
            self.rewrite_method, 
            self.rule_repr)

    
##################################################################
# canonical rewriting rule

def canonical_rewrite(rule: CanonicalRule, trs : TRS, term : Term) -> Term | None:
    '''
    The rewrite method for canonical rules.

    try rewriting the term using this rule. Return the result if successful, otherwise return None.

    (The parameter [trs] is necessary to be consistent with customized rewriting methods.)
    '''
    subst = Matching.single_match(rule.lhs, term)
    if len(subst) == 0:
        return None
    else:
        return subst[0](rule.rhs)
        
class CanonicalRule(Rule):
    def __init__(self, 
                 rule_name:str,
                 lhs: Term, 
                 rhs: Term,
                 rule_repr: str|None = None):
        
        self.rule_name = rule_name
        self.lhs = lhs
        self.rhs = rhs
        self.rule_repr = rule_repr
        self.rewrite_method = canonical_rewrite

        
    def subst(self, sigma : Subst|dict[Var, Term]) -> CanonicalRule:
        if isinstance(sigma, dict):
            sigma = Subst(sigma)

        return CanonicalRule(
            self.rule_name, 
            self.lhs.subst(sigma), 
            self.rhs.subst(sigma))
    

#############################################################
# a signature

class Signature:
    def __init__(self, symbols: Sequence[Type[Term]]):
        self.symbols = list(symbols)

    def append(self, symbol: Type[Term]):
        self.symbols.append(symbol)

    @staticmethod
    def cime2_repr_single(std_type: Type[Term]) -> str:
        '''
        The description of a symbol in the signature language of CiME2.
        '''
        prefix = f"(* {std_type.__name__} *)\t{std_type.fsymbol} \t\t:"
        if issubclass(std_type, AC):
            sort = f" AC ;"
        
        elif issubclass(std_type, InfixBinary):
            sort = f" infix binary ;"
        
        elif issubclass(std_type, CommBinary):
            sort = f" commutative ;"
        
        elif issubclass(std_type, StdTerm):
            if std_type.arity == 0:
                sort = f" constant ;"
            
            elif std_type.arity == 1:
                sort = f" unary ;"
            
            elif std_type.arity == 2:
                sort = f" binary ;"
            
            else:
                sort = f" {std_type.arity} ;"

        elif issubclass(std_type, Typing):
            sort = f" infix binary ;"
        
        else:
            raise ValueError("The symbol is not supported in CiME2.")

        return prefix + sort
        

    def cime2_repr(self) -> str:
        '''
        The representation is intended for CiME2 signature.
        '''
        res = '''
let F = signature
"
'''
        for symbol in self.symbols:
            res += self.cime2_repr_single(symbol) + "\n"
        
        res += '''
";
'''
        return res

        


######################################################################
# term rewriting system
        
class TRS:

    def __init__(self, rules: Sequence[Rule]):
        '''
        side_info_procs provides methods to preprocess side informations (executed in sequence)
        '''
        self.rules : List[Rule] = []
        self.extended_rules : List[Rule] = []

        # the rule sequence that will be check during the rewriting. the order maters.
        self.rule_seq : List[Rule] = []

        self.rule_seq_name = []

        for rule in rules:
            self.append(rule)

    def copy(self) -> TRS:
        res = TRS([])
        res.rules = self.rules.copy()
        res.extended_rules = self.extended_rules.copy()
        res.rule_seq = self.rule_seq.copy()
        res.rule_seq_name = self.rule_seq_name.copy()
        return res

    
    def __getitem__(self, __rule_name: str) -> Rule|None:
        '''
        return the rule with the given name
        '''
        for rule in self.extended_rules:
            if rule.rule_name == __rule_name:
                return rule
        return None


    def append(self, rule: Rule) -> None:
        '''
        append a rule to the TRS
        '''
        
        # check whether the same rule already exists
        if self[rule.rule_name] is not None:
            raise ValueError(f"The rule with the name {rule.rule_name} already exists.")

        self.rules.append(rule)
        self.extended_rules.append(rule)
        self.rule_seq.append(rule)
        self.rule_seq_name.append(rule.rule_name)

        # extend the rules automatically
        if isinstance(rule, (CanonicalRule, TypingRule)) and isinstance(rule.lhs, AC) and isinstance(rule.rhs, Term):
            varX = new_var(rule.lhs.variables() | rule.rhs.variables(), "X")
            ext_rule = CanonicalRule(
                rule.rule_name + "-EXT",
                lhs = type(rule.lhs)(rule.lhs, varX),
                rhs = type(rule.lhs)(rule.rhs, varX)
            )
            self.extended_rules.append(ext_rule)
            self.rule_seq.append(ext_rule)
            self.rule_seq_name.append(ext_rule.rule_name)

    def set_rule_seq(self, rule_seq: List[str]) -> None:
        '''
        set the rule sequence that will be check during the rewriting. the order maters.
        '''
        new_seq = []

        for name in rule_seq:
            rule = self[name]
            if rule is None:
                raise ValueError(f"The rule with the name {name} does not exist.")
            new_seq.append(rule)
            self.rule_seq.remove(rule)

        # append the remaining part
        self.rule_seq = new_seq + self.rule_seq

        self.rule_seq_name = rule_seq.copy()

    def subtrs(self, rule_names: List[str]) -> TRS:
        '''
        return the sub TRS with the rules with the given names
        '''
        result = TRS([rule for rule in self.rules if rule.rule_name in rule_names])
        result.set_rule_seq(rule_names)
        return result
    

    def __str__(self) -> str:
        res = ""
        for rule in self.extended_rules:
            res += str(rule) + "\n"
        return res
    
    def __repr__(self) -> str:
        '''
        This representation is intended for CiME2 checking.
        '''
        res = ""
        for rule in self.extended_rules:
            res += repr(rule) + "\n"
        return res
    
    def cime_vars_repr(self) -> str:
        '''
        The description of the variables in the signature language of CiME2.
        '''
        res = f'''
let X = vars " {' '.join(map(str, list(self.variables()))) + " x0 x1 x2 x3 x4 x5 x6 x7"} ";
'''
        return res
    
    def cime_trs_repr(self) -> str:
        '''
        The description of the TRS in the signature language of CiME2.
        '''
        res = f'''
let R = TRS F X "
{repr(self)}
";
'''     
        return res

    def ordered_str(self) -> str:
        res = ""
        for rule in self.rule_seq:
            res += str(rule) + "\n"
        return res
    
    def __add__(self, other: TRS) -> TRS:
        return TRS(self.rules + other.rules)

    def variables(self) -> set[Var]:
        '''
        Return a set of all free variables in the rules.
        (This method is not that rigorous, and only acts as a hint.)
        '''
        res = set()
        for rule in self.extended_rules:
            if isinstance(rule.lhs, Term) and isinstance(rule.rhs, Term):
                res |= rule.lhs.variables() | rule.rhs.variables()
        return res
    
    def subst(self, sigma : Subst) -> TRS:
        '''
        Apply the substitution on the TRS. Return the result.
        '''
        new_rules = []
        for rule in self.rules:
            new_rules.append(rule.subst(sigma))

        res = TRS(new_rules)
        res.set_rule_seq(self.rule_seq_name)
        return res
    
    def avoid_vars(self, var_set: set[Var]) -> TRS:
        # check the variable conincidence
        overlap = var_set & self.variables()
        if len(overlap) > 0:

            subst = {}
            for var in overlap:
                subst[var] = new_var(overlap|set(subst.keys()), var.name)
            
            return self.subst(Subst(subst))

        else:
            return self


    def normalize(self, 
            term : Term, 
            verbose: bool = False, 
            stream: TextIO = sys.stdout,
            step_limit : int | None = None,
            alg: str = "inner_most") -> Term:

        # check the variable conincidence
        renamed_trs = self.avoid_vars(term.variables())

        current_term = term          

        # choose the algorithm
        if alg == "outer_most":
            rewrite = renamed_trs.rewrite_outer_most  
        elif alg == "inner_most":
            rewrite = renamed_trs.rewrite_inner_most

        step=0
        while True:

            # check whether the step limit is reached
            step += 1
            if step_limit is not None and step > step_limit:
                return current_term

            if verbose:
                stream.write(f"== STEP {step} ==\n")
                stream.write("Current Term:\n")
                stream.write(str(current_term)+"\n\n")
                
            # check whether rewrite rules are applicable
            new_term = rewrite(current_term, verbose, stream)

            if new_term is None:
                if verbose:
                    stream.write("It is the normal form.\n")
                return current_term
            
            current_term = new_term
            
    

    def rewrite_outer_most(self, term : Term, verbose:bool = False, stream: TextIO = sys.stdout) -> Term | None:
        '''
        rewrite the term using the rules. Return the result.
        return None when no rewriting is applicable

        algorithm: outer most
        '''

        # try to rewrite the term using the rules
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
                        
        if isinstance(term, StdTerm):
            # try to rewrite the subterms
            for i in range(len(term.args)):
                new_subterm = self.rewrite_outer_most(term.args[i], verbose, stream)
                if new_subterm is not None:
                    return type(term)(*term.args[:i], new_subterm, *term.args[i+1:])
                
        elif isinstance(term, BindVarTerm):
            new_body = self.rewrite_outer_most(term.body, verbose, stream)
            if new_body is not None:
                # risk exists: term.bind_var may collide with new_body
                # but normal rewriting rules should not cause this problem because there are no free variables on the RHS
                return type(term)(term.bind_var, new_body)
            
        elif isinstance(term, MultiBindTerm):
            new_body = self.rewrite_outer_most(term.body, verbose, stream)
            if new_body is not None:
                return type(term)(term.bind_vars, new_body)
            
        elif isinstance(term, Typing):
            new_term = self.rewrite_inner_most(term.term, verbose, stream)
            if new_term is not None:
                return type(term)(new_term, term.type)

            
        return None
    

    def rewrite_inner_most(self, term : Term, verbose:bool = False, stream:TextIO = sys.stdout) -> Term | None:
        '''
        rewrite the term using the rules. Return the result.
        return None when no rewriting is applicable

        algorithm: outer most
        '''

        if isinstance(term, StdTerm):
            # try to rewrite the subterms
            for i in range(len(term.args)):
                new_subterm = self.rewrite_inner_most(term.args[i], verbose, stream)
                if new_subterm is not None:
                    return type(term)(*term.args[:i], new_subterm, *term.args[i+1:])
                
        elif isinstance(term, BindVarTerm):
            new_body = self.rewrite_inner_most(term.body, verbose, stream)
            if new_body is not None:
                # risk exists: term.bind_var may collide with new_body
                # but normal rewriting rules should not cause this problem because there are no free variables on the RHS
                return type(term)(term.bind_var, new_body)
            
        elif isinstance(term, MultiBindTerm):
            new_body = self.rewrite_inner_most(term.body, verbose, stream)
            if new_body is not None:
                return type(term)(term.bind_vars, new_body)

        elif isinstance(term, Typing):
            new_term = self.rewrite_inner_most(term.term, verbose, stream)
            if new_term is not None:
                return type(term)(new_term, term.type)

        # try to rewrite the term using the rules
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
    

class TypeTerm(Term):
    '''
    The term that represent a type.
    '''
    fsymbol_print = 'type-term'
    fsymbol = 'TYPE-TERM'

    @abstractmethod
    def subst(self, sigma: Subst | dict[Var, Term]) -> TypeTerm:
        pass

class StdTypeTerm(TypeTerm, StdTerm):
    '''
    The standard type term.
    '''

    fsymbol_print = 'std-type-term'
    fsymbol = 'STD-TYPE-TERM'
    
    def __init__(self, *args: Term):
        StdTerm.__init__(self, *args)

    def subst(self, sigma: Subst | dict[Var, Term]) -> TypeTerm:
        return StdTerm.subst(self, sigma) # type: ignore


class Typing(Term):
    '''
    The symbol that represents a typing relation.
    '''
    fsymbol_print = 'typing'
    fsymbol = '$'

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
        return rf'({repr(self.term)} $ {repr(self.type)})'
    
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
    


def canonical_typing(rule: TypingRule, trs: TRS, term: Term) -> Term|None:
    
    assert isinstance(rule.lhs, Term)
    assert isinstance(rule.rhs, Typing)

    subst = Matching.single_match(rule.lhs, term)
    if len(subst) == 0:
        return None
    else:
        return subst[0](rule.rhs)

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
        
        if isinstance(rhs, TypeTerm):
            assert isinstance(rhs, Typing), "the RHS should be a typing symbol"

        # check whether the rule is well-formed
        if isinstance(lhs, Term):

            if isinstance(lhs, StdTerm):
                # this is disabled because sometimes we need to use the typing symbol as the first parameter

                # assert all(isinstance(arg, Typing) for arg in lhs.args), "the LHS parameters should start with typed terms"

                pass
            

        # if type inferrence of AC symbol want to go into the canonical treatment by unifcation, we want the typing to be flattened. The constraint is that the RHS typing and the LHS argument typing should be the same. And we need an extension rule to ``flatten'' the typing of AC symbol.

        if isinstance(lhs, AC):
            assert isinstance(rhs, Typing), "the RHS should be a typing symbol"

            assert lhs.args[0].type == rhs.type and lhs.args[1].type == rhs.type, "the typing of the AC symbol should be the same as the RHS"
                

        
        self.rule_name = rule_name
        self.lhs = lhs
        self.rhs = rhs
        self.rewrite_method = rewrite_method
        self.rule_repr = rule_repr

    def subst(self, sigma: Subst | dict[Var, Term]) -> TypingRule:
        if isinstance(sigma, dict):
            sigma = Subst(sigma)
            
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


    def append(self, rule: Rule) -> None:
        super().append(rule)

        # add the flatten rule
        if isinstance(rule.lhs, AC) and isinstance(rule.rhs, Typing):
            ac = type(rule.lhs)
            T = rule.rhs.type
            varX1, varX2, varX3 = new_var_ls(rule.lhs.variables() | rule.rhs.variables(), 3, "X")

            flt_rule = TypingRule(
                rule.rule_name + "-FLT",

                # lhs = [((A:S) + (B:S):S) + X]:S
                lhs = Typing(
                    ac(
                        Typing(
                            ac(
                                Typing(varX1, T),
                                Typing(varX2, T)
                            ),
                            T
                        ),
                        varX3
                    ),
                    T
                ),

                # rhs = (A:S) + (B:S) + X :S
                rhs = Typing(
                    ac(
                        Typing(varX1, T),
                        Typing(varX2, T),
                        varX3
                    ),
                    T
                )
            )
            self.extended_rules.append(flt_rule)
            self.rule_seq.append(flt_rule)
            self.rule_seq_name.append(flt_rule.rule_name)


    
    
    def copy(self) -> TypeChecker:
        res = TypeChecker([])
        res.rules = self.rules.copy()
        res.extended_rules = self.extended_rules.copy()
        res.rule_seq = self.rule_seq.copy()
        res.rule_seq_name = self.rule_seq_name.copy()
        return res


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
            step_limit: int | None = None,
            well_typed_check: bool = True) -> Term:
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
        if well_typed_check:
            if not isinstance(current_term, Typing):
                raise ValueError(f"The term {current_term} is not well-typed.")

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


class TypedTRS(TRS):
    '''
    Typed TRS is a term rewriting system with typing rules.
    The Canonical Rules will go through the type checking process.
    Other rules with special conditions should take care of the type checking by themselves.
    '''
    def __init__(self, 
                type_checker: TypeChecker,
                untyped_rules: Sequence[Rule]):
        self.type_checker = type_checker.copy()
        super().__init__(untyped_rules)

    def copy(self) -> TypedTRS:
        res = TypedTRS(self.type_checker, [])
        res.rules = self.rules.copy()
        res.extended_rules = self.extended_rules.copy()
        res.rule_seq = self.rule_seq.copy()
        res.rule_seq_name = self.rule_seq_name.copy()
        res.type_checker = self.type_checker.copy()
        return res
    
    def rule_type_checking(self, rule: Rule, well_typed_check: bool = True) -> Rule:
        '''
        Apply type inference and type checking on the canonical rule.
        '''
        if isinstance(rule, CanonicalRule):
            new_lhs = self.type_checker.normalize(rule.lhs, well_typed_check = well_typed_check)
            new_rhs = self.type_checker.normalize(rule.rhs, well_typed_check = well_typed_check)

            return CanonicalRule(rule.rule_name, new_lhs, new_rhs)

        else:
            return rule
        
    
    def append(self, untyped_rule: Rule) -> None:
        '''
        append a rule to the Typed TRS
        (the rule will go through a type checking first)
        '''
        
        # check whether the same rule already exists
        if self[untyped_rule.rule_name] is not None:
            raise ValueError(f"The rule with the name {untyped_rule.rule_name} already exists.")
        
        type_checked_rule = self.rule_type_checking(untyped_rule)

        self.rules.append(untyped_rule)
        self.extended_rules.append(type_checked_rule)
        self.rule_seq.append(type_checked_rule)
        self.rule_seq_name.append(type_checked_rule.rule_name)

        # extend the rules automatically
        if isinstance(type_checked_rule.lhs, Typing) and isinstance(type_checked_rule.lhs.term, AC) and isinstance(type_checked_rule.rhs, Typing):
            varX = new_var(type_checked_rule.lhs.variables() | type_checked_rule.rhs.variables(), "X")

            ac = type(type_checked_rule.lhs.term)
            T = type_checked_rule.rhs.type
            
            ext_rule = CanonicalRule(
                untyped_rule.rule_name + "-EXT",
                lhs = Typing(
                        ac(
                            type_checked_rule.lhs.term,
                            Typing(varX, T)
                        ),
                        T
                    ),
                rhs = Typing(
                        ac(
                            type_checked_rule.rhs,
                            varX
                        ),
                        T
                    )
            )

            self.extended_rules.append(ext_rule)
            self.rule_seq.append(ext_rule)
            self.rule_seq_name.append(ext_rule.rule_name)

        # add the flatten rule
        if isinstance(type_checked_rule.lhs, Typing) and isinstance(type_checked_rule.lhs.term, AC) and isinstance(type_checked_rule.rhs, Typing):

            ac = type(type_checked_rule.lhs.term)
            T = type_checked_rule.rhs.type
            varX1, varX2, varX3 = new_var_ls(type_checked_rule.lhs.variables() | type_checked_rule.rhs.variables(), 3, "X")

            flt_rule = TypingRule(
                type_checked_rule.rule_name + "-FLT",

                # lhs = [((A:S) + (B:S):S) + X]:S
                lhs = Typing(
                    ac(
                        Typing(
                            ac(
                                Typing(varX1, T),
                                varX2,
                            ),
                            T
                        ),
                        varX3
                    ),
                    T
                ),

                # rhs = (A:S) + (B:S) + X :S
                rhs = Typing(
                    ac(
                        Typing(varX1, T),
                        varX2,
                        varX3
                    ),
                    T
                )
            )
            self.extended_rules.append(flt_rule)
            self.rule_seq.append(flt_rule)
            self.rule_seq_name.append(flt_rule.rule_name)


    def append_canonical(self, 
                        rule_name:str,
                        lhs: Term, 
                        rhs: Term,
                        rule_repr: str|None = None) -> None:
        self.append(CanonicalRule(rule_name, lhs, rhs, rule_repr))

    def subst(self, sigma : Subst) -> TypedTRS:
        '''
        Apply the substitution on the TRS. Return the result.
        '''
        new_rules = []
        for rule in self.rules:
            new_rules.append(rule.subst(sigma))

        res = TypedTRS(self.type_checker, new_rules)
        res.set_rule_seq(self.rule_seq_name)
        return res


    def type_checking(self, term: Term) -> Term:
        '''
        Conduct the type checking and inferrence.
        '''
        return self.type_checker.normalize(term)
    
    def normalize(self, term: Term, verbose: bool = False, stream: TextIO = sys.stdout, step_limit: int | None = None, alg: str = "inner_most") -> Term:

        # check the type first
        type_checked_term = self.type_checking(term)

        return super().normalize(type_checked_term, verbose, stream, step_limit, alg)
    
    def original_rules_repr(self) -> str:
        res = ""
        for rule in self.rules:
            res += repr(rule) + "\n"
        return res
    
    def subtrs(self, rule_names: List[str]) -> TypedTRS:
        '''
        return the sub TRS with the rules with the given names
        '''
        result = TypedTRS(self.type_checker, [rule for rule in self.rules if rule.rule_name in rule_names])
        result.set_rule_seq(rule_names)
        return result
