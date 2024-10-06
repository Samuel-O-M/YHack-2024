import subprocess
import os

def tex_to_pdf(tex_file_path, output_dir=None):
    # Check if the file exists
    if not os.path.exists(tex_file_path):
        raise FileNotFoundError(f"The file {tex_file_path} does not exist.")

    # Construct the pdflatex command
    command = ['pdflatex', '-interaction=nonstopmode', tex_file_path]
    
    # Set output directory if specified
    if output_dir:
        command.insert(1, f'-output-directory={output_dir}')
    
    # Run the command to compile the tex file to pdf
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check if the process was successful
    if process.returncode != 0:
        print("Error during PDF generation.")
        print(process.stderr.decode())
    else:
        print("PDF successfully generated.")

# Example usage:
# tex_file = r'C:\Users\chuck\Downloads\text.txt'
# output_directory = r'C:\Users\chuck\Downloads\output_folderr'  # You can specify an output folder or leave it as None
# tex_to_pdf(tex_file, output_directory)

import json

# def list_to_json(lst):
    # # Create a dictionary from the list where keys are numbers starting from 1
    # dictionary = {str(index + 1): item for index, item in enumerate(lst)}
    # # Convert the dictionary to a JSON string
    # return json.dumps(dictionary, indent=4)

def list_to_json(lst):
    # Create a dictionary with "formulas" as the key and the list as the value
    dictionary = {"formulas": lst}
    # Convert the dictionary to a JSON string
    return json.dumps(dictionary, indent=4)

# Example usage
list_of_strings = [["E_0 \\leq \\frac{\\bra{\\psi}\\hat{H}\\ket{\\psi}}{\\bra{\\psi}\\psi\\rangle}.", "E_{\\text{VQE}} = \\min_{\\theta} \\bra{0}U^\\dagger(\\theta) \\hat{H} U(\\theta)\\ket{0}.", "\\hat{P}_a \\in \\{I, X, Y, Z\\}^{\\otimes N},", "\\hat{H} = \\sum_a w_a \\hat{P}_a,", "E_{\\text{VQE}} = \\min_{\\theta} \\sum_a w_a \\bra{0}U^\\dagger(\\theta) \\hat{P}_a U(\\theta)\\ket{0},"]]
json_result = list_to_json(list_of_strings)
print(json_result)
