'''
The architecture of the term rewriting system
'''

from __future__ import annotations
from typing import Tuple, Any

import hashlib

class TRSTerm:
    fsymbol_print : str
    fsymbol : str

    def __init__(self, *args: Any):
        self.args = args

    def __str__(self) -> str:
        return f'{self.fsymbol_print}({", ".join(map(str, self.args))})'

    def __repr__(self) -> str:
        '''
        It is required that equivalence of the repr of two terms is equivalent to that of the terms.
        '''
        return f'{self.fsymbol}({", ".join(map(repr, self.args))})'

    def __eq__(self, other: TRSTerm) -> bool:
        '''
        This method calculates the equivalence in pure syntactic level.
        '''
        return isinstance(other, type(self)) and self.args == other.args
    
    def __lt__(self, other: TRSTerm) -> bool:
        h_self = hash(self)
        h_other = hash(other)
        if h_self == h_other:
            return repr(self) < repr(other)
        else:
            return h_self < h_other

    
    
    def __hash__(self) -> int:
        h = hashlib.md5(self.fsymbol.encode())
        for arg in self.args:
            h.update(hash(arg).to_bytes(16, 'big'))

        return int(h.hexdigest(), 16)
        

class TRSVar(TRSTerm):

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name
    
    def __eq__(self, other: TRSVar) -> bool:
        return isinstance(other, TRSVar) and self.name == other.name
    
    def __hash__(self) -> int:
        h = hashlib.md5(("var" + self.name).encode())
        return int(h.hexdigest(), 16)
    
class TRSInfixBinary(TRSTerm):
    def __init__(self, L : TRSTerm, R : TRSTerm):
        super().__init__(L, R)

    def __str__(self) -> str:
        return f'({str(self.args[0])} {self.fsymbol_print} {str(self.args[1])})'

    def __repr__(self) -> str:
        return f'({repr(self.args[0])} {self.fsymbol} {repr(self.args[1])})'
    
class TRSCommBinary(TRSTerm):
    '''
    (not infix)
    '''
    def __init__(self, L : Any, R : Any):
        if L > R:
            L, R = R, L
        super().__init__(L, R)

    def __str__(self) -> str:
        return f'{self.fsymbol_print}({str(self.args[0])}, {str(self.args[1])})'

    def __repr__(self) -> str:
        return f'{self.fsymbol}({repr(self.args[0])}, {repr(self.args[1])})'
    
class TRS_AC(TRSTerm):
    def __init__(self, tup: Tuple):
        '''
        The method of flatten the tuple of arguments for the ac_symbol.
        Assume that the items in tup are already flattened.
        '''
        if len(tup) < 2:
            raise ValueError("The tuple lengh should be at least 2.")

        new_ls = []
        for item in tup:
            if isinstance(item, type(self)):
                new_ls.extend(item.args)
            else:
                new_ls.append(item)

        self.args = tuple(sorted(new_ls))

    def __str__(self) -> str:
        return f'({f" {self.fsymbol_print} ".join(map(str, self.args))})'
    
    def __repr__(self) -> str:
        return f'({f" {self.fsymbol} ".join(map(repr, self.args))})'
