from flask import Flask, jsonify, Response
from PIL import Image
import os
import io
import openai
from openai import OpenAI

app = Flask(__name__)


# Paths to directories and files
IMAGE_FOLDER = 'backend/images'  # Path to the images directory
TEXT_FILE = 'backend/text.txt'           # Path to the text file


with open('secret_key', 'r') as key_file:
    openai.api_key = key_file.read().strip()
print(openai.api_key)
# openai.api_key = 'your-openai-api-key'

@app.route('/process-images', methods=['GET'])
def process_images():
    """Process all images stored locally in the images folder."""
    image_filenames = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith('.png')]
    
    if not image_filenames:
        return 'No images found in the directory', 400

    processed_images = []

    # Iterate through each image in the folder
    for filename in image_filenames:
        try:
            image_path = os.path.join(IMAGE_FOLDER, filename)
            image = Image.open(image_path)
            
            # Example: Convert image to grayscale
            grayscale_image = image.convert('L')

            # Save processed image to bytes buffer (in memory)
            buf = io.BytesIO()
            grayscale_image.save(buf, format='PNG')
            processed_images.append({
                'filename': filename,
                'data': buf.getvalue()
            })
        except Exception as e:
            return f"Error processing image {filename}: {str(e)}", 500

    return jsonify({'message': 'Images processed successfully', 'image_count': len(processed_images)})


def open_text(text_file):
        # Read the LaTeX file
    with open(text_file, 'r', encoding='utf-8') as f:
        text_data = f.read().strip()
    return text_data

# text = open_text(TEXT_FILE)
# print(text)




def read_latex_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_api_key(key_file_path):
    with open(key_file_path, 'r', encoding='utf-8') as key_file:
        return key_file.read().strip()

def get_sections_from_latex(latex_content, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for extracting LaTeX document structures."},
            {"role": "user", "content": f"Extract and list all the section titles from the following LaTeX document: \n\n{latex_content}"}
        ]
    )

    sections = response.choices[0].message.content.strip()
    return sections

@app.route('/process-text', methods=['GET'])
def process_text(text_data):
        # Prepare the prompt to ask GPT to extract function definitions
    client = OpenAI()
    # Make the API call to OpenAI GPT to process the text
    completion = client.chat.completions.create()(
        model="gpt-4o-mini",
        messages = [
        {"role": "system", "content": "You are a helpful assistant that extracts functions from LaTeX code."},
        {"role": "user", "content": f"Extract all the function definitions from the following LaTeX text:\n\n{text_data}"}
    ]
    )
    # Get the extracted functions from the GPT response
    # extracted_functions = response['choices'][0]['message']['content'].strip()
    extracted_functions = completion.choices[0].message.content.strip()
    return extracted_functions

        # Return the extracted functions as a JSON response
        # return jsonify({'message': 'Functions extracted', 'functions': extracted_functions})

    
text = process_text(TEXT_FILE)
print(text)

# if __name__ == '__main__':
#     app.run(debug=True)


# from openai import OpenAI

# client = OpenAI()

# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Write a haiku about recursion in programming."}
#     ]
# )

# # Correct print statement to access the content attribute
# print(completion.choices[0].message.content)


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
    tex_file = request.files['textfile']

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

    # move images -> output/images folder      names of the images -> images.json
    # move tex file -> input folder

    # Change current working directory to the temp directory
    original_cwd = os.getcwd()
    os.chdir(temp_dir)

    # Compile the LaTeX code
    pdf_data = compile_latex_to_pdf(text_filename)

    # Change back to the original working directory
    os.chdir(original_cwd)


    if pdf_data is not None:
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


'''
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
    tex_file = request.files['textfile']

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

    # move images -> output/images folder      names of the images -> images.json
    # move tex file -> input folder

    # Change current working directory to the temp directory
    original_cwd = os.getcwd()
    os.chdir(temp_dir)

    # Compile the LaTeX code
    pdf_data = compile_latex_to_pdf(text_filename)

    # Change back to the original working directory
    os.chdir(original_cwd)


    if pdf_data is not None:
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
'''