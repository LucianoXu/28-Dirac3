# from wolframclient.evaluation import WolframLanguageSession
# from wolframclient.language import wl, wlexpr
# session = WolframLanguageSession()

# print(session.evaluate(wlexpr('Range[5]')))
# session.terminate()

from diracdec import *

if __name__ == "__main__":
    try:
        print(parse(''' snd((fst(("1.1", _b_)) , 'ss')) ''' ))
        a = parse(''' 'ss + ss' ''')
        b = parse(''' '2 ss' ''')
        print(a == b)
        print(hash(a))
        print(hash(b))

    finally:
        wolfram_backend.wolfram_terminate()