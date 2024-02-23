'''
A lightweight wrapping of Wolfram Engine.

providing the unique 'session'.
'''

from typing import Sequence

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
from wolframclient.language.expression import WLFunction, WLSymbol
import contextlib

# the only session
session = WolframLanguageSession()

def session_start():
    session.start()

def session_terminate():
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