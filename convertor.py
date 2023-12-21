"""
==================
THINGS TO-DO
==================
Need to test longer pdf files
    -Need to figure out batching for longer pdfs
"""
from pdfminer.high_level import extract_text
from openai import OpenAI

#convert pdfs to a string
def pdf_conversion(file_path):
    pdf_text = extract_text(file_path)
    return pdf_text


def xml_conversion(pdf_text, user_prompt):
    #restricts the user to only XML related conversions
    assistant_prompt = """
    You are a helpful assistant. You only convert user 
    pdf_text strings to xml. Only accept convert to xml 
    prompts.Have an underscore between names. Always
    include xml header.
    """

    client = OpenAI()
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [{"role": "system", "content": assistant_prompt},
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": pdf_text}
                ],
        stream=True,
        max_tokens=256,
        n=1,
        stop=None
    )
    return stream

def display_response(stream):
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

def save_xml_file(stream, xml_file_name):
    #file_name = input('Enter file name to save:')
    file = open(xml_file_name, "w", encoding="utf-8")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            file.write(chunk.choices[0].delta.content)