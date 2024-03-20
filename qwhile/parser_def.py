
from __future__ import annotations
from typing import Tuple

from .ast import *

from diracdec.parser import parser_def as dirac_syntax_parser


from diracdec.parser.parser_def import p_dirac_add, p_dirac_adj, p_dirac_scal, p_dirac_zero, p_diracbase2, p_diracbase3, p_diracbase4, p_diracbra1, p_diracbra2, p_diracbra3, p_diracket1, p_diracket2, p_diracket3, p_diracop1, p_diracop2, p_diracop3, p_diracop4, p_diracscalar2, p_diracscalar3, p_diracscalar4, p_diracscalar5, p_diracscalar6, p_term, p_term_parentheses, p_trs_item, p_trs_var, p_abstract, p_apply, p_dirac_braL1, p_dirac_braL2, p_dirac_ketL1, p_dirac_ketL2, p_dirac_opL1, p_dirac_opL2, p_dirac_opL3, p_dirac_sum, p_dirac_sums, p_dirac_tp, p_diracnotationL1, p_diracnotationL2, p_diracscalar7, p_qreg1, p_qreg2, p_qreg3, p_qregset1, p_qregset2, p_qregset3, p_qregset4, p_set_eset, p_set_union, p_set_uset, p_sub, p_sub_list, p_term_append

start = "statement"

precedence = (
    ('right', ';'), # sequential composition is right-associated
) + dirac_syntax_parser.precedence


def type_match(p, types: Tuple[str, ...]) -> bool:
    '''
    The method to check whether the sentence match the corresponding types.
    '''
    if len(p) != len(types) + 1:
        return False
    
    for i in range(len(types)):
        if p.slice[i + 1].type != types[i]:
            return False
    return True

def p_statement(p):
    '''
    statement   : ABORT ';'
                | SKIP ';'
                | trs-term ASSIGN0 ';'
                | trs-term ';'
                | statement statement
                | IF trs-term THEN statement ELSE statement END ';'
                | WHILE trs-term DO statement END ';'
    '''

    # abort
    if type_match(p, ("ABORT", ';')):
        p[0] = Abort()

    # skip
    elif type_match(p, ("SKIP", ';')):
        p[0] = Skip()

    # initialization
    elif type_match(p, ("trs-term", "ASSIGN0", ';')):
        p[0] = Init(p[1])

    # unitary
    elif type_match(p, ("trs-term", ';')):
        p[0] = Unitary(p[1])
    
    # sequential composition
    elif type_match(p, ("statement", "statement")):
        p[0] = Seq((p[1], p[2]))

    # if
    elif type_match(p, ("IF", "trs-term", "THEN", "statement", "ELSE", "statement", "END", ';')):
        p[0] = If(p[2], p[4], p[6])

    # while
    elif type_match(p, ("WHILE", "trs-term", "DO", "statement", "END", ';')):
        p[0] = While(p[2], p[4])
       

def p_error(p):
    if p is None:
        raise RuntimeError("Syntax error: unexpected end of file.")
    raise RuntimeError("Syntax error in input: '" + str(p.value) + "'.")