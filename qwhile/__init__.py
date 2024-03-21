from diracdec.backends import wolfram_backend

try:

    from .lang import *

    from .factory import parser, parse

    from .factory import forward_trs

except Exception as e:
    raise e

finally:    
    wolfram_backend.session_terminate()
