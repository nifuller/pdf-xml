"""
==================
THINGS TO-DO
==================
Need to test longer pdf files
    -Need to figure out batching for longer pdfs
"""
from pdfminer.high_level import extract_text
from openai import OpenAI
from tkinter import Tk
from tkinter.filedialog import askopenfilename

intro = """
██████╗ ██████╗ ███████╗    ████████╗ ██████╗     ██╗  ██╗███╗   ███╗██╗          ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝    ╚══██╔══╝██╔═══██╗    ╚██╗██╔╝████╗ ████║██║         ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝██║  ██║█████╗         ██║   ██║   ██║     ╚███╔╝ ██╔████╔██║██║         ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
██╔═══╝ ██║  ██║██╔══╝         ██║   ██║   ██║     ██╔██╗ ██║╚██╔╝██║██║         ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
██║     ██████╔╝██║            ██║   ╚██████╔╝    ██╔╝ ██╗██║ ╚═╝ ██║███████╗    ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝     ╚═════╝ ╚═╝            ╚═╝    ╚═════╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                                                                                              
██████╗  ██████╗ ██╗    ██╗███████╗██████╗ ███████╗██████╗     ██████╗ ██╗   ██╗     ██████╗██╗  ██╗ █████╗ ████████╗ ██████╗ ██████╗ ████████╗               
██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗██╔════╝██╔══██╗    ██╔══██╗╚██╗ ██╔╝    ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔════╝ ██╔══██╗╚══██╔══╝               
██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝█████╗  ██║  ██║    ██████╔╝ ╚████╔╝     ██║     ███████║███████║   ██║   ██║  ███╗██████╔╝   ██║                  
██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗██╔══╝  ██║  ██║    ██╔══██╗  ╚██╔╝      ██║     ██╔══██║██╔══██║   ██║   ██║   ██║██╔═══╝    ██║                  
██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║███████╗██████╔╝    ██████╔╝   ██║       ╚██████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║        ██║                  
╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝     ╚═════╝    ╚═╝        ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝        ╚═╝                                                                                                                                                                               
"""

print(intro)


#opens up a window for user to select pdf file
Tk().withdraw()
file_path = askopenfilename()

#convert pdfs to a string
pdf_text = extract_text(file_path)



prompt_example = """
====================================================================================================================================================
||                                                            EXAMPLE PROMPT                                                                      ||
====================================================================================================================================================
                        'convert to xml: medical, patient, last_name first_name, payment, payment_amount, payment_date'
"""
print(prompt_example)

#grab user's input. should only be entering xml related prompts
user_prompt = input('Enter prompt command:')

#restricts the user to only XML related conversions
assistant_prompt = """
You are a helpful assistant. You only convert user 
pdf_text strings to xml. Only accept convert to xml
prompts. User may use element to describe xml elements.
"""

client = OpenAI()
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages= [{"role": "system", "content": assistant_prompt},
               {"role": "user", "content": "xml version and endcoding" + user_prompt},
               {"role": "assistant", "content": pdf_text}
              ],
    stream=True,
    max_tokens=256,
    n=1,
    stop=None
)
file_name = input('Enter file name to save:')
file = open(file_name + ".xml", "w", encoding="utf-8")
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        file.write(chunk.choices[0].delta.content)
        print(chunk.choices[0].delta.content, end="")