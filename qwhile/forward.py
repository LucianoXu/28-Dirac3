from diracdec.theory.trs import *
from ply import yacc
from .lang import *

class Cfg(StdTerm):
    '''
    A qwhile program-state configuration.
    '''
    fsymbol_print = 'cfg'
    fsymbol = 'cfg'

    def __init__(self, prog: Term, stt: Term):
        super().__init__(prog, stt)
        self.prog = prog
        self.stt = stt

    def __str__(self) -> str:
        return str(HSeqBlock(
            '< ', str(self.prog), ' , ', str(self.stt), ' >',
            v_align='c'
        ))
    
    def tex(self) -> str:
        raise NotImplementedError()
    

class Halt(StdTerm):
    '''
    The halting state for configuration.
    '''
    fsymbol_print = 'Halt'
    fsymbol = 'Halt'

    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Halt"

    def tex(self) -> str:
        raise NotImplementedError()


class CfgSet(AC):
    '''
    The symbol to represent a multiset of configurations
    '''
    fsymbol_print = 'cfg-union'
    fsymbol = 'cfg-union'

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)

    def __str__(self) -> str:

        content = [str(self.args[0])]
        for item in self.args[1:]:
            content.append(", ")
            content.append(str(item))

        return str(HSeqBlock(
            '{| ', 
            *content,
            ' |}',
            v_align='c'
        ))
    
    def tex(self) -> str:
        raise NotImplementedError()


def construct_trs(
        parser: yacc.LRParser) -> TRS:
    
    def parse(s: str) -> Term:
        return parser.parse(s)
    
    # inherit the rules from dirac
    rules = []


    OP_SEM_ABORT = CanonicalRule(
        'OP-SEM-ABORT',
        lhs = parse(''' < abort; , rho > '''),
        rhs = parse(''' < HALT , 0X > ''')
    )
    rules.append(OP_SEM_ABORT)

    OP_SEM_SKIP = CanonicalRule(
        'OP-SEM-SKIP',
        lhs = parse(''' < skip; , rho > '''),
        rhs = parse(''' < HALT , rho > ''')
    )
    rules.append(OP_SEM_SKIP)

    def get_zero_basis(q: Any):
        '''
        get the corresponding basis according to the qreg q
        TODO: refine the implementation by typing
        '''
        if isinstance(q, QRegPair):
            return BasePair(get_zero_basis(q.args[0]), get_zero_basis(q.args[1]))
        else:
            return parse(''' '0' ''')

    def op_sem_init_rewrite(rule, trs, term):
        if isinstance(term, Cfg) and isinstance(term.args[0], Init):
            zero_base = get_zero_basis(term.args[0].qvar)
            bind_v = new_var(term.args[0].variables())
            return Cfg(
                Halt(),
                Sum(
                    ((bind_v, UniversalSet()),), 
                    OpApplyL(
                        OpApplyL(
                            Labelled1(OpOuter(KetBase(zero_base), BraBase(bind_v)), term.args[0].qvar),
                            term.args[1]
                        ),
                        Labelled1(OpOuter(KetBase(bind_v), BraBase(zero_base)), term.args[0].qvar)
                        )
                )
            )

    OP_SEM_INIT = Rule(
        'OP-SEM-INIT',
        lhs = ''' < q:=0; , rho > ''',
        rhs = ''' < HALT, SUM(i, |0><i| rho |i><0| > ''',
        rewrite_method = op_sem_init_rewrite
    )
    rules.append(OP_SEM_INIT)

    OP_SEM_UNITARY = CanonicalRule(
        'OP-SEM-UNITARY',
        lhs = parse(''' < U; , rho > '''),
        rhs = parse(''' < HALT , U MLTOL rho MLTOL ADJ(U) > ''')
    )
    rules.append(OP_SEM_UNITARY)

    OP_SEM_IF = CanonicalRule(
        'OP-SEM-IF',
        lhs = parse(''' < if P then s1 else s2 end; , rho > '''),
        rhs = CfgSet(
            parse(''' < s1 , P MLTOL rho MLTOL P > '''),
            parse(''' < s2 , (1O ADD ("-1" SCR P)) MLTOL rho MLTOL (1O ADD ("-1" SCR P)) > '''))
    )
    rules.append(OP_SEM_IF)

    def op_sem_while_rewrite(rule, trs, term):
        if isinstance(term, Cfg) and isinstance(term.args[0], While):
            if term.args[0].step > 0:
                return Cfg(
                        If(
                            term.args[0].args[0],
                            Seq(
                                term.args[0].S,
                                While(
                                    term.args[0].P, 
                                    term.args[0].step-1, 
                                    term.args[0].S)
                            ),
                            Skip()
                        ),
                        term.args[1]
                    )
            else:
                return Cfg(
                    Abort(),
                    term.args[1]
                )

    OP_SEM_WHILE = Rule(
        'OP-SEM-WHILE',
        lhs = ''' < while [n] P do s end; , rho > ''',
        rhs = ''' < if P then (s; while [n-1] P do s end;) else skip; end; , rho > ''',
        rewrite_method = op_sem_while_rewrite
    )
    rules.append(OP_SEM_WHILE)

    head_rules : List[Rule] = [
        OP_SEM_ABORT,
        OP_SEM_SKIP,
        OP_SEM_INIT,
        OP_SEM_UNITARY,
        OP_SEM_IF,
        OP_SEM_WHILE
    ]

    def op_sem_seq_rewrite(rule, trs, term):
        if isinstance(term, Cfg) and isinstance(term.args[0], Seq):
            for head_rule in head_rules:
                head_res = head_rule.rewrite_method(
                    head_rule, trs, 
                    Cfg(term.args[0].S0, term.args[1]))
                
                cfg_ls = []
                if isinstance(head_res, Cfg):
                    cfg_ls.append(head_res)
                elif isinstance(head_res, CfgSet):
                    for cfg in head_res.args:
                        cfg_ls.append(cfg)

                if len(cfg_ls) > 0:
                    res_ls = []
                    for cfg in cfg_ls:
                        if isinstance(cfg.args[0], Halt):
                            res_ls.append(Cfg(term.args[0].S1, cfg.args[1]))
                        else:
                            res_ls.append(Cfg(cfg.args[0] @ term.args[0].S1, cfg.args[1]))

                    return CfgSet(*res_ls)

    OP_SEM_SEQ = Rule(
        'OP-SEM-SEQ',
        lhs = ''' < S0 S1 , rho > (< S0 , rho > -> <S0' , rho'>)''',
        rhs = ''' < S0' S1, rho' > ''',
        rewrite_method = op_sem_seq_rewrite
    )
    rules.append(OP_SEM_SEQ)


    OP_SEM_ADD = CanonicalRule(
        'OP-SEM-ADD',
        lhs = CfgSet(parse(''' < HALT , rho1 > '''), parse(''' < HALT ,rho2 > ''')),
        rhs = parse(''' < HALT , rho1 ADD rho2 > ''')
    )
    rules.append(OP_SEM_ADD)
    

    # build the trs
    rules = rules + rules
    return TRS(rules)
