from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image
import io
import subprocess
import os
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png'}
ALLOWED_TEXT_EXTENSIONS = {'txt'}

def allowed_file(filename, allowed_extensions):
    """Check if a file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/upload-images', methods=['POST'])
def upload_images():
    """Endpoint to receive and process image files."""
    if 'images' not in request.files:
        return 'No images part in the request', 400

    images = request.files.getlist('images')
    image_data_list = []  # List to store image data in memory

    for image in images:
        if image.filename == '':
            return 'No selected file', 400
        if image and allowed_file(image.filename, ALLOWED_IMAGE_EXTENSIONS):
            # Read image data into memory
            image_data = image.read()
            image_filename = secure_filename(image.filename)
            image_data_list.append({
                'filename': image_filename,
                'data': image_data
            })
        else:
            return 'Invalid file type', 400

    # Example processing: Convert images to a different format or resize
    processed_images = []
    for img in image_data_list:
        image = Image.open(io.BytesIO(img['data']))
        # Example: Convert image to grayscale
        grayscale_image = image.convert('L')
        # Save processed image to bytes buffer
        buf = io.BytesIO()
        grayscale_image.save(buf, format='PNG')
        processed_images.append({
            'filename': img['filename'],
            'data': buf.getvalue()
        })

    # Return a success message
    return 'Images successfully received and processed in memory', 200

@app.route('/upload-text', methods=['POST'])
def upload_text():
    """Endpoint to receive and process LaTeX text files."""
    if 'textfile' not in request.files:
        return 'No textfile part in the request', 400

    text_file = request.files['textfile']

    if text_file.filename == '':
        return 'No selected file', 400

    if text_file and allowed_file(text_file.filename, ALLOWED_TEXT_EXTENSIONS):
        # Read text file data into memory
        text_data = text_file.read().decode('utf-8')  # Assuming UTF-8 encoding
        text_filename = secure_filename(text_file.filename)

        # Process the LaTeX code (optional)
        # For example, compile it to PDF and return the PDF data
        pdf_data = compile_latex_to_pdf(text_data)

        if pdf_data is not None:
            # Return the PDF data as a response
            response = Response(pdf_data, mimetype='application/pdf')
            response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
            return response
        else:
            return 'Error processing LaTeX file', 500
    else:
        return 'Invalid file type', 400

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

if __name__ == '__main__':
    app.run(debug=True)
