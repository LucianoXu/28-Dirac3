'''
The script to construct rewriting systems and corresponding parsers with different components
'''

#########################
# prepare the theories (functors)

from .theory import dirac

from .theory.trs import TRSTerm, TRSVar

#########################
# build some parser


### ALL WOLFRAM BACKEND

from .components import wolfram_abase, wolfram_cscalar

dirac_parser = dirac.construct_parser(wolfram_cscalar.WolframCScalar, wolfram_abase.WolframABase)

def dirac_parse(s: str) -> TRSTerm:
    return dirac_parser.parse(s)

dirac_trs = dirac.construct_trs(wolfram_cscalar.WolframCScalar, wolfram_abase.WolframABase)
    
###