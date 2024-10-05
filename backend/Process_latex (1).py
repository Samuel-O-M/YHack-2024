import subprocess
import os

def compile_latex_to_pdf(latex_code):
    """Compile LaTeX code to PDF and return the PDF data."""
    try:
        # Write the LaTeX code to a temporary file
        temp_tex_filename = 'temp.tex'
        with open(temp_tex_filename, 'w', encoding='utf-8') as f:
            f.write(latex_code)

        # Run pdflatex to generate PDF
        subprocess.run(['pdflatex', '-interaction=nonstopmode', temp_tex_filename],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Read the generated PDF into memory
        with open('temp.pdf', 'rb') as f:
            pdf_data = f.read()

        # Clean up temporary files
        for ext in ['tex', 'pdf', 'log', 'aux']:
            os.remove(f'temp.{ext}')

        return pdf_data
    except subprocess.CalledProcessError:
        # Clean up even if there's an error
        for ext in ['tex', 'pdf', 'log', 'aux']:
            if os.path.exists(f'temp.{ext}'):
                os.remove(f'temp.{ext}')
        return None
