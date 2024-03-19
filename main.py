# from wolframclient.evaluation import WolframLanguageSession
# from wolframclient.language import wl, wlexpr
# session = WolframLanguageSession()

# print(session.evaluate(wlexpr('Range[5]')))
# session.terminate()

from diracdec import *
from diracdec import parse as parse, dirac_bigop_delta_trs as trs, label_trs

trs = trs + label_trs


if __name__ == "__main__":
    with wolfram_backend.wolfram_session():
        a = parse(r'''{
        ket0 : KET('0');
        bra0 : BRA('0');
        ket1 : KET('1');
        bra1 : BRA('1');
        ketP :  "Sqrt[1/2]" SCR (ket0 ADD ket1) ;
        braP :  "Sqrt[1/2]" SCR (bra0 ADD bra1) ;
        ketM :  "Sqrt[1/2]" SCR (ket0 ADD ("-1" MLTK ket1)) ;
        braM :  "Sqrt[1/2]" SCR (bra0 ADD ("-1" MLTB bra1)) ;

        beta00 :  "Sqrt[1/2]" SCR ((ket0 TSRK ket0) ADD (ket1 TSRK ket1));

        I2 : (ket0 OUTER bra0) ADD (ket1 OUTER bra1);

        Z : (ket0 OUTER bra0) ADD ("-1" SCR (ket1 OUTER bra1));

        X : (ket0 OUTER bra1) ADD (ket1 OUTER bra0);

        Y : ("-I" SCR (ket0 OUTER bra1)) ADD ("I" SCR (ket1 OUTER bra0));


        H :  "Sqrt[1/2]" SCR ((ket0 OUTER bra0) ADD (ket0 OUTER bra1) ADD (ket1 OUTER bra0) ADD ("-1" SCR (ket1 OUTER bra1)));

        CX :  ((ket0 TSRK ket0) OUTER (bra0 TSRB bra0))
                    ADD ((ket0 TSRK ket1) OUTER (bra0 TSRB bra1)) 
                    ADD ((ket1 TSRK ket1) OUTER (bra1 TSRB bra0))
                    ADD ((ket1 TSRK ket0) OUTER (bra1 TSRB bra1));

        CZ :  ((ket0 TSRK ket0) OUTER (bra0 TSRB bra0))
                    ADD ((ket0 TSRK ket1) OUTER (bra0 TSRB bra1)) 
                    ADD ((ket1 TSRK ket0) OUTER (bra1 TSRB bra0))
                    ADD ("-1" SCR ((ket1 TSRK ket1) OUTER (bra1 TSRB bra1)));
        }''')
        a = parse(''' 
(KET(a) OUTER BRA(b)) MLTO (KET(c) OUTER BRA(d))            ''')
        b = parse(''' 
                (
                    (SUM(i, KET(i) OUTER BRA(i))[T]) MLTOL (TP(A)[T])
                ) 
                MLTKL 
                (
                    SUM(i, KET(PAIR(i, i))[PAIRR(S, T)])
                ) 
            ''')
        

        print(trs.normalize(a, verbose=True))
        print(trs.normalize(b))
        print(repr(trs.normalize(a)))
        # print(trs.normalize(b))

