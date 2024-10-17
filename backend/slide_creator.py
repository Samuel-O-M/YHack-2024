import json
import os
import shutil
from openai import OpenAI
import re


def chatgpt(slide, prompt, section):

    key_file_path = os.path.join(os.getcwd(), "openai_key")

    with open(key_file_path, 'r', encoding='utf-8') as key_file:
        api_key = key_file.read().strip()

    client = OpenAI(api_key=api_key)

    paper_file_path = os.path.join(os.getcwd(), 'input', 'paper.tex')

    with open(paper_file_path, 'r', encoding='utf-8') as paper_file:
        paper = paper_file.read()

    prompt = f'''Task: Given this LaTeX slide, {prompt}. Make this a simplified and concise slide, relevant to a specific section of the paper, including the formula or image provided. Use bullet points and blocks to organize the content.

Slide: {slide}

Paper: {paper} \n'''

    format = '''\n Format: Return the code in this format:

```latex
\\begin{frame}{''' + section + '''}
...
\\end{frame}
```
    '''

    print(format)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for designing document structures."},
            {"role": "user", "content": prompt + format}
        ]
    )

    answer = response.choices[0].message.content.strip()

    answer = answer.strip('`')

    if answer.startswith('latex'):
        answer = answer[5:]

    frame_pattern = r'\\begin{frame}\{(.*?)\}(.*?)\\end{frame}'

    match = re.search(frame_pattern, answer, re.DOTALL)
    
    if match:
        section_name = match.group(1).strip()
        content = match.group(2).strip()
        return content
    else:
        return None


class SlideCreator:
    def __init__(self, title, name, date, sections):
        
        with open('formulas.json', 'r') as f:
            self.formulas = json.load(f)['formulas']
        with open('images.json', 'r') as f:
            self.images = json.load(f)['images']

        print(self.formulas)
        print(self.images)
        
        self.title = title
        self.name = name
        self.date = date
        self.sections = sections
        self.slides = {section: [] for section in sections}
        self.document_preamble = []
        self.slide_count = 0
        self.init_document()
        
    def init_document(self):
        
        self.document_preamble.extend([
            '\\documentclass{beamer}\n',
            '\\usetheme{Madrid}\n',
            '\\usepackage{amsmath}\n', 
            '\\usepackage{graphicx}\n', 
            '\\title{' + self.title + '}\n',
            '\\subtitle{}\n',
            '\\author{' + self.name + '}\n',
            '\\institute{}\n',
            '\\date{' + self.date + '}\n',
            '\\begin{document}\n',
            '\\begin{frame}\n',
            '\\titlepage\n',
            '\\end{frame}\n',
            '\\begin{frame}{Table of Contents}\n',
            '\\tableofcontents\n',
            '\\end{frame}\n'
        ])
        self.update_document()
        
    def update_document(self):
        
        content = self.document_preamble.copy()
        self.slide_count = 2 

        for section in self.sections:
            content.append('\\section{' + section + '}\n')
            content.extend([
                '\\begin{frame}\n',
                '\\centering\n',
                '\\Huge{' + section + '}\n',
                '\\end{frame}\n'
            ])
            self.slide_count += 1  

            for slide in self.slides[section]:
                content.append('\\begin{frame}{' + section + '}\n')
                content.extend(slide)
                content.append('\\end{frame}\n')
                self.slide_count += 1

        content.extend([
            '\\begin{frame}\n',
            '\\centering\n',
            '\\Huge{Thank You!}\n',
            '\\end{frame}\n',
            '\\end{document}\n'
        ])
        self.slide_count += 1  

        with open(os.path.join('output', 'slides.tex'), 'w') as f:
            f.writelines(content)


    def add_slide(self, section, position=None):
        if section not in self.sections:
            print(f"Section '{section}' does not exist.")
            return
        slide = []
        if position is None:
            self.slides[section].append(slide)
        else:
            if isinstance(position, int) and 0 <= position <= len(self.slides[section]):
                self.slides[section].insert(position, slide)
            else:
                print(f"Invalid position {position} for section '{section}'. Slide not added.")
                return
        self.update_document()

            
    def remove_slide(self, section, slide_number):
        if section not in self.sections:
            print(f"Section '{section}' does not exist.")
            return
        if 0 <= slide_number < len(self.slides[section]):
            del self.slides[section][slide_number]
            self.update_document()
        else:
            print(f"Slide number {slide_number} is out of range in section '{section}'.")


    def add_formula_to_slide(self, section, slide_number, formula):
        if section not in self.sections:
            print(f"Section '{section}' does not exist.")
            return
        if formula not in self.formulas:
            print(f"Formula '{formula}' is not available.")
            return
        if 0 <= slide_number < len(self.slides[section]):
            slide = self.slides[section][slide_number]
            slide.extend([
                r'\begin{align*}',
                formula,
                r'\end{align*}'
            ])
            self.slides[section][slide_number] = slide
            self.update_document()
        else:
            print(f"Slide number {slide_number} is out of range in section '{section}'.")


    def add_image_to_slide(self, section, slide_number, image):
        if section not in self.sections:
            print(f"Section '{section}' does not exist.")
            return
        if image not in self.images:
            print(f"Image '{image}' is not available.")
            return
        if 0 <= slide_number < len(self.slides[section]):
            slide = self.slides[section][slide_number]
            slide.extend([
                r'\begin{figure}[h]',
                r'\centering',
                rf'\includegraphics[width=0.8\textwidth]{{{image}}}',
                r'\end{figure}'
            ])
            self.slides[section][slide_number] = slide
            self.update_document()
        else:
            print(f"Slide number {slide_number} is out of range in section '{section}'.")


    def edit_slide_with_prompt(self, section, slide_number, prompt):
        if section not in self.sections:
            print(f"Section '{section}' does not exist.")
            return
        if 0 <= slide_number < len(self.slides[section]):
            old_slide = ['\\begin{frame}{' + section + '}\n']
            old_slide.extend(self.slides[section][slide_number])
            old_slide.append('\\end{frame}\n')
            slide = chatgpt(old_slide, prompt, section)
            self.slides[section][slide_number] = slide
            self.update_document()
        else:
            print(f"Slide number {slide_number} is out of range in section '{section}'.")


def create_output_directory(directory='output'):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")


if __name__ == "__main__":
    create_output_directory()

    with open('structure.json', 'r') as json_file:
        data = json.load(json_file)

    slide_creator = SlideCreator(
        title=data['title'],
        name=data['author'],
        date=data['date'],
        sections=data['sections']
    )

    slide_creator.add_slide("Introduction")

    slide_creator.add_slide("Theory")
    slide_creator.add_slide("Theory")

    slide_creator.add_slide("Methodology")
    slide_creator.add_slide("Methodology")

    slide_creator.add_slide("Performance Metrics and Evaluation")

    slide_creator.add_slide("Results")

    slide_creator.add_slide("Discussion")

    slide_creator.add_slide("Conclusion")

    



    slide_creator.add_formula_to_slide("Introduction", 0, "f(x) = x^2")
    slide_creator.add_formula_to_slide("Introduction", 0, "g(x) = 2x + 5")
    slide_creator.add_formula_to_slide("Introduction", 0, "p(x) = x^3 - 4x + 1")

    slide_creator.add_formula_to_slide("Formulas", 0, "f(x) = x^2")
    slide_creator.add_formula_to_slide("Formulas", 1, "g(x) = 2x + 5")
    slide_creator.add_formula_to_slide("Formulas", 1, "p(x) = x^3 - 4x + 1")
    slide_creator.add_formula_to_slide("Formulas", 1, "p(x) = x^3 - 4x + 1")
    
    slide_creator.add_image_to_slide("Images", 0, "image1.png")
    slide_creator.add_image_to_slide("Images", 0, "icon.png")

    slide_creator.add_image_to_slide("Conclusion", 0, "image2.png")

    slide_creator.edit_slide_with_prompt("Introduction", 0, "Explain what this formula means, regardless of the paper")

    slide_creator.remove_slide("Conclusion", 0)

    print("Test sequence completed. The final LaTeX document is saved in 'output/slides.tex'.")
