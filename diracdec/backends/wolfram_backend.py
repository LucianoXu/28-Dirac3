'''
A lightweight wrapping of Wolfram Engine.

providing the unique 'session'.
'''

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

# the only session
session = WolframLanguageSession()

def wolfram_start():
    session.start()

def wolfram_terminate():
    session.terminate()

def wolfram_parser(code : str):
    return session.evaluate(code)