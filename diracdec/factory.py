'''
The script to construct rewriting systems and corresponding parsers with different components
'''

#########################
# prepare the theories (functors)

from .theory import dirac, delta_ext

from .theory.trs import TRSTerm, TRSVar

#########################
# build some parser


### ALL WOLFRAM BACKEND

from .components import wolfram_abase, wolfram_cscalar

dirac_parser = dirac.construct_parser(wolfram_cscalar.WolframCScalar, wolfram_abase.WolframABase)

def dirac_parse(s: str) -> TRSTerm:
    return dirac_parser.parse(s)

dirac_trs = dirac.construct_trs(
    wolfram_cscalar.WolframCScalar, 
    wolfram_abase.WolframABase, 
    dirac_parser
    )

def dirac_cime2_file(path: str):
    dirac.dirac_cime2_file(dirac_trs, path)
    
### with delta extensions

dirac_delta_parser = dirac_parser

def dirac_delta_parse(s: str) -> TRSTerm:
    return dirac_delta_parser.parse(s)

dirac_delta_trs = delta_ext.modify_trs(
    dirac_trs, 
    wolfram_cscalar.WolframCScalar, 
    wolfram_abase.WolframABase
    )
