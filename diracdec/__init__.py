
from .backends import wolfram_backend

# avoid the block from wolfram session
try:

    from . import backends, components, theory

    from .factory import dirac_parser, dirac_parse, dirac_trs

except Exception as e:
    raise e

finally:    
    wolfram_backend.session_terminate()
