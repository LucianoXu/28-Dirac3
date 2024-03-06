import io
from flask import Flask, request, render_template

from diracdec import *
from diracdec import dirac_bigop_delta_parse as parse, dirac_bigop_delta_trs as trs, juxt, sumeq, wolU
import signal

app = Flask(__name__)

default_subst = '''{
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
        }'''

default_termA = '''
(
    (
        SUM(i, KET(i) OUTER BRA(i)) TSRO 1O
    ) 
    MLTO (A TSRO 1O)
) 
MLTK (SUM(i, KET(PAIR(i, i)))) 
'''
default_termB = '''
(
    (1O TSRO SUM(i, KET(i) OUTER BRA(i))) MLTO (1O TSRO TP(A))
) 
MLTK 
(SUM(i, KET(PAIR(i, i)))) 
'''

@app.route('/')
def home():
    return render_template('index.html',
                           subst = default_subst,
                           termA=default_termA,
                           termB=default_termB,
                           eqres='TO BE CHECKED')


@app.route('/calculate', methods=['POST'])
def calculate():


    # obtain all inputs
    subst_code = request.form.get('sub-code')
    termA_code = request.form.get('termA-code')
    termB_code = request.form.get('termB-code')

    # get substitution
    assert subst_code is not None
    try:
        sub = parse(subst_code)
        sub_parsed = str(sub)
        sub_idempotent = sub.get_idempotent()
    except Exception as e:
        sub_parsed = str(e)

    

    assert termA_code is not None and termB_code is not None

    # normalize term A
    proofA_stream = io.StringIO()

    try:
        termA = parse(termA_code).substitute(sub_idempotent)
        norm_termA = wolU(trs.normalize(juxt(sumeq(trs.normalize(termA, verbose=True, stream=proofA_stream)))))
        norm_termA_text = str(norm_termA)

    except Exception as e:
        norm_termA = None
        norm_termA_text = "Error: " + str(e)


    # normalize term B
    proofB_stream = io.StringIO()

    try:
        termB = parse(termB_code).substitute(sub_idempotent)
        norm_termB = wolU(trs.normalize(juxt(sumeq(trs.normalize(termB, verbose=True, stream=proofB_stream)))))
        norm_termB_text = str(norm_termB)
    
    except Exception as e:
        norm_termB = None
        norm_termB_text = "Error: " + str(e)

    
    if norm_termA is not None and norm_termB is not None:
        if norm_termA == norm_termB:
            compare_result = "CHECKED"
        else:
            compare_result = "NOT SURE"
    else:
        compare_result = "TO BE CHECKED"

    proofA_stream.seek(0)
    proofB_stream.seek(0)    

    # Return the result to the template
    return render_template('index.html',
                           subst = subst_code,
                           subst_parsed = sub_parsed,
                           termA=termA_code,
                           termB=termB_code,
                           termAstr = str(termA),
                           termBstr = str(termB),
                           normA=norm_termA_text,
                           normB=norm_termB_text,
                           proofA = proofA_stream.read(),
                           proofB = proofB_stream.read(),
                           eqres = compare_result)

if __name__ == '__main__':
    app.run(debug=True)