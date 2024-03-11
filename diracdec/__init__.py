
from .backends import wolfram_backend


from .backends import render_tex, render_tex_to_svg

# avoid the block from wolfram session
try:

    from . import backends, components, theory

    
    from .theory import TRSTerm, TRSVar, Subst

    from .factory import parse

    from .factory import dirac_trs, dirac_cime2_file

    from .factory import dirac_delta_trs

    from .factory import dirac_bigop_trs

    from .factory import dirac_bigop_delta_trs, entry_trs

    # transformers
    from .components import wolU
    from .factory import juxt


    # out-of-box interface
    from .factory import normalize, eq_check


except Exception as e:
    raise e

finally:    
    wolfram_backend.session_terminate()
