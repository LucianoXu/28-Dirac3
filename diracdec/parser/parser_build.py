
from typing import Type, Any, Callable


#############################################################
# the lexer

import ply.lex as lex

from .lexer_def import *

# Build the lexer
import re
lexer = lex.lex(reflags = re.UNICODE)



#############################################################
# the parser

import ply.yacc as yacc

from .parser_def import *

from ..theory.atomic_base import AtomicBase
from ..theory.complex_scalar import ComplexScalar

def construct_parser(CScalar: Type[ComplexScalar], ABase: Type[AtomicBase]) -> Callable[[str], Any]:

    def p_diracbase1(p):
        '''
        diracbase   : ATOMICBASE_EXPR
        '''
        p[0] = ABase(p[1])

    def p_diracscalar1(p):
        '''
        diracscalar : COMPLEXSCALAR_EXPR
        '''
        p[0] = CScalar(p[1])


    # Build the parser
    parser = yacc.yacc()

    def parse(s: str) -> Any:
        return parser.parse(s, lexer = lexer)


    return parse