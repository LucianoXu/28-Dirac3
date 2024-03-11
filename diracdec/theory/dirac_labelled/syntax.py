from __future__ import annotations

from ..dirac.syntax import *

from ..trs import BindVarTerm, MultiBindTerm, var_rename, var_rename_ls, seq_content_eq

import itertools

class QReg(TRSTerm):
    @staticmethod
    def normalize(A: TRSTerm) -> TRSTerm:
        '''
        Get the REG-normal form.
        '''
        # depth first
        if isinstance(A, QRegFst):
            A = QRegFst(QReg.normalize(A.args[0]))
        elif isinstance(A, QRegSnd):
            A = QRegSnd(QReg.normalize(A.args[0]))
        elif isinstance(A, QRegPair):
            A = QRegPair(QReg.normalize(A.args[0]), QReg.normalize(A.args[1]))
        
        # apply the rules
        if isinstance(A, QRegFst) and isinstance(A.args[0], QRegPair):
            return A.args[0].args[0]
        elif isinstance(A, QRegSnd) and isinstance(A.args[0], QRegPair):
            return A.args[0].args[1]
        elif isinstance(A, QRegPair) and isinstance(A.args[0], QRegFst) and isinstance(A.args[1], QRegSnd) and A.args[0].args[0] == A.args[1].args[0]:
            return A.args[0].args[0]
        
        return A


    @staticmethod
    def is_in(A: TRSTerm, B: TRSTerm) -> bool:
        '''
        Check whether the qreg A is in the qreg B.
        For example, `FSTR(R)` is in `R`, and `SND(FST(R))` is in `FST(R)`.

        This function will automatically calculated the REG-normal form before deciding.
        '''

        A = QReg.normalize(A)
        B = QReg.normalize(B)

        # R is in R
        if A == B:
            return True
        
        # X is in R -> FSTR(X) is in R /\ SNDR(X) is in R
        if isinstance(A, (QRegFst, QRegSnd)):
            return QReg.is_in(A.args[0], B)
        
        # A is in R /\ B is in R -> PAIRR(A, B) is in R
        if isinstance(A, QRegPair):
            return QReg.is_in(A.args[0], B) and QReg.is_in(A.args[1], B)
        
        # X is in R1 \/ X is in R2 -> X is in PAIRR(R1, R2)
        if isinstance(B, QRegPair):
            return QReg.is_in(A, B.args[0]) or QReg.is_in(A, B.args[1])
        
        
        return False
    
    @staticmethod
    def is_disj(A: TRSTerm, B: TRSTerm) -> bool:
        '''
        Check whether the qreg A and B are disjoint
        '''

        A = QReg.normalize(A)
        B = QReg.normalize(B)

        # the algorithm relies on the speical normal form: pairs will not appear inside FSTR or SNDR
        
        if isinstance(A, QRegPair):
            return QReg.is_disj(A.args[0], B) and QReg.is_disj(A.args[1], B)
        
        if isinstance(B, QRegPair):
            return QReg.is_disj(A, B.args[0]) and QReg.is_disj(A, B.args[1])
    
        return not QReg.is_in(A, B) and not QReg.is_in(B, A)



class QRegPair(QReg, StdTerm):
    fsymbol_print = "PAIRR"
    fsymbol = "PAIRR"

    def __init__(self, left: TRSTerm, right: TRSTerm):
        super().__init__(left, right)

    def __str__(self) -> str:
        return str(ParenBlock(HSeqBlock(
            str(self.args[0]), ', ', str(self.args[1]),
            v_align='b')))

    def tex(self) -> str:
        return f"( {self.args[0].tex()} , {self.args[1].tex()} )"
    

class QRegFst(DiracBase, StdTerm):
    fsymbol_print = "fstR"
    fsymbol = "FSTR"

    def __init__(self, p: TRSTerm):
        super().__init__(p)

    def tex(self) -> str:
        return rf" \mathrm{{fst}} {self.args[0].tex()}"
    
class QRegSnd(DiracBase, StdTerm):
    fsymbol_print = "sndR"
    fsymbol = "SNDR"

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