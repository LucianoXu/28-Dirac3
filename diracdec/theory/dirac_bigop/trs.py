

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
    rules = dirac_trs.rules.copy()

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
        
        else:
            return term
        
    
    def __construct_sum_term(bind_vars: Tuple[TRSVar, ...], body: TRSTerm) -> TRSTerm:
        if len(bind_vars) == 0:
            return body
        else:
            return ScalarSum(bind_vars[0], __construct_sum_term(bind_vars[1:], body))
    
        
    def sumeq_rewrite(term: TRSTerm) -> TRSTerm:
        if isinstance(term, ScalarSum):

            # get the bind variable and the body
            bind_vars : list[TRSVar] = []
            while isinstance(term, ScalarSum):
                bind_vars.append(term.bind_var)
                term = term.body

            # get all permutations of bind_vars
            perms = itertools.permutations(bind_vars)
            
            # construct the sumeq term
            return SumEq(*[__construct_sum_term(perm, term) for perm in perms])

        elif isinstance(term, StdTerm):
            return type(term)(*map(sumeq_rewrite, term.args))
        
        else:
            return term

             
        
    # build the trs
    return TRS(rules), juxtapose_rewrite, sumeq_rewrite