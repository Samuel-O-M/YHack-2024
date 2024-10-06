import openai
from openai import OpenAI
import os
import re
from flask import Flask, jsonify, Response
from PIL import Image
import json

TEXT_FILE = './backend/output/test.tex'       # Path to the text file

with open('./backend/openai_key', 'r') as key_file:
    openai.api_key = key_file.read().strip()
    print(openai.api_key)

def open_text(text_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        return file.read() 

text = open_text(TEXT_FILE)



def get_functions_from_latex(latex_content):
    client = OpenAI()

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
        
def main():
    text = open_text(TEXT_FILE)
    functions = get_functions_from_latex(text)
    print(functions)
    split_equations_text = split_latex_equations(functions)
    list_equations_text = list_equations(split_equations_text)
    json_string = list_to_json(list_equations_text)


if __name__ == "__main__":
    main()

