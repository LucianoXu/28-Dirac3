

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


# Build the parser
parser = yacc.yacc()

def parse(s: str) -> Any:
    return parser.parse(s, lexer = lexer)