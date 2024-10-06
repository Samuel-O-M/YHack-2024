from openai import OpenAI
import os
import openai
import json


TEXT_FILE = './backend/output/test.tex'       # Path to the text file

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



def get_sections_from_latex(latex_content, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for extracting LaTeX document structures."},
            {"role": "user", "content": f"Extract and list all the section titles from the following LaTeX document, do not add any additional text: \n\n{latex_content}"}
        ]
    )

    sections = response.choices[0].message.content.strip()
    return sections


def get_authors_from_latex(latex_content, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for extracting LaTeX document structures."},
            {"role": "user", "content": f"Extract and list all the authors from the following LaTeX document, do not add any descriptions: \n\n{latex_content}"}
        ]
    )

    authors = response.choices[0].message.content.strip()
    return authors


def get_title_from_latex(latex_content, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for extracting LaTeX document structures."},
            {"role": "user", "content": f"Extract the title from the following LaTeX document and remove any backslashes, do not add any descriptions: \n\n{latex_content}"}
        ]
    )

    title = response.choices[0].message.content.strip()
    return title
    


def process_sections(paper_name, section_titles, authors_names, file_path = "./backend/structure.json"):
    # Ensure that the inputs are lists, and remove any newline characters
    section_titles_list = section_titles.splitlines()
    authors_names_list = authors_names.splitlines()
    
    # Remove empty lines or any trailing spaces from the list items
    section_titles_list = [title.strip() for title in section_titles_list if title.strip()]
    authors_names_list = [author.strip() for author in authors_names_list if author.strip()]
    
    # Create a dictionary with each part as a list
    parsed_data = {
        'paper_name': [paper_name],  # Paper name as a list
        'section_titles': section_titles_list,  # Processed section titles list
        'authors_names': authors_names_list  # Processed authors names list
    }
    
    # Convert the dictionary to JSON format and return it
    with open(file_path, 'w') as json_file:
        json.dump(parsed_data, json_file, indent=4)



def main():
    api_key = load_openai_key()
    latex_content = open_text(TEXT_FILE)
    sections = get_sections_from_latex(latex_content, api_key)
    authors = get_authors_from_latex(latex_content, api_key)
    title = get_title_from_latex(latex_content, api_key)
    parsed_sections = process_sections(title, sections, authors)

if __name__ == "__main__":
    main()
