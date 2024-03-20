from __future__ import annotations

from ..dirac.syntax import *

from ..trs import BindVarTerm, MultiBindTerm, new_var, new_var_ls, seq_content_eq

import itertools

#####################################
# transpose

class Transpose(DiracNotation, StdTerm):
    fsymbol_print = "TP"
    fsymbol = "TP"

    def __init__(self, X : Term):
        super().__init__(X)

    def __str__(self) -> str:
        return str(IndexBlock(str(self.args[0]), UR_index="⊤"))
    
    def tex(self) -> str:
        return rf" {self.args[0].tex()}^\top"
    
#####################################
# high-level constructions


class Abstract(BindVarTerm):
    fsymbol_print = "λ"
    fsymbol = "LAMBDA"

    def tex(self) -> str:
        return rf" \left ( \lambda {self.bind_var.name} . {self.body.tex()} \right )"
    
class Apply(StdTerm):
    fsymbol_print = "apply"
    fsymbol = "APPLY"

    def __init__(self, f: Term, x: Term):
        super().__init__(f, x)

    def __str__(self) -> str:
        return str(HSeqBlock(
            str(self.args[0]), ' ', str(self.args[1]), 
            v_align='c'))

    def tex(self) -> str:
        return rf" \left ({self.args[0].tex()} {self.args[1].tex()} \right)"
    
###################################################################
# syntax for set

class SetTerm(Term):
    ...

class EmptySet(SetTerm, StdTerm):
    fsymbol_print = "∅"
    fsymbol = "ESET"

    def __str__(self) -> str:
        return "∅"
    
    def __repr__(self) -> str:
        return "ESET"
    
    def tex(self) -> str:
        return r" \emptyset"
    
class UniversalSet(SetTerm, StdTerm):
    fsymbol_print = "𝐔"
    fsymbol = "USET"

    def __str__(self) -> str:
        return "𝐔"
    
    def __repr__(self) -> str:
        return "USET"
    
    def tex(self) -> str:
        return r" \mathbf{U}"

class UnionSet(SetTerm, AC):
    fsymbol_print = "∪"
    fsymbol = "UNION"

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)


    def tex(self) -> str:
        return "( " + " \\cup ".join([s.tex() for s in self.args]) + " )"


class SumTemplate(MultiBindTerm):
    fsymbol_print = 'SumTemplate'
    fsymbol = 'SumTemplate'

    def __new__(cls, bind_vars: Tuple[Tuple[Var, Term], ...], body: Term):
        if len(bind_vars) == 0:
            return body
        else:
            obj = object.__new__(cls)
            SumTemplate.__init__(obj, bind_vars, body)
            return obj

    def __init__(self, bind_vars: Tuple[Tuple[Var, Term], ...], body: Term):
        # try to flatten
        if isinstance(body, type(self)):
            bind_vars = bind_vars + body.bind_vars
            body = body.body

        self.bind_vars = tuple(bind_vars)
        self.body = body

    def __str__(self) -> str:
        raise NotImplementedError()
    
    def __repr__(self) -> str:
        raise NotImplementedError()
    
    def tex(self) -> str:
        raise NotImplementedError()
    
    def __eq__(self, __value: Term) -> bool:
        '''
        alpha-conversion is considered in the syntactical equivalence of bind variable expressions
        '''
        if self is __value:
            return True
        
        if isinstance(__value, type(self)):
            if len(self.bind_vars) != len(__value.bind_vars):
                return False
            
            # first find common bind variable renaming list
            new_vars = new_var_ls(self.variables() | __value.variables(), len(self.bind_vars))

            self_renamed = self.rename_bind(tuple(v for v in new_vars))

            # try different bind variable sequences
            for perm in itertools.permutations(new_vars):
                other_renamed = __value.rename_bind(tuple(v for v in perm))
                # we check two parts: the body are the same, and the bind variables (with sets) have same contents
                if self_renamed.body == other_renamed.body and \
                    seq_content_eq(self_renamed.bind_vars, other_renamed.bind_vars):
                    return True
                
            return False
        
        else:
            return False

    
    def size(self) -> int:
        return self.body.size() + len(self.bind_vars) + 1
    
    def variables(self) -> set[Var]:
        bind_vars = set()
        for v, t in self.bind_vars:
            bind_vars.add(v.name)

        set_vars = set()
        for v, t in self.bind_vars:
            set_vars |= t.variables()

        return (self.body.variables() | set_vars) - bind_vars
    
    @property
    def is_ground(self) -> bool:
        return len(self.variables()) == 0


    def rename_bind(self, new_vars: Tuple[Var, ...]) -> SumTemplate:
        '''
        rename the bind variables in order
        '''
        sub_dist = {}
        for i, new_v in enumerate(new_vars):
            sub_dist[self.bind_vars[i][0]] = new_v

        new_vars_with_set = tuple(zip(new_vars, [t.subst(Subst(sub_dist)) for v, t in self.bind_vars]))

        return type(self)(new_vars_with_set, self.body.subst(Subst(sub_dist)))
    

    def avoid_vars(self, var_set: set[Var]) -> SumTemplate:
        '''
        return the bind variable term which avoids bind variables in var_set
        '''
        bind_var_names = set(v for v, t in self.bind_vars)
        if len(bind_var_names & var_set) > 0 :
            new_bind_var_ls = new_var_ls(var_set | self.variables(), len(self.bind_vars))
            return self.rename_bind(new_bind_var_ls)
        
        else:
            return self
        
    def subst(self, sigma: Subst | dict[Var, Term]) -> SumTemplate:
        '''
        check whether the bind variable appears in sigma.
        change the bind variable if so.
        '''

        if not isinstance(sigma, Subst):
            sigma = Subst(sigma)


        vset = sigma.domain | sigma.vrange
        bind_vars_set = set(map(lambda x:x[0], self.bind_vars))
        
        if len(bind_vars_set & vset) == 0:
            new_vars_with_set = tuple([(v, t.subst(sigma)) for v, t in self.bind_vars])
            return type(self)(new_vars_with_set, self.body.subst(sigma))
        else:
            new_vars = new_var_ls(vset, len(self.bind_vars))

            sub_dist = {}
            for i, new_v in enumerate(new_vars):
                sub_dist[self.bind_vars[i][0]] = new_v

            new_vars_with_set = tuple([(new_vars[i], self.bind_vars[i][1].subst(sigma)) for i in range(len(new_vars))])

            new_sigma = sigma.composite(Subst(sub_dist))
            return type(self)(new_vars_with_set, self.body.subst(new_sigma))
            

class SumS(DiracNotation, SumTemplate):
    fsymbol_print = "sums"
    fsymbol = "SUMS"

    def __str__(self) -> str:
        vars_names = ", ".join([f'{v.name} ∈ {str(t)}' for v, t in self.bind_vars])
        return str(HSeqBlock(
            IndexBlock('__\n\\ \n/ \n‾‾', D_index=vars_names), " ", str(self.body)))
    
    def __repr__(self) -> str:
        return f"SumS({repr(self.bind_vars)}, {repr(self.body)})"

    def tex(self) -> str:
        vars_names = ", ".join([rf'{v.name} \in {t.tex()}' for v, t in self.bind_vars])
        return rf" \left ( \sum_{{{vars_names}}} {self.body.tex()} \right )"
    

class Sum(DiracNotation, SumTemplate):
    fsymbol_print = "sum"
    fsymbol = "SUM"

    def __str__(self) -> str:
        vars_names = ", ".join([f'{v.name} ∈ {str(t)}' for v, t in self.bind_vars])
        return str(HSeqBlock(
            IndexBlock('__\n\\ \n/ \n‾‾', D_index=vars_names), " ", str(self.body)))
    
    def __repr__(self) -> str:
        return f"Sum({repr(self.bind_vars)}, {repr(self.body)})"

    def tex(self) -> str:
        vars_names = ", ".join([rf'{v.name} \in {t.tex()}' for v, t in self.bind_vars])
        return rf" \left ( \sum_{{{vars_names}}} {self.body.tex()} \right )"
    

#####################################
# section-2 syntax
    
class Juxtapose(DiracScalar, CommBinary):
    '''
    Note: this rule is only for internal representation, and should not be used in the user interface or parsing
    '''
    fsymbol_print = "JUXT"
    fsymbol = "JUXT"

    def __init__(self, A: Term, B: Term):
        super().__init__(A, B)

    def __str__(self) -> str:
        '''
        use the first one to represent
        '''
        return str(self.args[0])
    
    def tex(self) -> str:
        '''
        use the first one to represent
        '''
        return self.args[0].tex()




