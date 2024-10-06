from openai import OpenAI
import openai
import os
import re

IMAGE_FOLDER = 'backend/images'  # Path to the images directory
TEXT_FILE = 'backend/text.txt'           # Path to the text file
    
def open_text(text_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        return file.read() 

with open('secret_key', 'r') as key_file:
    openai.api_key = key_file.read().strip()
print(openai.api_key)


def get_functions_from_latex(latex_content):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for extracting LaTeX document structures."},
            {"role": "user", "content": f"Extract all the function definitions from the following text, do not give me the name of each equation \n\n{latex_content}"}
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


        
def main():
    text = open_text(TEXT_FILE)
    functions = get_functions_from_latex(text)
    split_equations_text = split_latex_equations(functions)
    list_equations_text = list_equations(split_equations_text)
    print(list_equations_text)

if __name__ == "__main__":
    main()
