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
