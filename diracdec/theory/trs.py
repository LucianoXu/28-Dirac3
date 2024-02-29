'''
The architecture of the term rewriting system
'''

from __future__ import annotations
from typing import Callable, Tuple, Any, Dict, List

from abc import ABC, abstractmethod

from IPython.core.display import Image

from ..backends import render_tex, render_tex_to_svg

import hashlib

def var_rename(vars: set[str], prefix: str = "x") -> str:
    '''
    return the new variable name that is not in the vars.
    '''
    i = 0
    while prefix + str(i) in vars:
        i += 1
    return prefix + str(i)

class TRSTerm(ABC):
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

    @abstractmethod
    def tex(self) -> str:
        '''
        return the texcode of the term.
        '''
        pass

    @abstractmethod
    def __eq__(self, __value: TRSTerm) -> bool:
        '''
        This method calculates the equivalence in pure syntactic level.
        '''
        return super().__eq__(__value)
    
    @abstractmethod
    def __hash__(self) -> int:
        pass


    def __lt__(self, other: TRSTerm) -> bool:
        h_self = hash(self)
        h_other = hash(other)
        if h_self == h_other:
            return repr(self) < repr(other)
        else:
            return h_self < h_other
        
    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def variables(self) -> set[str]:
        pass

    def free_variables(self) -> set[str]:
        return self.variables()

    @property
    def is_ground(self) -> bool:
        return len(self.variables()) == 0

    @abstractmethod
    def substitute(self, sigma : Subst) -> TRSTerm:
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
        

class TRSVar(TRSTerm):
    fsymbol_print = "var"
    fsymbol = "VAR"

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name
    
    def tex(self) -> str:
        new_name = self.name.replace('_',r'\_')
        return rf" \mathit{{{new_name}}}"
    
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

class StdTerm(TRSTerm):
    fsymbol_print = 'std'
    fsymbol = 'STD'

    def __init__(self, *args: TRSTerm):
        self.args = args

    def __str__(self) -> str:
        return f'{self.fsymbol_print}({", ".join(map(str, self.args))})'

    def __repr__(self) -> str:
        return f'{self.fsymbol}({", ".join(map(repr, self.args))})'

    def __eq__(self, other: TRSTerm) -> bool:
        if self is other:
            return True
        
        return isinstance(other, type(self)) and self.args == other.args


    def __hash__(self) -> int:
        h = hashlib.md5(self.fsymbol.encode())
        for arg in self.args:
            h.update(abs(hash(arg)).to_bytes(16, 'big'))

        return int(h.hexdigest(), 16)
    
    def __getitem__(self, index) -> TRSTerm:
        return self.args[index]
    
    def size(self) -> int:
        '''
        Return the size of the abstract syntax tree.
        '''
        return 1 + sum(arg.size() for arg in self.args)
    
    def variables(self) -> set[str]:
        '''
        Return a set of (the name of) all variables in this term. (including the bind variables)
        '''
        res = set()
        for arg in self.args:
            res |= arg.variables()
        return res
    
    def substitute(self, sigma : Subst) -> TRSTerm:
        
        new_args = tuple(
            arg.substitute(sigma) for arg in self.args
        )
        return type(self)(*new_args)

class BindVarTerm(TRSTerm):
    fsymbol_print = 'bind'
    fsymbol = 'BIND'

    '''
    The TRSTerm with a bind variable
    '''
    def __init__(self, bind_var: TRSVar, body: TRSTerm):
        self.bind_var = bind_var
        self.body = body

    def __str__(self) -> str:
        return f"({self.fsymbol_print} {self.bind_var}.{self.body})"
    
    def __repr__(self) -> str:
        return f"{self.fsymbol}[{repr(self.bind_var)}]({repr(self.body)})"
    
    def tex(self) -> str:
        return rf" \left ({self.fsymbol_print}\ {self.bind_var.tex()}.{self.body.tex()} \right )"
    
    def __eq__(self, __value: TRSTerm) -> bool:
        '''
        alpha-conversion is considered in the syntactical equivalence of bind variable expressions
        '''
        if self is __value:
            return True
        
        if isinstance(__value, BindVarTerm):
            if self.bind_var == __value.bind_var:
                return self.body == __value.body
            else:
                new_v = var_rename(self.variables() | __value.variables())
                return self.rename_bind(TRSVar(new_v)) == __value.rename_bind(TRSVar(new_v))
        
        else:
            return False
    
    def __hash__(self) -> int:
        '''
        To make the hash value of the term unique, we need to consider the alpha-conversion of the bind variable.
        '''
        canonical_var = var_rename(self.free_variables())
        h = hashlib.md5(self.fsymbol.encode())
        h.update(canonical_var.encode())
        h.update(abs(
            hash(
                self.body.substitute(
                    Subst({self.bind_var.name: TRSVar(canonical_var)})
                    )
                )).to_bytes(16, 'big')
            )
        return int(h.hexdigest(), 16)
    
    def size(self) -> int:
        return self.body.size() + 2
    
    def variables(self) -> set[str]:
        return self.body.variables() | {self.bind_var.name}
    
    def free_variables(self) -> set[str]:
        res = self.body.variables()
        res.discard(self.bind_var.name)
        return res
    
    @property
    def is_ground(self) -> bool:
        return len(self.free_variables()) == 0


    def rename_bind(self, new_v: TRSVar) -> BindVarTerm:
        '''
        rename the bind variable to a new one.
        '''
        return type(self)(new_v, self.body.substitute(Subst({self.bind_var.name: new_v})))
    
    def substitute(self, sigma: Subst) -> BindVarTerm:
        '''
        check whether the bind variable appears in sigma.
        change the bind variable if so.
        '''
        vset = sigma.domain | sigma.vrange
        if self.bind_var.name not in vset:
            return type(self)(self.bind_var, self.body.substitute(sigma))
        else:
            new_v = TRSVar(var_rename(vset))
            new_sigma = sigma.composite(Subst({self.bind_var.name : new_v}))
            return type(self)(new_v, self.body.substitute(new_sigma))
            

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
        return "{\n\t" + ", \n\t".join(f"{key} ↦ {self.data[key]}" for key in self.data) + "\n}"
    
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
        '''
        variable range: the variables occuring in the range
        '''
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
            elif isinstance(lhs, StdTerm):
                if isinstance(rhs, TRSVar):
                    return None
            
                elif isinstance(rhs, StdTerm):
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
    
class TRSInfixBinary(StdTerm):
    def __init__(self, L : TRSTerm, R : TRSTerm):
        super().__init__(L, R)

    def __str__(self) -> str:
        return f'({str(self.args[0])} {self.fsymbol_print} {str(self.args[1])})'

    def __repr__(self) -> str:
        return f'({repr(self.args[0])} {self.fsymbol} {repr(self.args[1])})'
    
    def substitute(self, sigma: Subst) -> TRSTerm:
        return super().substitute(sigma)
    
class TRSCommBinary(StdTerm):
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
    

class TRSCommBinary_safe(StdTerm):
    '''
    TRSCommBinary_safe does not try to sort the operands, but compare them one by one. The hash value calculation is adjusted accordingly.

    This is less efficient but more robust.
    '''
    def __init__(self, L : Any, R : Any):
        super().__init__(L, R)

    def __str__(self) -> str:
        return f'{self.fsymbol_print}({str(self.args[0])}, {str(self.args[1])})'

    def __repr__(self) -> str:
        return f'{self.fsymbol}({repr(self.args[0])}, {repr(self.args[1])})'
    
    def substitute(self, sigma: Subst) -> TRSTerm:
        return super().substitute(sigma)

    def __eq__(self, other):
        if self is other:
            return True
        
        if isinstance(other, TRSCommBinary_safe):
            if self.args[0] == other.args[0] and self.args[1] == other.args[1]:
                return True
            
            if self.args[0] == other.args[1] and self.args[1] == other.args[0]:
                return True
            
            return False
        
        else:
            return False
        
    def __hash__(self) -> int:
        h = int(hashlib.md5(self.fsymbol.encode()).hexdigest(), 16)

        return h + hash(self.args[0]) + hash(self.args[1])
    

class TRS_AC(StdTerm):

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
            TRS_AC.__init__(obj, *tup)
            return obj
        
    def __init__(self, *tup: Any):
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
    
    def tex(self) -> str:
        return rf' \left ({f" {self.fsymbol_print} ".join(map(lambda x: x.tex(), self.args))} \right )'
    
    def substitute(self, sigma: Subst) -> TRSTerm:
        return type(self)(*tuple(arg.substitute(sigma) for arg in self.args))
    
    def remained_terms(self, *idx: int):
        '''
        collect the terms that are not in the idx, and return as a new tuple.
        '''
        return tuple(self.args[i] for i in range(len(self.args)) if i not in idx)
    

class TRS_AC_safe(StdTerm):
    '''
    TRS_AC_safe does not try to sort the operands, but compare them one by one. The hash value calculation is adjusted accordingly.

    This is less efficient but more robust.
    '''

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
            TRS_AC_safe.__init__(obj, *tup)
            return obj
        
    def __init__(self, *tup: Any):
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

        self.args = tuple(new_ls)

    def __str__(self) -> str:
        return f'({f" {self.fsymbol_print} ".join(map(str, self.args))})'
    
    def __repr__(self) -> str:
        return f'({f" {self.fsymbol} ".join(map(repr, self.args))})'
    
    def tex(self) -> str:
        return rf' \left ({f" {self.fsymbol_print} ".join(map(lambda x: x.tex(), self.args))} \right )'
    
    def substitute(self, sigma: Subst) -> TRSTerm:
        return type(self)(*tuple(arg.substitute(sigma) for arg in self.args))
    
    def remained_terms(self, *idx: int):
        '''
        collect the terms that are not in the idx, and return as a new tuple.
        '''
        return tuple(self.args[i] for i in range(len(self.args)) if i not in idx)
    
    def __eq__(self, other):
        if self is other:
            return True
        
        if isinstance(other, TRS_AC_safe):
            if len(self.args) != len(other.args):
                return False
            
            ls_self = list(self.args)
            ls_other = list(other.args)

            for i in range(len(ls_self)):
                if ls_self[i] in ls_other:
                    ls_other.remove(ls_self[i])
                else:
                    return False
                
            return True
        
        else:
            return False
        
    def __hash__(self) -> int:
        h = int(hashlib.md5(self.fsymbol.encode()).hexdigest(), 16)
        for arg in self.args:
            h += hash(arg)

        return h

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
            return False
        elif isinstance(term, StdTerm):
            for arg in term.args:
                if check_special_symbol(arg):
                    return True
            return False
        else:
            return False


def normal_rewrite(self, term : TRSTerm, side_info : dict[str, Any]) -> TRSTerm | None:
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
                 rule_name:str,
                 lhs: TRSTerm|str, 
                 rhs: TRSTerm|str,
                 rewrite_method : Callable[[TRSRule, TRSTerm, Dict[str, Any]], TRSTerm|None] = normal_rewrite,
                 rule_repr: str|None = None):
        '''
        note: the rewrite_method checks whether the current rule can rewrite the given term (not including subterms)
        '''
        self.rewrite_method = rewrite_method

        if isinstance(lhs, StdTerm) and check_special_symbol(lhs):
            raise ValueError(f"The rule {{{lhs}->{rhs}}} should not contain special symbols in the LHS.")

        self.rule_name = rule_name
        self.lhs = lhs
        self.rhs = rhs
        self.rule_repr = rule_repr

    def __str__(self) -> str:
        return f'{self.lhs} → {self.rhs}'

    def __repr__(self) -> str:
        if self.rule_repr is not None:
            return self.rule_repr
        
        str_lhs = self.lhs if isinstance(self.lhs, str) else repr(self.lhs)
        str_rhs = self.rhs if isinstance(self.rhs, str) else repr(self.rhs)
        return f'{str_lhs} -> {str_rhs} ;'

        
# define rule for AC symbols by defining new class
        

######################################################################
# term rewriting system
        
class TRS:

    def __init__(self, 
                 rules: List[TRSRule], 
                 side_info_procs: Tuple[Callable[[Dict[str, Any]], Dict[str, Any]],...] = (),
                 ):
        '''
        side_info_procs provides methods to preprocess side informations (executed in sequence)
        '''
        self.rules : List[TRSRule] = rules
        self.side_info_procs = side_info_procs

    def variables(self) -> set[str]:
        '''
        Return a set of all free variables in the rules.
        (This method is not that rigorous, and only acts as a hint.)
        '''
        res = set()
        for rule in self.rules:
            if isinstance(rule.lhs, TRSTerm) and isinstance(rule.rhs, TRSTerm):
                res |= rule.lhs.variables() | rule.rhs.variables()
        return res
    
    def CiME2_rules(self) -> str:
        '''
        output the TRS rules for CiME2 as a string
        '''
        res = ""

        # print the rules
        for rule in self.rules:
            res += repr(rule) + "\n"
        return res
    
    def substitute(self, sigma : Subst) -> TRS:
        '''
        Apply the substitution on the TRS. Return the result.
        '''
        new_rules = []
        for rule in self.rules:
            new_lhs = rule.lhs.substitute(sigma) if isinstance(rule.lhs, TRSTerm) else rule.lhs
            new_rhs = rule.rhs.substitute(sigma) if isinstance(rule.rhs, TRSTerm) else rule.rhs
            new_rules.append(TRSRule(rule.rule_name, new_lhs, new_rhs, rule.rewrite_method, rule.rule_repr))

        return TRS(new_rules)

    def normalize(self, 
            term : TRSTerm, 
            side_info : dict[str, Any] = {},
            verbose: bool = False, 
            step_limit : int | None = None,
            alg: str = "inner_most") -> TRSTerm:

        # check the variable conincidence
        overlap = term.variables() & self.variables()
        if len(overlap) > 0:
            if verbose:
                print("Renaming rule variables...")

            subst = {}
            for var in overlap:
                subst[var] = TRSVar(var_rename(overlap|set(subst.keys()), var))
            
            renamed_trs = self.substitute(Subst(subst))

        else:
            renamed_trs = self

        # execute the preprocess of side information
        for proc in self.side_info_procs:
            side_info = proc(side_info)

        current_term = term          

        # choose the algorithm
        if alg == "outer_most":
            rewrite = self.rewrite_outer_most  
        elif alg == "inner_most":
            rewrite = self.rewrite_inner_most

        step=0
        while True:

            # check whether the step limit is reached
            step += 1
            if step_limit is not None and step > step_limit:
                return current_term

            if verbose:
                print(f"== STEP {step} ==\n")
                
            # check whether rewrite rules are applicable
            new_term = rewrite(current_term, side_info, verbose)
            if new_term is None:
                return current_term
            
            current_term = new_term
            
    

    def rewrite_outer_most(self, term : TRSTerm, side_info: dict[str, Any], verbose:bool = False) -> TRSTerm | None:
        '''
        rewrite the term using the rules. Return the result.
        return None when no rewriting is applicable

        algorithm: outer most
        '''

        # try to rewrite the term using the rules
        for rule in self.rules:
            new_term = rule.rewrite_method(rule, term, side_info)
            if new_term is not None:
                # output information
                if verbose:
                    print(f"apply {rule.rule_name}: {term} -> {new_term}")
                return new_term
                        
        if isinstance(term, StdTerm):
            # try to rewrite the subterms
            for i in range(len(term.args)):
                new_subterm = self.rewrite_outer_most(term.args[i], side_info, verbose)
                if new_subterm is not None:
                    return type(term)(*term.args[:i], new_subterm, *term.args[i+1:])
                
        elif isinstance(term, BindVarTerm):
            new_body = self.rewrite_outer_most(term.body, side_info, verbose)
            if new_body is not None:
                # risk exists: term.bind_var may collide with new_body
                # but normal rewriting rules should not cause this problem because there are no free variables on the RHS
                return type(term)(term.bind_var, new_body)

        return None
    

    def rewrite_inner_most(self, term : TRSTerm, side_info: dict[str, Any], verbose:bool = False) -> TRSTerm | None:
        '''
        rewrite the term using the rules. Return the result.
        return None when no rewriting is applicable

        algorithm: outer most
        '''

        if isinstance(term, StdTerm):
            # try to rewrite the subterms
            for i in range(len(term.args)):
                new_subterm = self.rewrite_inner_most(term.args[i], side_info, verbose)
                if new_subterm is not None:
                    return type(term)(*term.args[:i], new_subterm, *term.args[i+1:])
                
        elif isinstance(term, BindVarTerm):
            new_body = self.rewrite_inner_most(term.body, side_info, verbose)
            if new_body is not None:
                # risk exists: term.bind_var may collide with new_body
                # but normal rewriting rules should not cause this problem because there are no free variables on the RHS
                return type(term)(term.bind_var, new_body)


        # try to rewrite the term using the rules
        for rule in self.rules:
            new_term = rule.rewrite_method(rule, term, side_info)
            if new_term is not None:
                # output information
                if verbose:
                    print(f"apply {rule.rule_name}: {term} -> {new_term}")
                return new_term
        
        return None