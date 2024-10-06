import subprocess
import os

def compile_latex_to_pdf(latex_filename):
    """Compile LaTeX file to PDF and return the PDF data."""
    try:
        # Run pdflatex to generate PDF
        subprocess.run(['pdflatex', '-interaction=nonstopmode', latex_filename],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # The output PDF will have the same name but with .pdf extension
        pdf_filename = os.path.splitext(latex_filename)[0] + '.pdf'

        # Read the generated PDF into memory
        with open(pdf_filename, 'rb') as f:
            pdf_data = f.read()

        # Clean up auxiliary files
        for ext in ['aux', 'log', 'out', 'tex']:
            temp_file = os.path.splitext(latex_filename)[0] + f'.{ext}'
            if os.path.exists(temp_file):
                os.remove(temp_file)

        return pdf_data
    except subprocess.CalledProcessError as e:
        # Clean up even if there's an error
        for ext in ['aux', 'log', 'out', 'pdf', 'tex']:
            temp_file = os.path.splitext(latex_filename)[0] + f'.{ext}'
            if os.path.exists(temp_file):
                os.remove(temp_file)
        print(f'LaTeX compilation error: {e}')
        return None
