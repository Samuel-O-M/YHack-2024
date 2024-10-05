from openai import OpenAI
import os

def read_latex_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_api_key(key_file_path):
    with open(key_file_path, 'r', encoding='utf-8') as key_file:
        return key_file.read().strip()

def get_sections_from_latex(latex_content, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for extracting LaTeX document structures."},
            {"role": "user", "content": f"Extract and list all the section titles from the following LaTeX document: \n\n{latex_content}"}
        ]
    )

    sections = response.choices[0].message.content.strip()
    return sections

def main():
    latex_file_path = os.path.join("test_input", "paper.tex")
    key_file_path = os.path.join(os.getcwd(), "openai_key")
    api_key = read_api_key(key_file_path)
    latex_content = read_latex_file(latex_file_path)
    sections = get_sections_from_latex(latex_content, api_key)
    print("Extracted Sections:")
    print(sections)

if __name__ == "__main__":
    main()
