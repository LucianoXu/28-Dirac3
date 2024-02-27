'''
The script to construct rewriting systems and corresponding parsers with different components
'''

#########################
# prepare the theories (functors)

from .theory import dirac, delta_ext, dirac_bigop

from .theory.trs import TRSTerm, TRSVar

#########################
# build some parser


### ALL WOLFRAM BACKEND

from .components import wolfram_simple

dirac_parser = dirac.construct_parser(
    wolfram_simple.WolframCScalar,
    wolfram_simple.WolframABase)

def dirac_parse(s: str) -> TRSTerm:
    return dirac_parser.parse(s)

dirac_trs = dirac.construct_trs(
    wolfram_simple.WolframCScalar,
    wolfram_simple.WolframABase, 
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
    wolfram_simple.WolframCScalar,
    wolfram_simple.WolframABase
    )

#############################################
# wolfram_unique backend

from .components import wolfram_unique

dirac_U_parser = dirac.construct_parser(
    wolfram_unique.WolCScalarUnique,
    wolfram_unique.WolABaseUnique)

def dirac_U_parse(s: str) -> TRSTerm:
    return dirac_parser.parse(s)

dirac_U_trs = dirac.construct_trs(
    wolfram_unique.WolCScalarUnique,
    wolfram_unique.WolABaseUnique, 
    dirac_U_parser
    )
    
### with delta extensions

dirac_U_delta_parser = dirac_U_parser

def dirac_U_delta_parse(s: str) -> TRSTerm:
    return dirac_U_delta_parser.parse(s)

dirac_U_delta_trs = delta_ext.modify_trs(
    dirac_U_trs, 
    wolfram_unique.WolCScalarUnique,
    wolfram_unique.WolABaseUnique, 
    )



############# with big-op

from .components import wolfram_simple

dirac_bigop_parser = dirac_bigop.construct_parser(wolfram_simple.WolframCScalar, wolfram_simple.WolframABase)

def dirac_bigop_parse(s: str) -> TRSTerm:
    return dirac_bigop_parser.parse(s)

dirac_bigop_trs, juxt, sumeq = dirac_bigop.construct_trs(
    wolfram_simple.WolframCScalar, 
    wolfram_simple.WolframABase, 
    dirac_bigop_parser
    )
    
### with delta extensions

dirac_bigop_delta_parser = dirac_bigop_parser

def dirac_bigop_delta_parse(s: str) -> TRSTerm:
    return dirac_bigop_delta_parser.parse(s)

dirac_bigop_delta_trs = delta_ext.modify_trs(
    dirac_bigop_trs, 
    wolfram_simple.WolframCScalar, 
    wolfram_simple.WolframABase
    )