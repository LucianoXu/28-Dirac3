
from .backends import wolfram_backend

# avoid the block from wolfram session
try:

    from . import components

    from .theory import *

    from .parser import parse

    from .dirac_trs import diractrs

except Exception as e:
    raise e

finally:    
    wolfram_backend.session_terminate()
