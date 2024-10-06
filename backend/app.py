from flask import Flask, jsonify, request
from compiler import *
from images import *
from formulas import *
from structure import *
from slide_creator import *


app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the SlideForge!"


# initialize
# get the images and the .tex from the paper
# process the images in images.py, sending to images.json
# process the .tex in structure.py, sending to structure.json
# process the formulas in formulas.py, sending to formulas.json
@app.route('/initialize', methods=['POST'])
def initialize():
    return 0


# call compiler.py.
# compile the .tex file from output using .tex and images
# convert the .pdf to .png 
@app.route('/compile', methods=['POST'])
def compile():
    clear_png('output/slide_png')
    tex_to_pdf('output/slides.tex', output_folder='input')
    pdf_to_png('input/slides.pdf')


# add image to the slide
# call slide_creator.py
@app.route('/add_image', methods=['POST'])
def add_image():
    return 0


# add formula to the slide
# call slide_creator.py
@app.route('/add_formula', methods=['POST'])
def add_formula():
    return 0


# add slide
# call slide_creator.py
@app.route('/add_slide', methods=['POST'])
def add_slide():
    return 0


# remove slide
# call slide_creator.py
@app.route('/remove_slide', methods=['POST'])
def remove_slide():
    return 0


# edit slide given prompt
# call slide_creator.py
@app.route('/edit_slide', methods=['POST'])
def edit_slide():
    return 0


# call compiler.py
# get the .pdf
@app.route('/get_pdf', methods=['GET'])
def get_pdf():
    return 0


# call compiler.py
# get the .tex
@app.route('/get_tex', methods=['GET'])
def get_tex():
    return 0


if __name__ == '__main__':
    app.run(debug=True)