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
