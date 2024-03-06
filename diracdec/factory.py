'''
The script to construct rewriting systems and corresponding parsers with different components
'''

#########################
# prepare the theories (functors)


from .theory.trs import TRSTerm, TRSVar
from .components import wolU

#########################
# build some parser

from .theory import dirac, delta_ext

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

############# with big-op

from .theory import dirac_bigop, delta_ext
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



###############################################
# out-of-box interface

def normalize(s : str) -> dict:
    '''
    The most powerful interface to normalize a term.
    '''
    t = dirac_bigop_delta_parse(s)
    norm_t = dirac_bigop_delta_trs.normalize(t)
    res = {}
    res['norm-term'] = str(norm_t)
    return res

def eq_check(s1: str, s2: str) -> bool:
    '''
    The most powerful interface to check the equality of two terms.
    '''

    t1 = dirac_bigop_delta_parse(s1)
    t2 = dirac_bigop_delta_parse(s2)
    norm_t1 = dirac_bigop_delta_trs.normalize(t1)
    norm_t2 = dirac_bigop_delta_trs.normalize(t2)

    post_proc_t1 = wolU(juxt(sumeq(norm_t1)))
    post_proc_t2 = wolU(juxt(sumeq(norm_t2)))

    return post_proc_t1 == post_proc_t2