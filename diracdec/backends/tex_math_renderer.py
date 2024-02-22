from IPython.core.display import Image
import matplotlib.pyplot as plt
import tempfile

def render_tex(formula: str, filename:str|None = None, dpi=300) -> Image:
    '''
    render the latex math formula and return an Image object
    Notice: there should be no line breaks in the formula, and the formula must not be embraced in $ $
    '''

    formula = "$$ " + formula + " $$"
    
    # Configure Matplotlib to use LaTeX for text rendering
    plt.rcParams['text.usetex'] = True

    # Create a figure with no frame
    fig = plt.figure(figsize=(6, 1))
    fig.text(0, 0, formula, fontsize=24)
    
    if filename is None:

        # Use a temporary file to save the figure
        with tempfile.NamedTemporaryFile(delete=True, suffix=f'.png') as tmpfile:
            fig.savefig(tmpfile.name, dpi=dpi, bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)
            return Image(tmpfile.name)
    
    else:
        # Save the figure as an image
        fig.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        return Image(filename)
    

def render_tex_to_svg(formula: str, filename:str):
    '''
    render the latex math formula to a svg file
    Notice: there should be no line breaks in the formula, and the formula must not be embraced in $ $
    '''

    formula = "$$ " + formula + " $$"
    
    # Configure Matplotlib to use LaTeX for text rendering
    plt.rcParams['text.usetex'] = True

    # Create a figure with no frame
    fig = plt.figure(figsize=(6, 1))
    fig.text(0, 0, formula, fontsize=24)

    # Save the figure as an image
    fig.savefig(filename, format='svg', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)