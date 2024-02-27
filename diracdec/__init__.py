
from .backends import wolfram_backend

from .backends import render_tex, render_tex_to_svg

# avoid the block from wolfram session
try:

    from . import backends, components, theory

    from .theory import TRSTerm, TRSVar, Subst

    from .factory import dirac_parser, dirac_parse, dirac_trs, dirac_cime2_file

    from .factory import dirac_delta_parser, dirac_delta_parse, dirac_delta_trs

    from .factory import dirac_U_parser, dirac_U_parse, dirac_U_trs

    from .factory import dirac_U_delta_parser, dirac_U_delta_parse, dirac_U_delta_trs

    from .factory import dirac_bigop_parser, dirac_bigop_parse, dirac_bigop_trs, juxt, sumeq

    from .factory import dirac_bigop_delta_parser, dirac_bigop_delta_parse, dirac_bigop_delta_trs

except Exception as e:
    raise e

finally:    
    wolfram_backend.session_terminate()
