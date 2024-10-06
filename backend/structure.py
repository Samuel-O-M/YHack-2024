from openai import OpenAI
import os
import openai
import json
import re



def get_file():
    input_dir = "./backend/input"
    tex_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.tex')]
    tex_files = [file.replace('\\', '/') for file in tex_files]
    return ', '.join(tex_files) if tex_files else None

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
            {"role": "user", "content": f"Extract and list all the authors from the following LaTeX document, do not add any descriptions.\n\n{latex_content}"}
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
        'title': [paper_name],  # Paper name as a list
        'sections': section_titles_list,  # Processed section titles list
        'name': authors_names_list,  # Processed authors names list
        'date': r'\today'  # Current date
    }

    
    # Convert the dictionary to JSON format and save it
    try:
        with open(file_path, 'w') as json_file:
            json.dump(parsed_data, json_file, indent=4)
        print(f"Structure data saved to {file_path}")
    except Exception as e:
        print(f"Error saving structure data: {e}")

def process_structure(tex_file_path):
    """
    Main function to process the LaTeX file and extract structure.
    
    Args:
        tex_file_path (str): Path to the LaTeX `.tex` file.
        structure_file_path (str): Path to save the structure JSON file.
    """
    api_key = load_openai_key()
    latex_content = open_text(tex_file_path)
    sections = get_sections_from_latex(latex_content, api_key)
    authors = get_authors_from_latex(latex_content, api_key)
    title = get_title_from_latex(latex_content, api_key)
    parsed_sections = process_sections(title, sections, authors)




    # Load OpenAI API key
    # api_key = load_openai_key()
    # if not api_key:
    #     print("OpenAI API key not loaded. Exiting process_tex.")
    #     return
    
    # # Read the LaTeX content
    # latex_content = open_text(tex_file_path)
    # if not latex_content:
    #     print("Failed to read LaTeX content. Exiting process_tex.")
    #     return
    
    # # Extract title, authors, and sections
    # title = get_title_from_latex(latex_content)
    # authors = get_authors_from_latex(latex_content)
    # sections = get_sections_from_latex(latex_content)
    
    # if not title:
    #     print("No title extracted. Skipping structure processing.")
    #     return
    
    # # Process and save the extracted data
    # process_sections(title, sections, authors, structure_file_path)

# def main():
#     api_key = load_openai_key()
#     file = get_file()
#     latex_content = open_text(file)
#     sections = get_sections_from_latex(latex_content, api_key)
#     authors = get_authors_from_latex(latex_content, api_key)
#     title = get_title_from_latex(latex_content, api_key)
#     parsed_sections = process_sections(title, sections, authors)

if __name__ == "__main__":
    tex_file_path = "./backend/input/paper.tex"
    process_tex(tex_file_path)
