'''
A lightweight wrapping of Wolfram Engine.

providing the unique 'session'.
'''

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
import contextlib

# the only session
session = WolframLanguageSession()

def wolfram_start():
    session.start()

def wolfram_terminate():
    session.terminate()

def wolfram_parser(code : str):
    return session.evaluate(code)


@contextlib.contextmanager
def wolfram_session():
    try:
        session.start()
        yield session
    finally:
        session.terminate()