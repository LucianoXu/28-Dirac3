
from typing import Any

from diracdec.components import wolfram_simple
from .parser_build import construct_parser


parser = construct_parser(
    wolfram_simple.WolframCScalar,
    wolfram_simple.WolframABase)

def parse(s: str) -> Any:
    return parser.parse(s)
