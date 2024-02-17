# from wolframclient.evaluation import WolframLanguageSession
# from wolframclient.language import wl, wlexpr
# session = WolframLanguageSession()

# print(session.evaluate(wlexpr('Range[5]')))
# session.terminate()

from diracdec import *

if __name__ == "__main__":
    with wolfram_backend.wolfram_session():
        pass