import os
from flask import Flask, send_file, request, jsonify
import pdflatex
import requests

app = Flask(__name__)

OUTPUT_FOLDER = 'test_output/'
TEST_INPUT_FOLDER = 'test_input/'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['TEST_INPUT_FOLDER'] = TEST_INPUT_FOLDER


@app.route("/")
def home():
    condition = request.args.get('condition', 'False')
    if condition == 'True':
        return "<h1>Welcome to the Flask Backend!</h1><p>This is the landing page of your backend.</p>"
    else:
        return "<h1>Condition not met</h1>"


@app.route("/test_conversion", methods=['GET'])
def convert_test_tex_file():

    send_attachment = request.args.get('send_attachment', 'False')
    
    tex_file_path = os.path.join(app.config['TEST_INPUT_FOLDER'], 'main.tex')
    
    if not os.path.exists(tex_file_path):
        return jsonify({"error": "Test .tex file not found"}), 404
    
    pdf_file_path = convert_tex_to_pdf(tex_file_path)
    
    if pdf_file_path:
        if send_attachment == 'True':
            return send_file(pdf_file_path, as_attachment=True)
        else:
            return jsonify({"message": "Conversion successful"})
    else:
        return jsonify({"error": "Error converting to PDF"}), 500


def convert_tex_to_pdf(tex_file_path):
    try:
        with open(tex_file_path, 'rb') as tex_file:
            pdfl = pdflatex.PDFLaTeX.from_binarystring(tex_file.read(), tex_file_path)
            pdf, log, cp = pdfl.create_pdf()
        
        output_pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.pdf')
        with open(output_pdf_path, 'wb') as output_file:
            output_file.write(pdf)
        
        return output_pdf_path
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None


if __name__ == "__main__":
    app.run(debug=True)
