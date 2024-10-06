from flask import Flask, jsonify, request
from flask_cors import CORS
from compiler import *
from images import *
from formulas import *
from structure import *
from slide_creator import *
import os

app = Flask(__name__)
CORS(app)

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
    try:
        if not os.path.exists('output/images'):
            os.makedirs('output/images')

        tex_file = request.files.get('tex_file')
        images = request.files.getlist('images[]')

        if not tex_file or not images:
            return jsonify({'status': 'error', 'message': 'Missing .tex file or images.'}), 400

        tex_file_path = 'input/paper.tex'
        tex_file.save(tex_file_path)

        image_filenames = []
        for image in images:
            image_filename = image.filename
            image.save(f'output/images/{image_filename}')
            image_filenames.append(image_filename)

        images_json_data = {
            "images": image_filenames
        }

        # process_structure('output/paper.tex', 'structure.json')
        # process_formulas('output/paper.tex', 'formulas.json')
        
        # with open('output/images.json', 'w') as json_file:
        #     json.dump(images_json_data, json_file, indent=4)

        # with open('structure.json', 'r') as json_file:
        #     data = json.load(json_file)

        slide_creator = SlideCreator(
            title='title',
            name='name',
            date='date',
            sections=['Introduction', 'Methods', 'Results', 'Discussion']
        )

        tex_to_pdf('output/slides.tex', output_folder='output')
        pdf_to_png('output/slides.pdf')
        png_files = get_png('output/slide_png')

        return jsonify({
            'status': 'success',
            'message': 'Initialization completed successfully.',
            'png_files': png_files
        }), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'An error occurred: {str(e)}'}), 500



# call compiler.py.
# compile the .tex file from output using .tex and images
# convert the .pdf to .png 
@app.route('/compile', methods=['POST'])
def compile():
    try:
        clear_png('output/slide_png')
        tex_to_pdf('output/slides.tex', output_folder='output')
        pdf_to_png('output/slides.pdf')
        png_files = get_png('output/slide_png')

        return jsonify({
            'status': 'success',
            'message': 'Compilation and conversion completed successfully.',
            'png_files': png_files
        }), 200

    except FileNotFoundError as e:
        return jsonify({'status': 'error', 'message': f'File not found: {str(e)}'}), 400

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'An error occurred: {str(e)}'}), 500



# add image to the slide
# call slide_creator.py
@app.route('/add_image', methods=['POST'])
def add_image():
    try:
        section = request.form.get('section')
        slide_number = int(request.form.get('slide_number'))
        image = request.form.get('image')

        slide_creator.add_image_to_slide(section, slide_number, image)
        return {'status': 'success', 'message': 'Image added to slide successfully.'}, 200
    except Exception as e:
        return {'status': 'error', 'message': f'An error occurred: {str(e)}'}, 500


# add formula to the slide
# call slide_creator.py
@app.route('/add_formula', methods=['POST'])
def add_formula():
    try:
        section = request.form.get('section')
        slide_number = int(request.form.get('slide_number'))
        formula = request.form.get('formula')

        slide_creator.add_formula_to_slide(section, slide_number, formula)
        return {'status': 'success', 'message': 'Formula added to slide successfully.'}, 200
    except Exception as e:
        return {'status': 'error', 'message': f'An error occurred: {str(e)}'}, 500


# add slide
# call slide_creator.py
@app.route('/add_slide', methods=['POST'])
def add_slide():
    try:
        section = request.form.get('section')
        position = request.form.get('position')

        slide_creator.add_slide(section, position)
        return {'status': 'success', 'message': 'Slide added successfully.'}, 200
    except Exception as e:
        return {'status': 'error', 'message': f'An error occurred: {str(e)}'}, 500


# remove slide
# call slide_creator.py
@app.route('/remove_slide', methods=['POST'])
def remove_slide():
    try:
        section = request.form.get('section')
        slide_number = int(request.form.get('slide_number'))

        slide_creator.remove_slide(section, slide_number)
        return {'status': 'success', 'message': 'Slide removed successfully.'}, 200
    except Exception as e:
        return {'status': 'error', 'message': f'An error occurred: {str(e)}'}, 500


# edit slide given prompt
# call slide_creator.py
@app.route('/edit_slide', methods=['POST'])
def edit_slide():
    try:
        section = request.form.get('section')
        slide_number = int(request.form.get('slide_number'))
        prompt = request.form.get('prompt')

        slide_creator.edit_slide_with_prompt(section, slide_number, prompt)
        return {'status': 'success', 'message': 'Slide edited successfully.'}, 200
    except Exception as e:
        return {'status': 'error', 'message': f'An error occurred: {str(e)}'}, 500


# call compiler.py
# get the .pdf
@app.route('/get_pdf', methods=['GET'])
def get_pdf():
    get_pdf('output/slides.pdf')


# call compiler.py
# get the .tex
@app.route('/get_tex', methods=['GET'])
def get_tex():
    get_tex('output/slides.tex')



if __name__ == '__main__':
    app.run(debug=True)