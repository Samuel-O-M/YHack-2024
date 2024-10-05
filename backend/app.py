from flask import Flask, jsonify, Response
from PIL import Image
import os
import io
import openai

app = Flask(__name__)

# Paths to directories and files
IMAGE_FOLDER = 'backend/images'  # Path to the images directory
TEXT_FILE = 'backend/text.txt'           # Path to the text file

with open('secret_key', 'r') as key_file:
    openai.api_key = key_file.read().strip()
# print(openai.api_key)
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


@app.route('/process-text', methods=['GET'])
def process_text():
    """Read and process the LaTeX or text file."""
    if not os.path.exists(TEXT_FILE):
        return 'Text file not found', 404

    try:
        # Read the text file
        with open(TEXT_FILE, 'r', encoding='utf-8') as f:
            text_data = f.read()

        # Here you can process the LaTeX text if needed
        # For example, compile the LaTeX to a PDF (if it's LaTeX code)
        return jsonify({'message': 'Text file processed', 'content': text_data})

    except Exception as e:
        return f"Error reading text file: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
