import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter import filedialog
import convertor 

def browse_files():
    global filename
    filename = filedialog.askopenfilename(initialdir="/",
                                           title="select a file",
                                           filetypes=(("PDF files",
                                                       "*.pdf"),
                                                       ("all files",
                                                        "*.*")))
    lbl_filename["text"] = filename

def convert_pdf():
    global response
    pdf_text = convertor.pdf_conversion(filename)
    usr_prompt = entry_text.get("1.0", tk.END)
    response = convertor.xml_conversion(pdf_text, usr_prompt)


def save_xml():
    files = [('All Files', '*'),
             ('Python Files', '*.py'),
             ('XML Files', '*.xml')]
    file = asksaveasfile(filetypes=files, defaultextension=".xml")
    print(file.name)
    convertor.save_xml_file(response, file.name)

window = tk.Tk()
window.title("PDF Extractor")

window.rowconfigure(0, minsize=200, weight=1)
window.columnconfigure(1, minsize=200, weight=1)

menu_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
prompt_frame = tk.Frame(window, padx=10, pady=5)

entry_text = tk.Text(prompt_frame, height=10, width=50)
entry_text.grid(row=1, column=0)

lbl_prompt = tk.Label(prompt_frame, text="PROMPT ENTRY")
lbl_prompt.grid(row=0, column=0, sticky="nw")

lbl_filename = tk.Label(master=window, text="Test")
lbl_filename.grid(row=4, column=1, stick="w")

btn_open = tk.Button(menu_buttons, text="Open", command=browse_files)
btn_open.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

btn_convert = tk.Button(menu_buttons, text="Convert", command=convert_pdf)
btn_convert.grid(row=0, column=2, sticky="ew")

btn_save = tk.Button(menu_buttons, text="Save", command=save_xml)
btn_save.grid(row=0, column=3, sticky="ew")


menu_buttons.grid(row=1, column=1, sticky="sw")
prompt_frame.grid(row=0, column=1)

window.mainloop()