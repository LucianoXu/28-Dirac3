

from __future__ import annotations
import itertools

from typing import Type

from ply import yacc


from ..trs import *
from .syntax import *
from ..atomic_base import AtomicBase
from ..complex_scalar import ComplexScalar

from ..dirac.trs import construct_trs as dirac_construct_trs

def construct_trs(
        CScalar: Type[ComplexScalar], 
        ABase: Type[AtomicBase], 
        parse: Callable[[str], Any]) -> Tuple[TRS, Callable[[Term], Term]]:
    '''
    Return:
        - the first TRS is the trs for the bigop theory
        - the second function transform the term to apply juxtapose rule once.
        - the thrid function applies the sumeq extension.
    '''
    
    # inherit the rules from dirac
    trs = dirac_construct_trs(CScalar, ABase, parse)

    #####################################################
    # transpose

    trs.append(CanonicalRule(
        "TRANS-UNI-1",
        lhs = parse(r'''TP(0X)'''),
        rhs = parse(r'''0X'''),
    ))

    trs.append(CanonicalRule(
        "TRANS-UNI-2",
        lhs = parse(r'''TP(ADJ(X0))'''),
        rhs = parse(r'''ADJ(TP(X0))''')
    ))

    trs.append(CanonicalRule(
        "TRANS-UNI-3",
        lhs = parse(r'''TP(TP(X0))'''),
        rhs = parse(r'''X0'''),
    ))

    trs.append(CanonicalRule(
        "TRANS-UNI-4",
        lhs = parse(r'''TP(S0 SCR X0)'''),
        rhs = parse(r'''S0 SCR TP(X0)'''),
    ))

    def trans_5_rewrite(rule, trs, term):
        if isinstance(term, Transpose) and isinstance(term.args[0], Add):
                new_args = tuple(Transpose(arg) for arg in term.args[0].args)
                return Add(*new_args)
    trs.append(Rule(
        "TRANS-UNI-5",
        lhs = "TP(X1 ADD X2)",
        rhs = "TP(X1) ADD TP(X2)",
        rewrite_method=trans_5_rewrite
    ))

    trs.append(CanonicalRule(
        "TRANS-KET-1",
        lhs = parse(r'''TP(BRA(s))'''),
        rhs = parse(r'''KET(s)'''),
    ))

    trs.append(CanonicalRule(
        "TRANS-KET-2",
        lhs = parse(r'''TP(B0 MLTB O0)'''),
        rhs = parse(r'''TP(O0) MLTK TP(B0)''')
    ))

    trs.append(CanonicalRule(
        "TRANS-KET-3",
        lhs = parse(r'''TP(B1 TSRB B2)'''),
        rhs = parse(r'''TP(B1) TSRK TP(B2)''')
    ))

    trs.append(CanonicalRule(
        "TRANS-BRA-1",
        lhs = parse(r'''TP(KET(s))'''),
        rhs = parse(r'''BRA(s)'''),
    ))

    trs.append(CanonicalRule(
        "TRANS-BRA-2",
        lhs = parse(r'''TP(O0 MLTK K0)'''),
        rhs = parse(r'''TP(K0) MLTB TP(O0)''')
    ))

    trs.append(CanonicalRule(
        "TRANS-BRA-3",
        lhs = parse(r'''TP(K1 TSRK K2)'''),
        rhs = parse(r'''TP(K1) TSRB TP(K2)''')
    ))

    trs.append(CanonicalRule(
        "TRANS-OPT-1",
        lhs = parse(r'''TP(1O)'''),
        rhs = parse(r'''1O'''),
    ))

    trs.append(CanonicalRule(
        "TRANS-OPT-2",
        lhs = parse(r'''TP(K0 OUTER B0)'''),
        rhs = parse(r'''TP(B0) OUTER TP(K0)''')
    ))

    trs.append(CanonicalRule(
        "TRANS-OPT-3",
        lhs = parse(r'''TP(O1 MLTO O2)'''),
        rhs = parse(r'''TP(O2) MLTO TP(O1)''')
    ))

    trs.append(CanonicalRule(
        "TRANS-OPT-4",
        lhs = parse(r'''TP(O1 TSRO O2)'''),
        rhs = parse(r'''TP(O1) TSRO TP(O2)''')
    ))

    #####################################################
    # set-simp
    def set_simp_1_rewrite(rule, trs, term):
        if isinstance(term, UnionSet):
            for s in term.args:
                if s == UniversalSet():
                    return UniversalSet()
                
    trs.append(Rule(
        "SET-SIMP-1",
        lhs = "USET UNION X",
        rhs = "USET",
        rewrite_method = set_simp_1_rewrite
    ))

    def set_simp_2_rewrite(rule, trs, term):
        if isinstance(term, UnionSet):
            for i, s in enumerate(term.args):
                if s == EmptySet():
                    return UnionSet(*term.remained_terms(i))
                
    trs.append(Rule(
        "SET-SIMP-2",
        lhs = "ESET UNION X",
        rhs = "X",
        rewrite_method = set_simp_2_rewrite
    ))

    #####################################################
    # sum-elim

    def sum_elim_1_rewrite(rule, trs, term):
        if isinstance(term, SumS) and term.body == CScalar.zero():
            return CScalar.zero()
    trs.append(Rule(
        "SUM-ELIM-1",
        lhs = "SUMS(i, T, C(0))",
        rhs = "C(0)",
        rewrite_method = sum_elim_1_rewrite
    ))


    def sum_elim_2_rewrite(rule, trs, term):
        if isinstance(term, Sum) and isinstance(term.body, Zero):
            return type(term.body)()
    trs.append(Rule(
        "SUM-ELIM-2",
        lhs = "SUM(i, T, 0X)",
        rhs = "0X",
        rewrite_method = sum_elim_2_rewrite
    ))




    def sum_elim_3_rewrite(rule, trs, term):
        if isinstance(term, SumS) and isinstance(term.body, ScalarDelta):
            for i, v in enumerate(term.bind_vars):
                if v[0] == term.body.args[0]:
                    s = term.body.args[1]
                elif v[0] == term.body.args[1]:
                    s = term.body.args[0]
                else:
                    continue
            
                if v[0] not in s.variables() and v[1] == UniversalSet():
                    new_bind_vars = term.bind_vars[:i]+term.bind_vars[i+1:]
                    return SumS(new_bind_vars, CScalar.one())
                        
    trs.append(Rule(
        "SUM-ELIM-3",
        lhs = "SUMS(i, USET, DELTA(i, s))",
        rhs = "C(1)",
        rewrite_method = sum_elim_3_rewrite
    ))

    def sum_elim_4_rewrite(rule, trs, term):
        if isinstance(term, SumS) and isinstance(term.body, ScalarMlt):
            for i, item in enumerate(term.body.args):
                if isinstance(item, ScalarDelta):
                    for j, v in enumerate(term.bind_vars):
                        if v[0] == item.args[0]:
                            s = item.args[1]
                        elif v[0] == item.args[1]:
                            s = item.args[0]
                        else:
                            continue
                        
                        if v[0] not in s.variables() and v[1] == UniversalSet():
                            new_bind_vars = term.bind_vars[:j]+term.bind_vars[j+1:]

                            sub = Subst({v[0] : s})
                            return SumS(new_bind_vars, ScalarMlt(*term.body.remained_terms(i)).subst(sub))
                                    
    trs.append(Rule(
        "SUM-ELIM-4",
        lhs = "SUMS(i, USET, DELTA(i, s) MLTS S0)",
        rhs = "S0[i:=s]",
        rewrite_method = sum_elim_4_rewrite
    ))


    def sum_elim_5_rewrite(rule, trs, term):
        if isinstance(term, Sum) and isinstance(term.body, Scal) and isinstance(term.body.args[0], ScalarDelta):
            delta = term.body.args[0]
            for i, v in enumerate(term.bind_vars):

                if v[0] == delta.args[0]:
                    s = delta.args[1]
                elif v[0] == delta.args[1]:
                    s = delta.args[0]
                else:
                    continue
                
                if v[0] not in s.variables() and v[1] == UniversalSet():
                    new_bind_vars = term.bind_vars[:i]+term.bind_vars[i+1:]

                    sub = Subst({v[0] : s})
                    return Sum(new_bind_vars, term.body.args[1].subst(sub))
            
            
    trs.append(Rule(
        "SUM-ELIM-5",
        lhs = "SUM(i, USET, DELTA(i, s) SCR X)",
        rhs = "X[i:=s]",
        rewrite_method = sum_elim_5_rewrite
    ))


    def sum_elim_6_rewrite(rule, trs, term):
        if isinstance(term, Sum) and isinstance(term.body, Scal) and isinstance(term.body.args[0], ScalarMlt):
            for i, delta in enumerate(term.body.args[0].args):
                if isinstance(delta, ScalarDelta):
                    for j, v in enumerate(term.bind_vars):
                        if v[0] == delta.args[0]:
                            s = delta.args[1]
                        elif v[0] == delta.args[1]:
                            s = delta.args[0]
                        else:
                            continue
                        
                        if v[0] not in s.variables() and v[1] == UniversalSet():
                            new_bind_vars = term.bind_vars[:j]+term.bind_vars[j+1:]

                            sub = Subst({v[0] : s})

                            return Sum(new_bind_vars, type(term.body)(ScalarMlt(*term.body.args[0].remained_terms(i)).subst(sub), term.body.args[1].subst(sub)))
                        
            
    trs.append(Rule(
        "SUM-ELIM-6",
        lhs = "SUM(i, USET, (DELTA(i, s) MLTS S0) SCR X)",
        rhs = "S[i:=s] SCR X[i:=s]",
        rewrite_method = sum_elim_6_rewrite
    ))



    def sum_dist_1_rewrite(rule, trs, term):
        if isinstance(term, SumS) and isinstance(term.body, ScalarMlt):
            for i, item in enumerate(term.body.args):
                if set(v[0] for v in term.bind_vars) & item.variables() == set():
                    rest_body = ScalarMlt(*term.body.remained_terms(i))
                    return ScalarMlt(item, SumS(term.bind_vars, rest_body))
    trs.append(Rule(
        "SUM-DIST-1",
        rhs = "SUMS(i, T, S1 MLTS X)",
        lhs = "SUMS(i, T, S1) MLTS X",
        rewrite_method = sum_dist_1_rewrite
    ))


    def sum_dist_2_rewrite(rule, trs, term):
        if isinstance(term, ScalarConj) and isinstance(term.args[0], SumS):
            return SumS(term.args[0].bind_vars, ScalarConj(term.args[0].body))
    trs.append(Rule(
        "SUM-DIST-2",
        lhs = "CONJS(SUMS(i, T, A))",
        rhs = "SUMS(i, T, CONJS(A))",
        rewrite_method = sum_dist_2_rewrite
    ))



    def sum_dist_3_rewrite(rule, trs, term):
        if isinstance(term, Adj) and isinstance(term.args[0], Sum):
            return Sum(term.args[0].bind_vars, Adj(term.args[0].body))
    trs.append(Rule(
        "SUM-DIST-3",
        lhs = "ADJ(SUM(i, T, A))",
        rhs = "SUM(i, T, ADJ(A))",
        rewrite_method = sum_dist_3_rewrite
    ))


    def sum_dist_4_rewrite(rule, trs, term):
        if isinstance(term, Transpose) and isinstance(term.args[0], Sum):
            return Sum(term.args[0].bind_vars, Transpose(term.args[0].body))
    trs.append(Rule(
        "SUM-DIST-4",
        lhs = "TP(SUM(i, T, A))",
        rhs = "SUM(i, T, TP(A))",
        rewrite_method = sum_dist_4_rewrite
    ))


    def sum_dist_5_rewrite(rule, trs, term):
        if isinstance(term, Sum) and isinstance(term.body, Scal) and \
            set(v[0] for v in term.bind_vars) & term.body.args[0].variables() == set():
            return Scal(term.body.args[0], Sum(term.bind_vars, term.body.args[1]))
    trs.append(Rule(
        "SUM-DIST-5",
        lhs = "SUM(i, T, X SCR A)",
        rhs = "X SCR SUM(i, T, A)",
        rewrite_method = sum_dist_5_rewrite
    ))

    def sum_dist_6_rewrite(rule, trs, term):
        if isinstance(term, Sum) and isinstance(term.body, Scal) and \
            set(v[0] for v in term.bind_vars) & term.body.args[1].variables() == set():
            return Scal(SumS(term.bind_vars, term.body.args[0]), term.body.args[1])
    trs.append(Rule(
        "SUM-DIST-6",
        lhs = "SUM(i, T, A SCR X)",
        rhs = "SUMS(i, T, A) SCR X",
        rewrite_method = sum_dist_6_rewrite
    ))
    
    #####################################################
    # sum-distribution

    def sum_dist_7_rewrite(rule, trs, term):
        if isinstance(term, Sum) and isinstance(term.body, (ScalarDot, KetApply, BraApply, OpApply)) and \
            set(v[0] for v in term.bind_vars) & term.body.args[1].variables() == set():
            return type(term.body)(Sum(term.bind_vars, term.body.args[0]), term.body.args[1])
    trs.append(Rule(
        "SUM-DIST-7",
        lhs = "SUM(x, T, x1 {DOT/MLTK/MLTB/MLTO} X)",
        rhs = "SUM(x, T, x1) {DOT/MLTK/MLTB/MLTO} X",
        rewrite_method = sum_dist_7_rewrite
    ))

    def sum_dist_8_rewrite(rule, trs, term):
        if isinstance(term, Sum) and isinstance(term.body, (ScalarDot, KetApply, BraApply, OpApply)) and \
            set(v[0] for v in term.bind_vars) & term.body.args[0].variables() == set():
            return type(term.body)(term.body.args[0], Sum(term.bind_vars, term.body.args[1]))
    trs.append(Rule(
        "SUM-DIST-8",
        lhs = "SUM(x, T, X {DOT/MLTK/MLTB/MLTO} x2)",
        rhs = "X {DOT/MLTK/MLTB/MLTO} SUM(x, T, x2)",
        rewrite_method = sum_dist_8_rewrite
    ))


    def sum_dist_9_rewrite(rule, trs, term):
        if isinstance(term, Sum) and isinstance(term.body, (KetTensor, BraTensor, OpOuter, OpTensor)) and \
            set(v[0] for v in term.bind_vars) & term.body.args[1].variables() == set():
            return type(term.body)(Sum(term.bind_vars, term.body.args[0]), term.body.args[1])     
    trs.append(Rule(
        "SUM-DIST-9",
        lhs = "SUM(x, T, x1 {TSRK/TSRB/OUTER/TSRO} X)",
        rhs = "SUM(x, T, x1) {TSRK/TSRB/OUTER/TSRO} X",
        rewrite_method = sum_dist_9_rewrite
    ))


    def sum_dist_10_rewrite(rule, trs, term):
        if isinstance(term, Sum) and isinstance(term.body, (KetTensor, BraTensor, OpOuter, OpTensor)) and \
            set(v[0] for v in term.bind_vars) & term.body.args[0].variables() == set():
            return type(term.body)(term.body.args[0], Sum(term.bind_vars, term.body.args[1]))
    trs.append(Rule(
        "SUM-DIST-10",
        lhs = "SUM(x, T, X {TSRK/TSRB/OUTER/TSRO} x2)",
        rhs = "X {TSRK/TSRB/OUTER/TSRO} SUM(x, T, x2)",
        rewrite_method = sum_dist_10_rewrite
    ))

    def sum_comp_1_rewrite(rule, trs, term):
        if isinstance(term, (ScalarDot, KetApply, BraApply, OpApply)) and isinstance(term.args[0], Sum):

            # we have to rename if necessary
            avoided_term = term.args[0].avoid_vars(term.args[1].variables())

            combined_term = type(term)(avoided_term.body, term.args[1])
            norm_term = trs.normalize(combined_term)

            if norm_term != combined_term:
                if type(term) == ScalarDot:
                    return SumS(avoided_term.bind_vars, norm_term)
                else:
                    return Sum(avoided_term.bind_vars, norm_term)
    trs.append(Rule(
        "SUM-COMP-1",
        lhs = "SUM(i, T, A) {DOT/MLTK/MLTB/MLTO} X (with side condition)",
        rhs = "SUM(i, T, A {DOT/MLTK/MLTB/MLTO} X)",
        rewrite_method = sum_comp_1_rewrite
    ))

    def sum_comp_2_rewrite(rule, trs, term):
        if isinstance(term, (ScalarDot, KetApply, BraApply, OpApply)) and isinstance(term.args[1], Sum):

            # we have to rename if necessary
            avoided_term = term.args[1].avoid_vars(term.args[0].variables())

            combined_term = type(term)(term.args[0], avoided_term.body)
            norm_term = trs.normalize(combined_term)

            if norm_term != combined_term:
                if type(term) == ScalarDot:
                    return SumS(avoided_term.bind_vars, norm_term)
                else:
                    return Sum(avoided_term.bind_vars, norm_term)
    trs.append(Rule(
        "SUM-COMP-2",
        lhs = "X {DOT/MLTK/MLTB/MLTO} SUM(i, T, A) (with side condition)",
        rhs = "SUM(i, T, X {DOT/MLTK/MLTB/MLTO} A)",
        rewrite_method = sum_comp_2_rewrite
    ))


    def sum_comp_3_rewrite(rule, trs, term):
        if isinstance(term, (KetTensor, BraTensor, OpOuter, OpTensor)) and isinstance(term.args[0], Sum):

            # we have to rename if necessary
            avoided_term = term.args[0].avoid_vars(term.args[0].variables())

            combined_term = type(term)(avoided_term.body, term.args[1])
            norm_term = trs.normalize(combined_term)

            if norm_term != combined_term:
                return Sum(avoided_term.bind_vars, norm_term)
    trs.append(Rule(
        "SUM-COMP-3",
        lhs = "SUM(i, T, A) {TSRK/TSRB/OUTER/TSRO} X (with side condition)",
        rhs = "SUM(i, T, A {TSRK/TSRB/OUTER/TSRO} X)",
        rewrite_method = sum_comp_3_rewrite
    ))

    def sum_comp_4_rewrite(rule, trs, term):
        if isinstance(term, (KetTensor, BraTensor, OpOuter, OpTensor)) and isinstance(term.args[1], Sum):

            # we have to rename if necessary
            avoided_term = term.args[1].avoid_vars(term.args[0].variables())

            combined_term = type(term)(term.args[0], avoided_term.body)
            norm_term = trs.normalize(combined_term)

            if norm_term != combined_term:
                return Sum(avoided_term.bind_vars, norm_term)
            
    trs.append(Rule(
        "SUM-COMP-4",
        lhs = "X {TSRK/TSRB/OUTER/TSRO} SUM(i, T, A) (with side condition)",
        rhs = "SUM(i, T, X {TSRK/TSRB/OUTER/TSRO} A)",
        rewrite_method = sum_comp_4_rewrite
    ))

    def sum_comp_5_rewrite(rule, trs, term):
        if isinstance(term, SumS) and \
            set(v[0] for v in term.bind_vars) & term.body.variables() == set():
            if term.body != CScalar.one():
                return ScalarMlt(SumS(term.bind_vars, CScalar.one()), term.body)

    trs.append(Rule(
        "SUM-COMP-5",
        lhs = "SUMS(i, T, S0)",
        rhs = "SUMS(i, T, C(1)) MLTS S0",
        rewrite_method = sum_comp_5_rewrite
    ))


    def sum_comp_6_rewrite(rule, trs, term):
        if isinstance(term, Sum) and \
            set(v[0] for v in term.bind_vars) & term.body.variables() == set():
            return Scal(SumS(term.bind_vars, CScalar.one()), term.body)

    trs.append(Rule(
        "SUM-COMP-6",
        lhs = "SUM(i, T, A)",
        rhs = "SUMS(i, T, C(1)) SCR A",
        rewrite_method = sum_comp_6_rewrite
    ))

    # def sum_add_1_rewrite(rule, trs, term):
    #     if isinstance(term, ScalarAdd):
    #         for i, itemA in enumerate(term.args):
    #             if isinstance(itemA, SumS):
    #                 for j in range(i+1, len(term.args)):
    #                     itemB = term.args[j]
    #                     if isinstance(itemB, SumS):
    #                         new_bind_var = Var(new_var(itemA.variables() | itemB.variables()))
    #                         subA = Subst({
    #                             itemA.bind_var: new_bind_var,
    #                         })
    #                         subB = Subst({
    #                             itemB.bind_var: new_bind_var,
    #                         })
    #                         return type(term)(
    #                             SumS(new_bind_var, ScalarAdd(
    #                                 itemA.body.subst(subA), 
    #                                 itemB.body.subst(subB))),
    #                             *term.remained_terms(i, j))

    # SUM_ADD_1 = Rule(
    #     "SUM-ADD-1",
    #     lhs = "SUMS(i, A) ADDS SUMS(j, B)",
    #     rhs = "SUMS(k, A[i:=k] ADDS B[j:=k])",
    #     rewrite_method = sum_add_1_rewrite
    # )
    # rules.append(SUM_ADD_1)


    # def sum_add_2_rewrite(rule, trs, term):
    #     if isinstance(term, Add):
    #         for i, itemA in enumerate(term.args):
    #             if isinstance(itemA, Sum):
    #                 for j in range(i+1, len(term.args)):
    #                     itemB = term.args[j]
    #                     if isinstance(itemB, Sum):
    #                         new_bind_var = Var(new_var(itemA.variables() | itemB.variables()))
    #                         subA = Subst({
    #                             itemA.bind_var: new_bind_var,
    #                         })
    #                         subB = Subst({
    #                             itemB.bind_var: new_bind_var,
    #                         })
    #                         return type(term)(
    #                             Sum(new_bind_var, Add(
    #                                 itemA.body.subst(subA), 
    #                                 itemB.body.subst(subB))),
    #                             *term.remained_terms(i, j))

    # SUM_ADD_2 = Rule(
    #     "SUM-ADD-2",
    #     lhs = "SUM(i, A) ADD SUM(j, B)",
    #     rhs = "SUM(k, A[i:=k] ADD B[j:=k])",
    #     rewrite_method = sum_add_2_rewrite
    # )
    # rules.append(SUM_ADD_2)

    #####################################################
    # beta-reduction

    def beta_reduction_rewrite(rule, trs, term):
        if isinstance(term, Apply):
            f, x = term.args
            if isinstance(f, Abstract):
                return f.body.subst({f.bind_var: x})
            
    trs.append(Rule(
        "BETA-REDUCTION",
        lhs = "APPLY(LAMBDA(x, A), a)",
        rhs = "A[x := a]",
        rewrite_method = beta_reduction_rewrite,
        rule_repr = "(* beta-reduction: APPLY(LAMBDA(x, A), a) -> A[x := a] ;*)",
    ))



    #####################################################
    # Juxtapose

    def juxtapose_rewrite(term: Term) -> Term:
        if isinstance(term, ScalarDot):
            B, K = term.args[0], term.args[1]
            return Juxtapose(ScalarDot(B, K), ScalarDot(Transpose(K), Transpose(B)))
        
        elif isinstance(term, StdTerm):
            return type(term)(*map(juxtapose_rewrite, term.args))
        
        elif isinstance(term, BindVarTerm):
            return type(term)(term.bind_var, juxtapose_rewrite(term.body))
        
        elif isinstance(term, MultiBindTerm):
            return type(term)(term.bind_vars, juxtapose_rewrite(term.body))
        
        else:
            return term

             
        
    # build the trs
    return trs, juxtapose_rewrite



def construct_entry_trs(
        CScalar: Type[ComplexScalar], 
        ABase: Type[AtomicBase], 
        parse: Callable[[str], Any]) -> TRS:
    '''
    Return:
        - the first TRS is the trs for the bigop theory
        - the second function transform the term to apply juxtapose rule once.
        - the thrid function applies the sumeq extension.
    '''
    
    trs = TRS([])

    def sum_elim_7_rewrite(rule, trs, term):
        if isinstance(term, Sum):
            if isinstance(term.body, Scal) and\
                isinstance(term.body.args[0], ScalarDot) and\
                isinstance(term.body.args[0].args[0], BraBase) and\
                isinstance(term.body.args[1], KetBase):
                    for i, (v, T) in enumerate(term.bind_vars):
                        if v == term.body.args[0].args[0].args[0] and\
                            term.body.args[1].args[0] == v and \
                            T == UniversalSet():
                            return Sum(term.bind_vars[:i]+term.bind_vars[i+1:], term.body.args[0].args[1])
    trs.append(Rule(
        "SUM-ELIM-7",
        lhs = "SUM(i, (BRA(i) DOT K0) SCR KET(i))",
        rhs = "K0",
        rewrite_method = sum_elim_7_rewrite
    ))

    def sum_elim_8_rewrite(rule, trs, term):
        if isinstance(term, Sum):
            if isinstance(term.body, Scal) and\
                isinstance(term.body.args[0], ScalarDot) and\
                isinstance(term.body.args[0].args[1], KetBase) and\
                isinstance(term.body.args[1], BraBase):
                    for i, (v, T) in enumerate(term.bind_vars):
                        if v == term.body.args[0].args[1].args[0] and\
                            term.body.args[1].args[0] == v and \
                            T == UniversalSet():
                            return Sum(term.bind_vars[:i]+term.bind_vars[i+1:], term.body.args[0].args[0])
    trs.append(Rule(
        "SUM-ELIM-8",
        lhs = "SUM(i, (B0 DOT KET(i)) SCR BRA(i))",
        rhs = "B0",
        rewrite_method = sum_elim_8_rewrite
    ))

    def sum_elim_9_rewrite(rule, trs, term):
        '''
        Note: only SUM-SWAP-EQ is considered in matching.
        '''
        if isinstance(term, Sum) and isinstance(term.body, Scal):
            if isinstance(term.body.args[0], ScalarDot) and\
                isinstance(term.body.args[0].args[0], BraBase) and\
                isinstance(term.body.args[0].args[1], KetApply) and\
                isinstance(term.body.args[0].args[1].args[1], KetBase) and\
                isinstance(term.body.args[1], OpOuter) and\
                isinstance(term.body.args[1].args[0], KetBase) and\
                isinstance(term.body.args[1].args[1], BraBase):
                base_i = term.body.args[0].args[0].args[0]
                base_j = term.body.args[0].args[1].args[1].args[0]
                if base_i == term.body.args[1].args[0].args[0] and\
                    base_j == term.body.args[1].args[1].args[0]:
                        for i, (vi, Ti) in enumerate(term.bind_vars):
                            if vi == base_i and Ti == UniversalSet():
                                for j, (vj, Tj) in enumerate(term.bind_vars):
                                    if vj == base_j and Tj == UniversalSet():
                                        if j < i:
                                            i, j = j, i
                                        return Sum(term.bind_vars[:i]+term.bind_vars[i+1:j]+term.bind_vars[j+1:], term.body.args[0].args[1].args[0])
    trs.append(Rule(
        "SUM-ELIM-9",
        lhs = "SUM(i, SUM(j, (BRA(i) DOT (A MLTK KET(j))) SCR (KET(i) OUTER BRA(j)) ))",
        rhs = "A",
        rewrite_method = sum_elim_9_rewrite
    ))

    def sum_elim_10_rewrite(rule, trs, term):
        '''
        Note: only SUM-SWAP-EQ is considered in matching.
        '''
        if isinstance(term, Sum) and isinstance(term.body, Scal):
            if isinstance(term.body.args[0], ScalarDot) and\
                isinstance(term.body.args[0].args[0], BraBase) and\
                isinstance(term.body.args[0].args[1], KetApply) and\
                isinstance(term.body.args[0].args[1].args[1], KetBase) and\
                isinstance(term.body.args[1], OpOuter) and\
                isinstance(term.body.args[1].args[0], KetBase) and\
                isinstance(term.body.args[1].args[1], BraBase):
                base_i = term.body.args[0].args[0].args[0]
                base_j = term.body.args[0].args[1].args[1].args[0]

                if base_j == term.body.args[1].args[0].args[0] and\
                    base_i == term.body.args[1].args[1].args[0]:
                        for i, (vi, Ti) in enumerate(term.bind_vars):
                            if vi == base_i and Ti == UniversalSet():
                                for j, (vj, Tj) in enumerate(term.bind_vars):
                                    if vj == base_j and Tj == UniversalSet():
                                        if j < i:
                                            i, j = j, i
                                        return Sum(term.bind_vars[:i]+term.bind_vars[i+1:j]+term.bind_vars[j+1:], Transpose(term.body.args[0].args[1].args[0]))
                
    trs.append(Rule(
        "SUM-ELIM-10",
        lhs = "SUM(i, SUM(j, (BRA(i) DOT (A MLTK KET(j))) SCR (KET(j) OUTER BRA(i)) ))",
        rhs = "TP(A)",
        rewrite_method = sum_elim_10_rewrite
    ))

    return trs
