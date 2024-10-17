from slide_creator import *
from compiler import *
import json

# Ensure the output directory exists
create_output_directory()

with open('formulas.json', 'r') as f:
    formulas = json.load(f)
    formulas = formulas['formulas']

with open('images.json', 'r') as f:
    images = json.load(f)
    images = images['images']
    
with open('structure.json', 'r') as f:
    structure = json.load(f)

# Initialize the SlideCreator with the given structure
slide_creator = SlideCreator(
    title=structure['title'],
    name=structure['name'],
    date=structure['date'],
    sections=structure['sections']
)



## Add slides to each section


# Introduction section
slide_creator.add_slide("Introduction")  # Slide 0

# Theory section
slide_creator.add_slide("Theory")  # Slide 0
slide_creator.add_slide("Theory")  # Slide 1

# Methodology section
slide_creator.add_slide("Methodology")  # Slide 0
slide_creator.add_slide("Methodology")  # Slide 1

# Performance Metrics and Evaluation section
slide_creator.add_slide("Performance Metrics and Evaluation")  # Slide 0
slide_creator.add_slide("Performance Metrics and Evaluation")  # Slide 1

# Results section
slide_creator.add_slide("Results")  # Slide 0

# Discussion section
slide_creator.add_slide("Discussion")  # Slide 0
slide_creator.add_slide("Discussion")  # Slide 1

# Conclusion section
slide_creator.add_slide("Conclusion")  # Slide 0



slide_creator.add_slide("Introduction") 



# also slide_creator.remove_slide can be used



slide_creator.add_formula_to_slide("Introduction", 0, "E_0 \\leq \\frac{\\bra{\\psi}\\hat{H}\\ket{\\psi}}{\\bra{\\psi}\\psi\\rangle}.")



# also slide_creator.add_image can be used



slide_creator.edit_slide_with_prompt("Introduction", 0, "Give an introduction to how the given formula is used in quantum computing.")





# Introduction slides
intro_formula = formulas[0] 
slide_creator.add_formula_to_slide("Introduction", 1, intro_formula)
intro_prompt = "Provide an overview of quantum computing in finance and introduce VQE for portfolio optimization."
slide_creator.edit_slide_with_prompt("Introduction", 1, intro_prompt)

## Theory slides
# Slide 0
theory_formula1 = formulas[1]  # VQE energy formula
slide_creator.add_formula_to_slide("Theory", 0, theory_formula1)
theory_prompt1 = "Explain the objective of the VQE algorithm in finding the ground state energy."
slide_creator.edit_slide_with_prompt("Theory", 0, theory_prompt1)

# Slide 1
theory_formula2 = formulas[2]  # Hamiltonian decomposition
slide_creator.add_formula_to_slide("Theory", 1, theory_formula2)
theory_image1 = images[2]  # hamiltonian.png
slide_creator.add_image_to_slide("Theory", 1, theory_image1)
theory_prompt2 = "Describe how the Hamiltonian is represented as a sum of weighted Pauli operators."
slide_creator.edit_slide_with_prompt("Theory", 1, theory_prompt2)

## Methodology slides
# Slide 0
method_formula1 = formulas[4]  # Unitary operator U_i(θ)
slide_creator.add_formula_to_slide("Methodology", 0, method_formula1)
method_image1 = images[1]  # quantum_circuit.png
slide_creator.add_image_to_slide("Methodology", 0, method_image1)
method_prompt1 = "Detail the construction of parameterized quantum circuits in VQE."
slide_creator.edit_slide_with_prompt("Methodology", 0, method_prompt1)

# Slide 1
method_formula2 = formulas[3]  # L(b) function
slide_creator.add_formula_to_slide("Methodology", 1, method_formula2)
method_prompt2 = "Explain the optimization problem transformed into a loss function L(b) for VQE."
slide_creator.edit_slide_with_prompt("Methodology", 1, method_prompt2)

## Performance Metrics and Evaluation slides
# Slide 0
performance_formula1 = formulas[5]  # Risk calculation
slide_creator.add_formula_to_slide("Performance Metrics and Evaluation", 0, performance_formula1)
performance_prompt1 = "Discuss how risk is quantified in the context of portfolio optimization."
slide_creator.edit_slide_with_prompt("Performance Metrics and Evaluation", 0, performance_prompt1)

# Slide 1
performance_formula2 = formulas[8]  # Covariance formula
slide_creator.add_formula_to_slide("Performance Metrics and Evaluation", 1, performance_formula2)
performance_prompt2 = "Explain the calculation of covariance between assets."
slide_creator.edit_slide_with_prompt("Performance Metrics and Evaluation", 1, performance_prompt2)

## Results slide
results_image = images[5]  # Results_Graph.png
slide_creator.add_image_to_slide("Results", 0, results_image)
results_prompt = "Present the experimental results of the VQE algorithm applied to portfolio optimization."
slide_creator.edit_slide_with_prompt("Results", 0, results_prompt)

## Discussion slides
# Slide 0
discussion_prompt1 = "Analyze the performance benefits and challenges of using VQE over classical methods."
slide_creator.edit_slide_with_prompt("Discussion", 0, discussion_prompt1)

# Slide 1
discussion_image = images[7]  # Entanglement Analysis SU2.png
slide_creator.add_image_to_slide("Discussion", 1, discussion_image)
discussion_prompt2 = "Discuss the role of entanglement in improving the VQE algorithm's performance."
slide_creator.edit_slide_with_prompt("Discussion", 1, discussion_prompt2)

## Conclusion slide
conclusion_prompt = "Summarize the study's findings and the potential impact of quantum algorithms in finance."
slide_creator.edit_slide_with_prompt("Conclusion", 0, conclusion_prompt)


tex_to_pdf('output/slides.tex')
pdf_to_png('output/slides.pdf')

print("Slides have been created and updated in 'output/slides.tex'.")
