import openai
from openai import OpenAI
import os
import re
from flask import Flask, jsonify, Response
from PIL import Image
import json

def process_images():
    IMAGE_FOLDER = "./backend/output/images/"
    image_filenames  = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith('.png')]
    return image_filenames

def list_to_json(lst, file_path = "./backend/images.json"):
    # Create a dictionary with "formulas" as the key and the list as the value
    dictionary = {"images": lst}
    # Convert the dictionary to a JSON string
    with open(file_path, 'w') as json_file:
        json.dump(dictionary, json_file, indent=4)

images = process_images()
list_of_images = list_to_json(images)
# print(images)

# @app.route('/process-images', methods=['GET'])
# def process_images():
#     """Process all images stored locally in the images folder."""
#     image_filenames = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith('.png')]
    
#     if not image_filenames:
#         return 'No images found in the directory', 400

#     processed_images = []

#     # Iterate through each image in the folder
#     for filename in image_filenames:
#         try:
#             image_path = os.path.join(IMAGE_FOLDER, filename)
#             image = Image.open(image_path)
            
#             # Example: Convert image to grayscale
#             grayscale_image = image.convert('L')

#             # Save processed image to bytes buffer (in memory)
#             buf = io.BytesIO()
#             grayscale_image.save(buf, format='PNG')
#             processed_images.append({
#                 'filename': filename,
#                 'data': buf.getvalue()
#             })
#         except Exception as e:
#             return f"Error processing image {filename}: {str(e)}", 500

#     return jsonify({'message': 'Images processed successfully', 'image_count': len(processed_images)})

