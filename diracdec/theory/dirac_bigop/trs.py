

from __future__ import annotations
import itertools

from typing import Type

from ply import yacc


from ..trs import *
from .syntax import *
from ..atomic_base import AtomicBase
from ..complex_scalar import ComplexScalar

from .parser import construct_parser

from ..dirac.trs import construct_trs as dirac_construct_trs

def construct_trs(
        CScalar: Type[ComplexScalar], 
        ABase: Type[AtomicBase], 
        parser: yacc.LRParser|None = None) -> Tuple[TRS, Callable[[TRSTerm], TRSTerm], Callable[[TRSTerm], TRSTerm]]:
    '''
    Return:
        - the first TRS is the trs for the bigop theory
        - the second function transform the term to apply juxtapose rule once.
        - the thrid function applies the sumeq extension.
    '''

    # construct the parser
    if parser is None:
        parser = construct_parser(CScalar, ABase)

    def parse(s: str) -> TRSTerm:
        return parser.parse(s)
    
    # inherit the rules from dirac
    dirac_trs = dirac_construct_trs(CScalar, ABase)
    rules = []

    #####################################################
    # transpose

    KET_TRANS_1 = TRSRule(
        "KET_TRANS_1",
        lhs = parse(r'''TRANK(0B)'''),
        rhs = parse(r'''0K'''),
    )
    rules.append(KET_TRANS_1)

    KET_TRANS_2 = TRSRule(
        "KET_TRANS_2",
        lhs = parse(r'''TRANK(BRA(s))'''),
        rhs = parse(r'''KET(s)'''),
    )
    rules.append(KET_TRANS_2)

    KET_TRANS_3 = TRSRule(
        "KET_TRANS_3",
        lhs = parse(r'''TRANK(ADJB(K0))'''),
        rhs = parse(r'''ADJK(TRANB(K0))''')
    )
    rules.append(KET_TRANS_3)

    KET_TRANS_4 = TRSRule(
        "KET_TRANS_4",
        lhs = parse(r'''TRANK(TRANB(K0))'''),
        rhs = parse(r'''K0'''),
    )
    rules.append(KET_TRANS_4)

    KET_TRANS_5 = TRSRule(
        "KET_TRANS_5",
        lhs = parse(r'''TRANK(S0 SCRB B0)'''),
        rhs = parse(r'''S0 SCRK TRANK(B0)'''),
    )
    rules.append(KET_TRANS_5)

    def ket_trans_6_rewrite(rule, term, side_info):
        if isinstance(term, KetTrans) and isinstance(term.args[0], BraAdd):
                new_args = tuple(KetTrans(arg) for arg in term.args[0].args)
                return KetAdd(*new_args)
    KET_TRANS_6 = TRSRule(
        "KET_TRANS_6",
        lhs = "TRANK(B1 ADDB B2)",
        rhs = "TRANK(B1) ADDK TRANK(B2)",
        rewrite_method=ket_trans_6_rewrite
    )
    rules.append(KET_TRANS_6)

    KET_TRANS_7 = TRSRule(
         "KET_TRANS_7",
         lhs = parse(r'''TRANK(B0 MLTB O0)'''),
         rhs = parse(r'''TRANO(O0) MLTK TRANK(B0)''')
    )
    rules.append(KET_TRANS_7)

    KET_TRANS_8 = TRSRule(
        "KET_TRANS_8",
        lhs = parse(r'''TRANK(B1 TSRB B2)'''),
        rhs = parse(r'''TRANK(B1) TSRK TRANK(B2)''')
    )
    rules.append(KET_TRANS_8)


    BRA_TRANS_1 = TRSRule(
        "BRA_TRANS_1",
        lhs = parse(r'''TRANB(0K)'''),
        rhs = parse(r'''0B'''),
    )
    rules.append(BRA_TRANS_1)

    BRA_TRANS_2 = TRSRule(
        "BRA_TRANS_2",
        lhs = parse(r'''TRANB(KET(s))'''),
        rhs = parse(r'''BRA(s)'''),
    )
    rules.append(BRA_TRANS_2)

    BRA_TRANS_3 = TRSRule(
        "BRA_TRANS_3",
        lhs = parse(r'''TRANB(ADJK(B0))'''),
        rhs = parse(r'''ADJB(TRANK(B0))'''),
    )
    rules.append(BRA_TRANS_3)

    BRA_TRANS_4 = TRSRule(
        "BRA_TRANS_4",
        lhs = parse(r'''TRANB(TRANK(B0))'''),
        rhs = parse(r'''B0'''),
    )
    rules.append(BRA_TRANS_4)

    BRA_TRANS_5 = TRSRule(
        "BRA_TRANS_5",
        lhs = parse(r'''TRANB(S0 SCRK K0)'''),
        rhs = parse(r'''S0 SCRB TRANB(K0)'''),
    )
    rules.append(BRA_TRANS_5)

    def bra_trans_6_rewrite(rule, term, side_info):
        if isinstance(term, BraTrans) and isinstance(term.args[0], KetAdd):
                new_args = tuple(BraTrans(arg) for arg in term.args[0].args)
                return BraAdd(*new_args)
    BRA_TRANS_6 = TRSRule(
        "BRA_TRANS_6",
        lhs = "TRANB(K1 ADDK K2)",
        rhs = "TRANB(K1) ADDB TRANB(K2)",
        rewrite_method=bra_trans_6_rewrite
    )
    rules.append(BRA_TRANS_6)

    BRA_TRANS_7 = TRSRule(
         "BRA_TRANS_7",
         lhs = parse(r'''TRANB(O0 MLTK K0)'''),
         rhs = parse(r'''TRANB(K0) MLTB TRANO(O0)''')
    )
    rules.append(BRA_TRANS_7)

    BRA_TRANS_8 = TRSRule(
        "BRA_TRANS_8",
        lhs = parse(r'''TRANB(K1 TSRK K2)'''),
        rhs = parse(r'''TRANB(K1) TSRB TRANB(K2)''')
    )
    rules.append(BRA_TRANS_8)


    OPT_TRANS_1 = TRSRule(
        "OPT_TRANS_1",
        lhs = parse(r'''TRANO(0O)'''),
        rhs = parse(r'''0O'''),
    )
    rules.append(OPT_TRANS_1)

    OPT_TRANS_2 = TRSRule(
        "OPT_TRANS_2",
        lhs = parse(r'''TRANO(1O)'''),
        rhs = parse(r'''1O'''),
    )
    rules.append(OPT_TRANS_2)

    OPT_TRANS_3 = TRSRule(
        "OPT_TRANS_3",
        lhs = parse(r'''TRANO(K0 OUTER B0)'''),
        rhs = parse(r'''TRANK(B0) OUTER TRANB(K0)''')
    )
    rules.append(OPT_TRANS_3)

    OPT_TRANS_4 = TRSRule(
        "OPT_TRANS_4",
        lhs = parse(r'''TRANO(ADJO(O0))'''),
        rhs = parse(r'''ADJO(TRANO(O0))''')
    )
    rules.append(OPT_TRANS_4)

    OPT_TRANS_5 = TRSRule(
        "OPT_TRANS_5",
        lhs = parse(r'''TRANO(TRANO(O0))'''),
        rhs = parse(r'''O0'''),
    )
    rules.append(OPT_TRANS_5)

    OPT_TRANS_6 = TRSRule(
        "OPT_TRANS_6",
        lhs = parse(r'''TRANO(S0 SCRO O0)'''),
        rhs = parse(r'''S0 SCRO TRANO(O0)'''),
    )
    rules.append(OPT_TRANS_6)

    def opt_trans_7_rewrite(rule, term, side_info):
        if isinstance(term, OpTrans) and isinstance(term.args[0], OpAdd):
                new_args = tuple(OpTrans(arg) for arg in term.args[0].args)
                return OpAdd(*new_args)
    OPT_TRANS_7 = TRSRule(
        "OPT_TRANS_7",
        lhs = "TRANO(O1 ADDO O2)",
        rhs = "TRANO(O1) ADDO TRANO(O2)",
        rewrite_method=opt_trans_7_rewrite
    )
    rules.append(OPT_TRANS_7)

    OPT_TRANS_8 = TRSRule(
         "OPT_TRANS_8",
         lhs = parse(r'''TRANO(O1 MLTO O2)'''),
         rhs = parse(r'''TRANO(O2) MLTO TRANO(O1)''')
    )
    rules.append(OPT_TRANS_8)

    OPT_TRANS_9 = TRSRule(
        "OPT_TRANS_9",
        lhs = parse(r'''TRANO(O1 TSRO O2)'''),
        rhs = parse(r'''TRANO(O1) TSRO TRANO(O2)''')
    )
    rules.append(OPT_TRANS_9)

    #####################################################
    # sum-elim

    def sum_elim_1_rewrite(rule, term, side_info):
        if isinstance(term, Sum) and term.body == CScalar.zero():
            return CScalar.zero()
    SUM_ELIM_1 = TRSRule(
        "SUM_ELIM_1",
        lhs = "SUM(i, C(0))",
        rhs = "C(0)",
        rewrite_method = sum_elim_1_rewrite
    )
    rules.append(SUM_ELIM_1)


    def sum_elim_2_rewrite(rule, term, side_info):
        if isinstance(term, Sum) and isinstance(term.body, (KetZero, BraZero, OpZero)):
            return type(term.body)()
    SUM_ELIM_2 = TRSRule(
        "SUM_ELIM_2",
        lhs = "SUM(i, {0K/0B/0O})",
        rhs = "0O",
        rewrite_method = sum_elim_2_rewrite
    )
    rules.append(SUM_ELIM_2)




    def sum_elim_3_rewrite(rule, term, side_info):
        if isinstance(term, Sum) and isinstance(term.body, ScalarDelta):
            if term.bind_var == term.body.args[0]:
                s = term.body.args[1]
            elif term.bind_var == term.body.args[1]:
                s = term.body.args[0]
            else:
                return None
            
            if term.bind_var.name not in s.free_variables():
                return CScalar.one()
            
            else:
                return None
            
    SUM_ELIM_3 = TRSRule(
        "SUM_ELIM_3",
        lhs = "SUM(i, DELTA(i, s))",
        rhs = "C(1)",
        rewrite_method = sum_elim_3_rewrite
    )
    rules.append(SUM_ELIM_3)

    def sum_elim_4_rewrite(rule, term, side_info):
        if isinstance(term, Sum) and isinstance(term.body, ScalarMlt):
            for i, item in enumerate(term.body.args):
                if isinstance(item, ScalarDelta):
                    if term.bind_var == item.args[0]:
                        s = item.args[1]
                    elif term.bind_var == item.args[1]:
                        s = item.args[0]
                    else:
                        return None
                    
                    if term.bind_var.name not in s.free_variables():
                        sub = Subst({term.bind_var.name : s})
                        return ScalarMlt(*term.body.remained_terms(i)).substitute(sub)
                    
                    else:
                        return None
            
    SUM_ELIM_4 = TRSRule(
        "SUM_ELIM_4",
        lhs = "SUM(i, DELTA(i, s) MLTS S0)",
        rhs = "S0[i:=s]",
        rewrite_method = sum_elim_4_rewrite
    )
    rules.append(SUM_ELIM_4)


    def sum_elim_5_rewrite(rule, term, side_info):
        if isinstance(term, Sum) and isinstance(term.body, (KetScal, BraScal, OpScal)) and isinstance(term.body.args[0], ScalarDelta):
            delta = term.body.args[0]
            if term.bind_var == delta.args[0]:
                s = delta.args[1]
            elif term.bind_var == delta.args[1]:
                s = delta.args[0]
            else:
                return None
            
            if term.bind_var.name not in s.free_variables():
                sub = Subst({term.bind_var.name : s})
                return term.body.args[1].substitute(sub)
            
            else:
                return None
            
    SUM_ELIM_5 = TRSRule(
        "SUM_ELIM_5",
        lhs = "SUM(i, DELTA(i, s) {SCRK/SCRB/SCRO} X)",
        rhs = "X[i:=s]",
        rewrite_method = sum_elim_5_rewrite
    )
    rules.append(SUM_ELIM_5)


    def sum_elim_6_rewrite(rule, term, side_info):
        if isinstance(term, Sum) and isinstance(term.body, (KetScal, BraScal, OpScal)) and isinstance(term.body.args[0], ScalarMlt):
            for i, delta in enumerate(term.body.args[0].args):
                if isinstance(delta, ScalarDelta):
                    if term.bind_var == delta.args[0]:
                        s = delta.args[1]
                    elif term.bind_var == delta.args[1]:
                        s = delta.args[0]
                    else:
                        return None
                    
                    if term.bind_var.name not in s.free_variables():
                        sub = Subst({term.bind_var.name : s})

                        return type(term.body)(ScalarMlt(*term.body.args[0].remained_terms(i)).substitute(sub), term.body.args[1].substitute(sub))
                    
                    else:
                        return None
            
    SUM_ELIM_6 = TRSRule(
        "SUM_ELIM_6",
        lhs = "SUM(i, (DELTA(i, s) MLTS S0) {SCRK/SCRB/SCRO} X)",
        rhs = "S[i:=s] {SCRK/SCRB/SCRO} X[i:=s]",
        rewrite_method = sum_elim_6_rewrite
    )
    rules.append(SUM_ELIM_6)


    def sum_dist_1_rewrite(rule, term, side_info):
        if isinstance(term, ScalarMlt):
            for i, item in enumerate(term.args):
                if isinstance(item, Sum):

                    bind_var, body = item.bind_var, item.body

                    rest_body = ScalarMlt(*term.remained_terms(i))

                    # check whether the bind_var is already used
                    new_body_vars = body.variables() | rest_body.variables()
                    
                    if bind_var.name in new_body_vars:
                        bind_var = TRSVar(var_rename(new_body_vars))
                        body = body.substitute(Subst({item.bind_var.name: bind_var}))

                    return Sum(bind_var, ScalarMlt(body, rest_body))
    SUM_DIST_1 = TRSRule(
        "SUM_DIST_1",
        lhs = "SUM(i, S1) MLTS S2",
        rhs = "SUM(i, S1 MLTS S2)",
        rewrite_method = sum_dist_1_rewrite
    )
    rules.append(SUM_DIST_1)


    def sum_dist_2_rewrite(rule, term, side_info):
        if isinstance(term, ScalarConj) and isinstance(term.args[0], Sum):
            return Sum(term.args[0].bind_var, ScalarConj(term.args[0].body))
    SUM_DIST_2 = TRSRule(
        "SUM_DIST_2",
        lhs = "CONJS(SUM(i, A))",
        rhs = "SUM(i, CONJS(A))",
        rewrite_method = sum_dist_2_rewrite
    )
    rules.append(SUM_DIST_2)



    def sum_dist_3_rewrite(rule, term, side_info):
        if isinstance(term, (KetAdj, BraAdj, OpAdj)) and isinstance(term.args[0], Sum):
            return Sum(term.args[0].bind_var, type(term)(term.args[0].body))
    SUM_DIST_3 = TRSRule(
        "SUM_DIST_3",
        lhs = "{ADJK/ADJB/ADJO}(SUM(i, A))",
        rhs = "SUM(i, {ADJK/ADJB/ADJO}(A))",
        rewrite_method = sum_dist_3_rewrite
    )
    rules.append(SUM_DIST_3)


    def sum_dist_4_rewrite(rule, term, side_info):
        if isinstance(term, (KetTrans, BraTrans, OpTrans)) and isinstance(term.args[0], Sum):
            return Sum(term.args[0].bind_var, type(term)(term.args[0].body))
    SUM_DIST_4 = TRSRule(
        "SUM_DIST_4",
        lhs = "{TRANK/TRANB/TRANO}(SUM(i, A))",
        rhs = "SUM(i, {TRANK/TRANB/TRANO}(A))",
        rewrite_method = sum_dist_4_rewrite
    )
    rules.append(SUM_DIST_4)


    def sum_dist_5_rewrite(rule, term, side_info):
        if isinstance(term, (KetScal, BraScal, OpScal)) and isinstance(term.args[1], Sum):
            return Sum(term.args[1].bind_var, type(term)(term.args[0], term.args[1].body))
    SUM_DIST_5 = TRSRule(
        "SUM_DIST_5",
        lhs = "S0 {SCRK/SCRB/SCRO} SUM(i, X)",
        rhs = "SUM(i, S0 {SCRK/SCRB/SCRO} X)",
        rewrite_method = sum_dist_5_rewrite
    )
    rules.append(SUM_DIST_5)

    def sum_dist_6_rewrite(rule, term, side_info):
        if isinstance(term, (KetScal, BraScal, OpScal)) and isinstance(term.args[0], Sum):
            return Sum(term.args[0].bind_var, type(term)(term.args[0].body, term.args[1]))
    SUM_DIST_6 = TRSRule(
        "SUM_DIRAC_6",
        lhs = "SUM(i, S0) {SCRK/SCRB/SCRO} X",
        rhs = "SUM(i, S0 {SCRK/SCRB/SCRO} X)",
        rewrite_method = sum_dist_6_rewrite
    )
    rules.append(SUM_DIST_6)
    
    #####################################################
    # sum-distribution

    def sum_dist_7_rewrite(rule, term, side_info):
        if isinstance(term, (ScalarDot, KetApply, BraApply, OpApply)) and isinstance(term.args[0], Sum):

            bind_var, body = term.args[0].bind_var, term.args[0].body

            # check whether the bind_var is already used
            new_body_vars = body.variables() | term.args[1].variables()
            if bind_var.name in new_body_vars:
                bind_var = TRSVar(var_rename(new_body_vars))
                body = body.substitute(Subst({term.args[0].bind_var.name: bind_var}))

            return Sum(bind_var, type(term)(body, term.args[1]))
        
    SUM_DIST_7 = TRSRule(
        "SUM_DIST_7",
        lhs = "SUM(x, x1) {DOT/MLTK/MLTB/MLTO} x2",
        rhs = "SUM(x, x1 {DOT/MLTK/MLTB/MLTO} x2)",
        rewrite_method = sum_dist_7_rewrite
    )
    rules.append(SUM_DIST_7)

    def sum_dist_8_rewrite(rule, term, side_info):
        if isinstance(term, (ScalarDot, KetApply, BraApply, OpApply)) and isinstance(term.args[1], Sum):
            bind_var, body = term.args[1].bind_var, term.args[1].body

            # check whether the bind_var is already used
            new_body_vars = body.variables() | term.args[0].variables()
            if bind_var.name in new_body_vars:
                bind_var = TRSVar(var_rename(new_body_vars))
                body = body.substitute(Subst({term.args[1].bind_var.name: bind_var}))

            return Sum(bind_var, type(term)(term.args[0], body))
        
    SUM_DIST_8 = TRSRule(
        "SUM_DIST_8",
        lhs = "x1 {DOT/MLTK/MLTB/MLTO} SUM(x, x2)",
        rhs = "SUM(x, x1 {DOT/MLTK/MLTB/MLTO} x2)",
        rewrite_method = sum_dist_8_rewrite
    )
    rules.append(SUM_DIST_8)


    def sum_dist_9_rewrite(rule, term, side_info):
        if isinstance(term, (KetTensor, BraTensor, OpOuter, OpTensor)) and isinstance(term.args[0], Sum):

            bind_var, body = term.args[0].bind_var, term.args[0].body

            # check whether the bind_var is already used
            new_body_vars = body.variables() | term.args[1].variables()
            if bind_var.name in new_body_vars:
                bind_var = TRSVar(var_rename(new_body_vars))
                body = body.substitute(Subst({term.args[0].bind_var.name: bind_var}))

            return Sum(bind_var, type(term)(body, term.args[1]))
        
    SUM_DIST_9 = TRSRule(
        "SUM_DIST_9",
        lhs = "SUM(x, x1) {TSRK/TSRB/OUTER/TSRO} x2",
        rhs = "SUM(x, x1 {TSRK/TSRB/OUTER/TSRO} x2)",
        rewrite_method = sum_dist_9_rewrite
    )
    rules.append(SUM_DIST_9)


    def sum_dist_10_rewrite(rule, term, side_info):
        if isinstance(term, (KetTensor, BraTensor, OpOuter, OpTensor)) and isinstance(term.args[1], Sum):
            bind_var, body = term.args[1].bind_var, term.args[1].body

            # check whether the bind_var is already used
            new_body_vars = body.variables() | term.args[0].variables()
            if bind_var.name in new_body_vars:
                bind_var = TRSVar(var_rename(new_body_vars))
                body = body.substitute(Subst({term.args[1].bind_var.name: bind_var}))

            return Sum(bind_var, type(term)(term.args[0], body))
        
    SUM_DIST_10 = TRSRule(
        "SUM_DIST_10",
        lhs = "x1 {TSRK/TSRB/OUTER/TSRO} SUM(x, x2)",
        rhs = "SUM(x, x1 {TSRK/TSRB/OUTER/TSRO} x2)",
        rewrite_method = sum_dist_10_rewrite
    )
    rules.append(SUM_DIST_10)

    def sum_add_1_rewrite(rule, term, side_info):
        if isinstance(term, (ScalarAdd, KetAdd, BraAdd, OpAdd)):
            for i, itemA in enumerate(term.args):
                if isinstance(itemA, Sum):
                    for j in range(i+1, len(term.args)):
                        itemB = term.args[j]
                        if isinstance(itemB, Sum):
                            new_bind_var = TRSVar(var_rename(itemA.variables() | itemB.variables()))
                            subA = Subst({
                                itemA.bind_var.name: new_bind_var,
                            })
                            subB = Subst({
                                itemB.bind_var.name: new_bind_var,
                            })
                            return type(term)(
                                Sum(new_bind_var, type(term)(
                                    itemA.body.substitute(subA), 
                                    itemB.body.substitute(subB))),
                                *term.remained_terms(i, j))

    SUM_ADD_1 = TRSRule(
        "SUM_ADD_1",
        lhs = "SUM(i, A) {ADDS/ADDK/ADDB/ADDO} SUM(j, B)",
        rhs = "SUM(k, A[i:=k] {ADDS/ADDK/ADDB/ADDO} B[j:=k])",
        rewrite_method = sum_add_1_rewrite
    )
    rules.append(SUM_ADD_1)


    #####################################################
    # beta-reduction

    def beta_reduction_rewrite(rule, term, side_info):
        if isinstance(term, Apply):
            f, x = term.args
            if isinstance(f, Abstract):
                return f.body.substitute(Subst({f.bind_var.name: x}))
            
    BETA_REDUCTION = TRSRule(
        "BETA_REDUCTION",
        lhs = "APPLY(LAMBDA(x, A), a)",
        rhs = "A[x := a]",
        rewrite_method = beta_reduction_rewrite,
        rule_repr = "(* beta-reduction: APPLY(LAMBDA(x, A), a) -> A[x := a] ;*)",
    )
    rules.append(BETA_REDUCTION)



    #####################################################
    # Juxtapose

    def juxtapose_rewrite(term: TRSTerm) -> TRSTerm:
        if isinstance(term, ScalarDot):
            B, K = term.args[0], term.args[1]
            return Juxtapose(ScalarDot(B, K), ScalarDot(BraTrans(K), KetTrans(B)))
        
        elif isinstance(term, StdTerm):
            return type(term)(*map(juxtapose_rewrite, term.args))
        
        elif isinstance(term, BindVarTerm):
            return type(term)(term.bind_var, juxtapose_rewrite(term.body))
        
        else:
            return term
        
    
    def __construct_sum_term(bind_vars: Tuple[TRSVar, ...], body: TRSTerm) -> TRSTerm:
        if len(bind_vars) == 0:
            return body
        else:
            return Sum(bind_vars[0], __construct_sum_term(bind_vars[1:], body))
    
        
    def sumeq_rewrite(term: TRSTerm) -> TRSTerm:
        if isinstance(term, Sum):

            # get the bind variable and the body
            bind_vars : list[TRSVar] = []
            while isinstance(term, Sum):
                bind_vars.append(term.bind_var)
                term = term.body

            # get all permutations of bind_vars
            perms = itertools.permutations(bind_vars)
            
            # construct the sumeq term
            return SumEq(*[__construct_sum_term(perm, sumeq_rewrite(term)) for perm in perms])

        elif isinstance(term, StdTerm):
            return type(term)(*map(sumeq_rewrite, term.args))
        
        elif isinstance(term, BindVarTerm):
            return type(term)(term.bind_var, sumeq_rewrite(term.body))
        
        else:
            return term

             
        
    # build the trs
    rules = rules + dirac_trs.rules
    return TRS(rules), juxtapose_rewrite, sumeq_rewrite