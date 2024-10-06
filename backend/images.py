import openai
from openai import OpenAI
import os
import re
from flask import Flask, jsonify, Response
from PIL import Image
import json


def process_images(image_folder="./backend/output/images/"):
    """
    Process and list all PNG images in the specified folder.
    
    Args:
        image_folder (str): Path to the images folder.
        
    Returns:
        list: List of image filenames.
    """
    try:
        image_filenames = [f for f in os.listdir(image_folder) if f.lower().endswith('.png')]
        return image_filenames
    except FileNotFoundError:
        print(f"Error: The folder '{image_folder}' does not exist.")
        return []
    except Exception as e:
        print(f"Error processing images: {e}")
        return []

def list_to_json(lst, file_path = "./backend/images.json"):
    # Create a dictionary with "formulas" as the key and the list as the value
    dictionary = {"images": lst}
    # Convert the dictionary to a JSON string
    with open(file_path, 'w') as json_file:
        json.dump(dictionary, json_file, indent=4)

if __name__ == "__main__":
    images = process_images()
    list_of_images = list_to_json(images)
