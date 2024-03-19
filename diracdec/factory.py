'''
The script to construct rewriting systems and corresponding parsers with different components
'''

#########################
# prepare the theories (functors)


from typing import Any
from .theory.trs import Term, Var, Subst
from .components import wolU

#########################
# build some parser

from .theory import dirac, delta_ext
from .components import wolfram_simple
from .theory.parser import construct_parser

parser = construct_parser(
    wolfram_simple.WolframCScalar,
    wolfram_simple.WolframABase)

def parse(s: str) -> Any:
    return parser.parse(s)

### ALL WOLFRAM BACKEND


dirac_trs = dirac.construct_trs(
    wolfram_simple.WolframCScalar,
    wolfram_simple.WolframABase, 
    parser
    )

def dirac_cime2_file(path: str):
    dirac.dirac_cime2_file(dirac_trs, path)
    
### with delta extensions

dirac_delta_trs = delta_ext.modify_trs(
    dirac_trs, 
    wolfram_simple.WolframCScalar,
    wolfram_simple.WolframABase
    )

############# with big-op

from .theory import dirac_bigop, delta_ext
from .components import wolfram_simple

dirac_bigop_trs, juxt = dirac_bigop.construct_trs(
    wolfram_simple.WolframCScalar, 
    wolfram_simple.WolframABase, 
    parser
    )
    
### with delta extensions

dirac_bigop_delta_trs = delta_ext.modify_trs(
    dirac_bigop_trs, 
    wolfram_simple.WolframCScalar, 
    wolfram_simple.WolframABase
    )

entry_trs = dirac_bigop.construct_entry_trs(
    wolfram_simple.WolframCScalar, 
    wolfram_simple.WolframABase, 
    parser
)

###############################################
# TRS for labels

from .theory import dirac_labelled
label_trs = dirac_labelled.construct_trs(
    wolfram_simple.WolframCScalar, 
    wolfram_simple.WolframABase, 
    parser
)

###############################################
# out-of-box interface

def normalize(s : str) -> dict:
    '''
    The most powerful interface to normalize a term.
    '''
    t = parse(s)
    norm_t = dirac_bigop_delta_trs.normalize(t)
    res = {}
    res['norm-term'] = str(norm_t)
    return res

def eq_check(s1: str, s2: str) -> bool:
    '''
    The most powerful interface to check the equality of two terms.
    '''

    t1 = parse(s1)
    t2 = parse(s2)
    norm_t1 = dirac_bigop_delta_trs.normalize(t1)
    norm_t2 = dirac_bigop_delta_trs.normalize(t2)

    post_proc_t1 = wolU(juxt(norm_t1))
    post_proc_t2 = wolU(juxt(norm_t2))

    return post_proc_t1 == post_proc_t2