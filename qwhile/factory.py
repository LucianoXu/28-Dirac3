
from typing import Any

from diracdec.components import wolfram_simple
from .parser import construct_parser


parse = construct_parser(
    wolfram_simple.WolframCScalar,
    wolfram_simple.WolframABase)


########################################
# build the term rewriting system

from . import forward

forward_trs = forward.construct_trs(parse)
