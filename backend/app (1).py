from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import subprocess
import os
import uuid

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_TEXT_EXTENSIONS = {'txt'}

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename, allowed_extensions):
    """Check if a file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/upload', methods=['POST'])
def upload_files():
    """Endpoint to receive images and LaTeX text file."""
    if 'images' not in request.files or 'textfile' not in request.files:
        return 'Missing files in the request', 400

    images = request.files.getlist('images')
    text_file = request.files['textfile']

    # Create a unique temporary directory
    unique_id = uuid.uuid4().hex
    temp_dir = os.path.join(UPLOAD_FOLDER, unique_id)
    os.makedirs(temp_dir, exist_ok=True)

    # Save images to the temporary directory
    for image in images:
        if image.filename == '':
            continue  # Skip empty filenames
        if image and allowed_file(image.filename, ALLOWED_IMAGE_EXTENSIONS):
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(temp_dir, image_filename)
            image.save(image_path)
        else:
            return f'Invalid image file type: {image.filename}', 400

    # Save the LaTeX code to a file in the temporary directory
    if text_file.filename == '':
        return 'No selected text file', 400
    if text_file and allowed_file(text_file.filename, ALLOWED_TEXT_EXTENSIONS):
        text_filename = secure_filename(text_file.filename)
        latex_file_path = os.path.join(temp_dir, text_filename)
        text_file.save(latex_file_path)
    else:
        return 'Invalid text file type', 400

    # Change current working directory to the temp directory
    original_cwd = os.getcwd()
    os.chdir(temp_dir)

    # Compile the LaTeX code
    pdf_data = compile_latex_to_pdf(text_filename)

    # Change back to the original working directory
    os.chdir(original_cwd)

    # Clean up the temporary directory
    import shutil
    # shutil.rmtree(temp_dir)

    if pdf_data is not None:
        # Return the PDF data as a response
        response = Response(pdf_data, mimetype='application/pdf')
        response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response
    else:
        return 'Error processing LaTeX file', 500

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

if __name__ == '__main__':
    app.run(debug=True)
