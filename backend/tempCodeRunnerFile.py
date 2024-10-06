

def get_sections_from_latex(latex_content):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for extracting LaTeX document structures."},
            {"role": "user", "content": f"Extract all the function definitions from the following text, 
             don't give me the name of the equation, and remove the slashes and brackets at the beginning and end of the functions: \n\n{latex_content}"}
        ]
    )

    sections = response.choices[0].message.content.strip()
    return sections
