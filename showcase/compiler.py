# one function that converts .tex (in output) to .pdf (in output)
# one function that gets the .tex file (in output)
# one function that gets the .pdf file (in output)
# one function that converts the .pdf to images and stores them (in output/slide_png)
# one function that gets the images (in output/slide_png)


import subprocess
import os
import base64
import shutil
from pdf2image import convert_from_path  # Requires pdf2image module


def tex_to_pdf(tex_file_path, output_folder='output'):
    
    if not tex_file_path.endswith(".tex"):
        raise ValueError("The provided file is not a .tex file.")

    file_dir = os.path.dirname(tex_file_path)
    file_name = os.path.basename(tex_file_path)

    try:
        subprocess.run(["pdflatex", file_name], cwd=file_dir, check=True)
        pdf_file = file_name.replace(".tex", ".pdf")
        pdf_path = os.path.join(file_dir, pdf_file)

        if os.path.exists(pdf_path):     
            # return pdf_path       
            output_pdf_path = os.path.join(output_folder, pdf_file)
            shutil.move(pdf_path, output_pdf_path)
        else:
            raise FileNotFoundError(f"PDF not generated: {pdf_path}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error compiling LaTeX file: {str(e)}")


def get_tex(tex_file_path):
    with open(tex_file_path, 'rb') as f:
        return f.read()

def get_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as f:
        return f.read()


def pdf_to_png(pdf_file_path, output_folder='output/slide_png'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(output_folder):
        if file_name.endswith('.png'):
            os.remove(os.path.join(output_folder, file_name))

    images = convert_from_path(pdf_file_path)
    
    image_paths = []
    for i, image in enumerate(images):
        image_file = os.path.join(output_folder, f'slide_{i+1}.png')
        image.save(image_file, 'PNG')
        image_paths.append(image_file)


def get_png(image_folder):
    image_data = []
    for file_name in os.listdir(image_folder):
        if file_name.endswith('.png'):
            file_path = os.path.join(image_folder, file_name)
            with open(file_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                image_data.append({
                    'file_name': file_name,
                    'image_data': encoded_string
                })
    return image_data


def clear_pdf(pdf_file_path):
    os.remove(pdf_file_path)


def clear_png(image_folder):
    for file_name in os.listdir(image_folder):
        if file_name.endswith('.png'):
            os.remove(os.path.join(image_folder, file_name))


if __name__ == "__main__":
    clear_png('output/slide_png')
    tex_to_pdf('output/slides.tex', output_folder='input')
    pdf_to_png('input/slides.pdf')
    get_pdf('input/slides.pdf')
