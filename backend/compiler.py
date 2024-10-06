import os
import pdflatex
from pdf2image import convert_from_path
from io import BytesIO

folder = 'output'
os.makedirs(folder, exist_ok=True)

def convert_tex_to_pdf(tex_file_path):
    with open(tex_file_path, 'rb') as tex_file:
        pdfl = pdflatex.PDFLaTeX.from_binarystring(tex_file.read(), tex_file_path)
        pdf, log, cp = pdfl.create_pdf()
    return pdf

def convert_tex_file():
    tex_file_path = os.path.join(folder, 'slides.tex')
    if not os.path.exists(tex_file_path):
        raise FileNotFoundError("Test .tex file not found")
    try:
        pdf_content = convert_tex_to_pdf(tex_file_path)
    except Exception:
        raise RuntimeError("Error converting to PDF")
    output_pdf_path = os.path.join(folder, 'slides.pdf')
    try:
        with open(output_pdf_path, 'wb') as f:
            f.write(pdf_content)
    except Exception:
        raise IOError("Error writing PDF file")
    return output_pdf_path

def get_tex_file():
    tex_file_path = os.path.join(folder, 'slides.tex')
    if not os.path.exists(tex_file_path):
        raise FileNotFoundError("slides.tex not found")
    with open(tex_file_path, 'rb') as f:
        return f.read()

def get_pdf_file():
    pdf_file_path = os.path.join(folder, 'slides.pdf')
    if not os.path.exists(pdf_file_path):
        raise FileNotFoundError("slides.pdf not found")
    with open(pdf_file_path, 'rb') as f:
        return f.read()

def convert_pdf_to_images():
    pdf_file_path = os.path.join(folder, 'slides.pdf')
    if not os.path.exists(pdf_file_path):
        raise FileNotFoundError("slides.pdf not found")
    try:
        images = convert_from_path(pdf_file_path)
        image_bytes_list = []
        for img in images:
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            image_bytes_list.append(img_byte_arr.getvalue())
        return image_bytes_list
    except Exception:
        raise RuntimeError("Error converting PDF to images")

if __name__ == "__main__":
    try:
        pdf_file_path = convert_tex_file()
        print("Conversion successful")
        print(f"PDF saved to '{pdf_file_path}'")
        tex_content = get_tex_file()
        print(f"Retrieved slides.tex of size {len(tex_content)} bytes")
        pdf_content = get_pdf_file()
        print(f"Retrieved slides.pdf of size {len(pdf_content)} bytes")
        images = convert_pdf_to_images()
        for idx, img in enumerate(images, start=1):
            image_path = os.path.join(folder, 'slide_png', f'slide_{idx}.png')
            with open(image_path, 'wb') as img_file:
                img_file.write(img)
            print(f"Image saved to '{image_path}'")
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except IOError as e:
        print(f"I/O error: {e}")
    except RuntimeError as e:
        print(f"Runtime error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
