
from ..dirac.syntax import *

from ..trs import BindVarTerm

class ScalarSum(DiracScalar, BindVarTerm):
    fsymbol_print = "sum"
    fsymbol = "SUMS"

    