from flask import Flask, jsonify, Response
from PIL import Image
import os
import io
import openai
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

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
    """Read the LaTeX file and use GPT to extract function definitions."""
    if not os.path.exists(TEXT_FILE):
        return 'Text file not found', 404

    try:
        # Read the LaTeX file
        with open(TEXT_FILE, 'r', encoding='utf-8') as f:
            text_data = f.read()

        # Prepare the prompt to ask GPT to extract function definitions
        messages = [
            {"role": "system", "content": "You are a helpful assistant that extracts functions from LaTeX code."},
            {"role": "user", "content": f"Extract all the function definitions from the following LaTeX text:\n\n{text_data}"}
        ]

        # Make the API call to OpenAI GPT to process the text
        completion = client.chat.completions.create()(
            model="gpt-4",
            messages=messages,
            max_tokens=1000,  # Adjust depending on the size of your LaTeX file
            temperature=0.2  # Lower temperature for more deterministic responses
        )
        print('hi')

        # Get the extracted functions from the GPT response
        # extracted_functions = response['choices'][0]['message']['content'].strip()
        extracted_functions = completion.choices[0].message.content()

        print(extracted_functions)

        # Return the extracted functions as a JSON response
        return jsonify({'message': 'Functions extracted', 'functions': extracted_functions})

    except Exception as e:
        return f"Error processing LaTeX file: {str(e)}", 500

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
