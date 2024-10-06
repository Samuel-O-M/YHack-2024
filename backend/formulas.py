import openai
from openai import OpenAI
import os
import re
from flask import Flask, jsonify, Response
from PIL import Image
import json


def get_file():
    input_dir = "./backend/input"
    tex_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.tex')]
    tex_files = [file.replace('\\', '/') for file in tex_files]
    return ', '.join(tex_files) if tex_files else None
    # return tex_files

file  = get_file()
print(file)
    

# TEXT_FILE = './backend/input/test.tex'       # Path to the text file
def load_openai_key(key_file_path='./backend/openai_key'):
    try:
        with open(key_file_path, 'r') as key_file:
            openai.api_key = key_file.read().strip()
            return openai.api_key
    except FileNotFoundError:
        print(f"Error: The file '{key_file_path}' was not found.")
        return None



def open_text(text_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        return file.read() 

# text = open_text(TEXT_FILE)



def get_functions_from_latex(latex_content, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for extracting LaTeX document structures."},
            {"role": "user", "content": f"Extract all the function definitions from the following text, do not give me the name of each equation or any other text description \n\n{latex_content}"}
        ]
    )

    functions = response.choices[0].message.content.strip()
    return functions

def split_latex_equations(latex_content):

    # Regex to match LaTeX equations enclosed in \[ and \]
    pattern = r'\\\[.*?\\\]'
    
    # Find all matches and clean them for pretty output if necessary
    equations = re.findall(pattern, latex_content, flags=re.DOTALL)
    
    return equations

def list_equations(equations_text):
    cleaned_equations = []
    for equation in equations_text:
        # Strip the opening and closing bracket notation if present
        if equation.startswith(r'\[') and equation.endswith(r'\]'):
            cleaned_equation = equation[2:-2]  # Remove the first two and last two characters
        else:
            cleaned_equation = equation
        
        # Further clean the equation by stripping leading/trailing whitespace and normalizing inner spaces
        cleaned_equation = cleaned_equation.strip()  # Remove leading/trailing whitespace and newlines
        cleaned_equation = ' '.join(cleaned_equation.split())  # Normalize spaces

        cleaned_equations.append(cleaned_equation)
    return cleaned_equations


def list_to_json(lst, file_path = "./backend/formulas.json"):
    # Create a dictionary with "formulas" as the key and the list as the value
    dictionary = {"formulas": lst}
    # Convert the dictionary to a JSON string
    with open(file_path, 'w') as json_file:
        json.dump(dictionary, json_file, indent=4)
        
def process_formulas(tex_file_path):
    """
    Main function to process the LaTeX file and extract formulas.
    
    Args:
        tex_file_path (str): Path to the LaTeX `.tex` file.
        formulas_file_path (str): Path to save the formulas JSON file.
    """
    text = open_text(tex_file_path)
    api_key = load_openai_key()
    functions = get_functions_from_latex(text, api_key)
    split_equations_text = split_latex_equations(functions)
    list_equations_text = list_equations(split_equations_text)
    json_string = list_to_json(list_equations_text)


    # Load OpenAI API key
    api_key = load_openai_key()
    if not api_key:
        print("OpenAI API key not loaded. Exiting process_formulas.")
        return
    
    # Read the LaTeX content
    latex_content = open_text(tex_file_path)
    if not latex_content:
        print("Failed to read LaTeX content. Exiting process_formulas.")
        return
    
    # Extract functions using OpenAI's API
    functions = get_functions_from_latex(latex_content, api_key)
    if not functions:
        print("No functions extracted. Skipping formula processing.")
        return
    
    # Split the extracted functions into individual equations
    split_equations_text = split_latex_equations(functions)
    
    # Clean and normalize the equations
    list_equations_text = list_equations(split_equations_text)
    
    # Save the list of formulas to JSON
    list_to_json(list_equations_text)


if __name__ == "__main__":
    # Define the path to the LaTeX file and the formulas JSON file
    tex_file_path = "./backend/input/paper.tex"
    process_formulas(tex_file_path)



# def main():
#     file = get_file()
#     text = open_text(file)
#     api_key = load_openai_key()
#     functions = get_functions_from_latex(text, api_key)
#     print(functions)
#     split_equations_text = split_latex_equations(functions)
#     list_equations_text = list_equations(split_equations_text)
#     json_string = list_to_json(list_equations_text)

