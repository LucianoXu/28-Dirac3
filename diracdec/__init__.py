
from .backends import wolfram_backend

# avoid the block from wolfram session
try:

    from . import backends, components, theory

    from .factory import dirac_parser, dirac_parse, dirac_trs, dirac_cime2_file

    from .factory import dirac_delta_parser, dirac_delta_parse, dirac_delta_trs

except Exception as e:
    raise e

finally:    
    wolfram_backend.session_terminate()
