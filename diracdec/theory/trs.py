'''
The architecture of the term rewriting system
'''

from __future__ import annotations
from typing import Callable, Tuple, Any, Dict, List

from abc import ABC, abstractmethod

import hashlib

class TRSTerm(ABC):
    fsymbol_print : str
    fsymbol : str

    def __init__(self, *args: Any):
        self.args = args

    def __str__(self) -> str:
        return f'{self.fsymbol_print}({", ".join(map(str, self.args))})'

    def __repr__(self) -> str:
        '''
        It is required that equivalence of the repr of two terms is equivalent to that of the terms.
        '''
        return f'{self.fsymbol}({", ".join(map(repr, self.args))})'

    def __eq__(self, other: TRSTerm) -> bool:
        '''
        This method calculates the equivalence in pure syntactic level.
        '''
        if self is other:
            return True
        
        return isinstance(other, type(self)) and self.args == other.args
    
    def __lt__(self, other: TRSTerm) -> bool:
        h_self = hash(self)
        h_other = hash(other)
        if h_self == h_other:
            return repr(self) < repr(other)
        else:
            return h_self < h_other

    
    def __hash__(self) -> int:
        h = hashlib.md5(self.fsymbol.encode())
        for arg in self.args:
            h.update(hash(arg).to_bytes(16, 'big'))

        return int(h.hexdigest(), 16)
    
    @property
    def size(self) -> int:
        '''
        Return the size of the abstract syntax tree.
        '''
        return 1 + sum(arg.size for arg in self.args)
    
    def variables(self) -> set[str]:
        '''
        Return a set of (the name of) all free variables in this term.
        '''
        res = set()
        for arg in self.args:
            res |= arg.variables()
        return res

    @property
    def is_ground(self) -> bool:
        return len(self.variables()) == 0
    
    @abstractmethod
    def substitute(self, sigma : Subst) -> TRSTerm:
        
        new_args = tuple(arg.substitute(sigma) for arg in self.args)
        return type(self)(*new_args)
        

class TRSVar(TRSTerm):

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name
    
    def __eq__(self, other: TRSVar) -> bool:
        return isinstance(other, TRSVar) and self.name == other.name
    
    def __hash__(self) -> int:
        h = hashlib.md5(("var" + self.name).encode())
        return int(h.hexdigest(), 16)
    
    def size(self) -> int:
        return 1
    
    def variables(self) -> set[str]:
        return {self.name}
    
    def substitute(self, sigma: Subst) -> TRSTerm:
        return self if self.name not in sigma else sigma[self.name]
    

################################################################################
# universal algebra methods

class Subst:
    def __init__(self, data : Dict[str, TRSTerm]):
        self.data = data.copy()


    def __call__(self, term : TRSTerm) -> TRSTerm:
        '''
        Apply the substitution on a term. Return the result.
        '''
        return term.substitute(self)
    
    def __contains__(self, idx) -> bool:
        return idx in self.data

    def __getitem__(self, idx) -> TRSTerm:
        return self.data[idx]
    
    def __str__(self):
        return "{" + ", ".join(f"{key} ↦ {self.data[key]}" for key in self.data) + "}"
    
    def __eq__(self, other) -> bool:
        if self is other:
            return True
        
        if isinstance(other, Subst):
            return self.data == other.data
        
        else:
            return False
    

    ################################################
    # universal algebra methods
    
    @property
    def domain(self) -> set[str]:
        return set(self.data.keys())

    @property
    def range(self) -> set[TRSTerm]:
        return set(self.data.values())
    
    @property
    def vrange(self) -> set[str]:
        res = set()
        for rhs in self.data.values():
            res |= rhs.variables()
        return res
    
    def composite(self, other : Subst) -> Subst:
        '''
        return the composition `self(other)`.
        '''
        new_data = {}

        for var in other.domain:
            new_data[var] = other[var].substitute(self)

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

##################################################################
# matching
# notice: no variable renaming applied here
    
class Matching:
    '''
    A matching problem in the TRS system.
    (No type check.)

    Based on [Term Rewriting and All That] Sec.4.7
    '''
    def __init__(self, ineqs : List[Tuple[TRSTerm, TRSTerm]]):
        self.ineqs = ineqs

    def __str__(self) -> str:
        
        return "{" + ", ".join([f"{lhs} ≲? {rhs}" for lhs, rhs in self.ineqs]) + "}"
    
    @property
    def variables(self) -> set[str]:
        res = set()
        for lhs, rhs in self.ineqs:
            res |= lhs.variables() | rhs.variables()
        return res        
    

    def solve(self) -> Subst | None:
        return self.solve_matching(self.ineqs)

    @staticmethod
    def solve_matching(ineqs: List[Tuple[TRSTerm, TRSTerm]]) -> Subst | None:

        subst : Dict[str, TRSTerm] = {}

        while len(ineqs) > 0:
            lhs, rhs = ineqs[0]

            if isinstance(lhs, TRSVar):
                if lhs.name in subst.keys():
                    if Subst(subst)(lhs) == rhs:
                        ineqs = ineqs[1:]
                        continue
                    else:
                        return None
                else:
                    subst[lhs.name] = rhs
                    ineqs = ineqs[1:]
                    continue

            # being function constructions
            elif isinstance(lhs, TRSTerm):
                if isinstance(rhs, TRSVar):
                    return None
            
                elif isinstance(rhs, TRSTerm):
                    if lhs.fsymbol == rhs.fsymbol:
                        ineqs = ineqs[1:]
                        for i in range(len(lhs.args)):
                            ineqs.append((lhs.args[i], rhs.args[i]))
                        continue

                    else:
                        return None
                    
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
    def single_match(lhs : TRSTerm, rhs : TRSTerm) -> Subst | None:
        return Matching.solve_matching([(lhs, rhs)])


##################################################################
# other specified terms (Commutative, AC, infix binary, ...)
    
class TRSInfixBinary(TRSTerm):
    def __init__(self, L : TRSTerm, R : TRSTerm):
        super().__init__(L, R)

    def __str__(self) -> str:
        return f'({str(self.args[0])} {self.fsymbol_print} {str(self.args[1])})'

    def __repr__(self) -> str:
        return f'({repr(self.args[0])} {self.fsymbol} {repr(self.args[1])})'
    
    def substitute(self, sigma: Subst) -> TRSTerm:
        return super().substitute(sigma)
    
class TRSCommBinary(TRSTerm):
    '''
    (not infix)
    '''
    def __init__(self, L : Any, R : Any):
        if L > R:
            L, R = R, L
        super().__init__(L, R)

    def __str__(self) -> str:
        return f'{self.fsymbol_print}({str(self.args[0])}, {str(self.args[1])})'

    def __repr__(self) -> str:
        return f'{self.fsymbol}({repr(self.args[0])}, {repr(self.args[1])})'
    
    def substitute(self, sigma: Subst) -> TRSTerm:
        return super().substitute(sigma)
    
class TRS_AC(TRSTerm):
    def __init__(self, tup: Tuple):
        '''
        The method of flatten the tuple of arguments for the ac_symbol.
        Assume that the items in tup are already flattened.
        '''
        if len(tup) < 2:
            raise ValueError("The tuple lengh should be at least 2.")

        new_ls = []
        for item in tup:
            if isinstance(item, type(self)):
                new_ls.extend(item.args)
            else:
                new_ls.append(item)

        self.args = tuple(sorted(new_ls))

    def __str__(self) -> str:
        return f'({f" {self.fsymbol_print} ".join(map(str, self.args))})'
    
    def __repr__(self) -> str:
        return f'({f" {self.fsymbol} ".join(map(repr, self.args))})'
    
    def substitute(self, sigma: Subst) -> TRSTerm:
        return type(self)(tuple(arg.substitute(sigma) for arg in self.args))


############################################################################
# term rewriting rules
# note that there are different mechanisms for matching the rules and the terms
# for common rules we use normal matching, and for rules with equational theories, we write specified matching algorithms.
# this is a good balance of generality and efficiency.
    
def check_special_symbol(term : TRSTerm) -> bool:
    '''
    iteratively check whether there are subterms of TRS_AC or TRS_CommBinary.
    return True if there are.
    '''
    if isinstance(term, TRS_AC) or isinstance(term, TRSCommBinary):
        return True
    else:
        if isinstance(term, TRSVar):
            return True
        else:
            for arg in term.args:
                if check_special_symbol(arg):
                    return True
            return False


def normal_rewrite(self, term : TRSTerm) -> TRSTerm | None:
        '''
        The rewrite method for normal rules.

        try rewriting the term using this rule. Return the result if successful, otherwise return None.
        '''
        subst = Matching.single_match(self.lhs, term)
        if subst is None:
            return None
        else:
            return subst(self.rhs)

class TRSRule:
    def __init__(self, 
                 lhs: TRSTerm, 
                 rhs: TRSTerm,
                 rewrite_method : Callable[[TRSRule, TRSTerm], TRSTerm|None] = normal_rewrite,
):
        '''
        note: the rewrite_method checks whether the current rule can rewrite the given term (not including subterms)
        '''
        self.rewrite_method = rewrite_method
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f'{self.lhs} → {self.rhs}'

    def __repr__(self) -> str:
        return f'{repr(self.lhs)} -> {repr(self.rhs)}'


class NormalRule:
    def __init__(self, lhs : TRSTerm, rhs : TRSTerm):
        if not check_special_symbol(lhs) or not check_special_symbol(rhs):
            raise ValueError("The rule should not contain special symbols.")
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f'{self.lhs} → {self.rhs}'
    
    def __repr__(self) -> str:
        return f'{repr(self.lhs)} -> {repr(self.rhs)}'
    
    def rewrite(self, term : TRSTerm) -> TRSTerm | None:
        '''
        try rewriting the term using this rule. Return the result if successful, otherwise return None.
        '''
        subst = Matching.single_match(self.lhs, term)
        if subst is None:
            return None
        else:
            return subst(self.rhs)
        
# define rule for AC symbols by defining new class
        

######################################################################
# term rewriting system
        
class TRS:

    def __init__(self, rules : List[TRSRule]):
        self.rules : List[TRSRule] = rules

    def normalize(self, term : TRSTerm, verbose: bool = False) -> TRSTerm:
        current_term = term

        while True:
            if verbose:
                print("--> ", current_term)

            new_term = self.rewrite(current_term)
            if new_term is None:
                return current_term
            
            current_term = new_term
        

            
    

    def rewrite(self, term : TRSTerm) -> TRSTerm | None:
        '''
        rewrite the term using the rules. Return the result.
        return None when no rewriting is applicable
        '''

        # try to rewrite the term using the rules
        for rule in self.rules:
            new_term = rule.rewrite_method(rule, term)
            if new_term is not None:
                return new_term
            
        if isinstance(term, TRSVar):
            return None
        
        elif isinstance(term, TRSTerm):
            # try to rewrite the subterms
            for i in range(len(term.args)):
                new_subterm = self.rewrite(term.args[i])
                if new_subterm is not None:
                    return type(term)(*term.args[:i], new_subterm, *term.args[i+1:])

            return None
        
        else:
            return None
