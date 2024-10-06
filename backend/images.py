import openai
from openai import OpenAI
import os
import re
from flask import Flask, jsonify, Response
from PIL import Image


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

