from __future__ import annotations

from ..dirac.syntax import *

from ..trs import BindVarTerm, MultiBindTerm, var_rename, var_rename_ls, seq_content_eq

import itertools

class QReg(TRSTerm):
    ...


class QRegPair(QReg, StdTerm):
    fsymbol_print = "RPAIR"
    fsymbol = "RPAIR"

    def __init__(self, left: TRSTerm, right: TRSTerm):
        super().__init__(left, right)

    def __str__(self) -> str:
        return str(ParenBlock(HSeqBlock(
            str(self.args[0]), ', ', str(self.args[1]),
            v_align='b')))

    def tex(self) -> str:
        return f"( {self.args[0].tex()} , {self.args[1].tex()} )"
    

class QRegFst(DiracBase, StdTerm):
    fsymbol_print = "rfst"
    fsymbol = "RFST"

    def __init__(self, p: TRSTerm):
        super().__init__(p)

    def tex(self) -> str:
        return rf" \mathrm{{fst}} {self.args[0].tex()}"
    
class QRegSnd(DiracBase, StdTerm):
    fsymbol_print = "rsnd"
    fsymbol = "RSND"

    def __init__(self, p: TRSTerm):
        super().__init__(p)

    def tex(self) -> str:
        return rf" \mathrm{{snd}} {self.args[0].tex()}"


#######################################################
# QRegSet: this part will not go into parsing

class QRegSet(TRSTerm):
    ...


class EmptyRSet(QRegSet, StdTerm):
    fsymbol_print = "∅"
    fsymbol = "ESETR"

    def __str__(self) -> str:
        return "∅"
    
    def __repr__(self) -> str:
        return "ESETR"
    
    def tex(self) -> str:
        return r" \emptyset"
    
class RegRSet(QRegSet, StdTerm):
    fsymbol_print = "SETR"
    fsymbol = "SETR"

    def __init__(self, qreg : TRSTerm):
        super().__init__(qreg)

    def __str__(self) -> str:
        return str(HSeqBlock("{", str(self.args[0]), "}"))
    
    def tex(self) -> str:
        return r" \{ " + self.args[0].tex() + r" \}"

class UnionRSet(QRegSet, TRS_AC):
    fsymbol_print = "∪"
    fsymbol = "UNIONR"

    def __init__(self, *tup : TRSTerm):
        TRS_AC.__init__(self, *tup)


    def tex(self) -> str:
        return "( " + " \\cup ".join([s.tex() for s in self.args]) + " )"
    
class SubRSet(QRegSet, TRSInfixBinary):
    fsymbol_print = "\\"
    fsymbol = "SUBR"

    def tex(self) -> str:
        return r" \left ( " + self.args[0].tex() + r" \setminus " + self.args[1].tex() + r" \right )"