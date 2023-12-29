import tkinter as tk
import pdf_converter
from tkinter import filedialog
from tkinter import ttk
import os

def setup_gui():
    root = tk.Tk()
    root.title("PDF to XML")

    # Create and hide the pdf_label widget
    pdf_label = tk.Label(root, text="Example on how to use the PDF to XML converter: \n 'Convert to XML:'\n")
    pdf_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="we")
    pdf_label.grid_remove()

    # Create and hide the status_label widget
    status_label = tk.Label(root, text="No file selected")
    status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="sw")
    status_label.grid_remove()

    # Create and hide the user_text widget
    user_text = tk.Text(root, width=75, height=15, state="disabled")
    user_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    user_text.grid_remove()

    # Create the button_frame widget and configure its grid
    button_frame = tk.Frame(root)
    button_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nswe")
    for i in range(5):
        button_frame.grid_rowconfigure(i, weight=1)
    for i in range(4):
        button_frame.grid_columnconfigure(i, weight=1)

    # Create the open_button widget
    open_button = tk.Button(button_frame, text="Open", command=open_file)
    open_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # Create the convert_button widget
    convert_button = tk.Button(button_frame, text="Convert", command=convert_file)
    convert_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    # Create the save_button widget
    save_button = tk.Button(button_frame, text="Save", command=save_file)
    save_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

    # Create the clear_button widget
    clear_button = tk.Button(button_frame, text="Clear", command=lambda : clear_text(user_text))
    clear_button.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    return root, pdf_label, user_text, button_frame, open_button, status_label, clear_button, save_button

def clear_text(text_widget):
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        #text_widget.config(state="disabled")

def open_file(root, user_text, status_label, pdf_label):
    global file_path
    if not root.winfo_exists():
        return
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        user_text.grid()
        pdf_label.grid()
        user_text.config(state="normal")
        status_label.config(text="File opened: " + file_path)
        status_label.grid()
    else:
        status_label.config(text="No file selected")
        status_label.grid()

def create_loading_window(root):
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading...")

    # set the window size
    loading_window.geometry("300x100")

    loading_label = tk.Label(loading_window, text="Converting file, please wait...")
    loading_label.pack(padx=10, pady=10)
    
    progress_bar = ttk.Progressbar(loading_window, mode="determinate", length=200)
    progress_bar.pack(padx=10, pady=10)
    progress_bar.start()
    
    loading_window.update()
    return loading_window

def convert_file():
    if not root.winfo_exists():
        return
    global xml_content

    if not file_path:
        status_label.config(text="No file selected")
        status_label.grid()
        return
    
    loading_win = create_loading_window(root)

    try:
        # Call the conversion function
        user_text_content = user_text.get("1.0", tk.END)
        text = pdf_converter.convert_pdf_to_text(file_path)
        user_text.delete("1.0", tk.END)
        if text == None:
            status_label.config(text="Conversion failed")
        else:
            xml_content = pdf_converter.convert_text_to_xml(text, user_text_content)
            if xml_content is not None:
                for choice in xml_content:
                    if choice.choices[0].delta.content is not None:
                        user_text.insert(tk.END, str(choice.choices[0].delta.content))
                        loading_win.update()

        status_label.config(text="Conversion Finished")

    except Exception as e:
        status_label.config(text="An error occurred: " + str(e))
    
    finally:
        loading_win.destroy()
        user_text.config(state="disabled")

def save_file():
    if not root.winfo_exists():
        return
    
    file_path = filedialog.asksaveasfile(defaultextension=".xml", filetypes=[("XML Files", "*.xml")])
    filename = os.path.basename(file_path.name)
    xml_data = user_text.get("1.0", tk.END)
    
    if file_path is None:
        status_label.config(text="Save cancelled")
    
    else:
        try:
            pdf_converter.save_xml(xml_data, filename)
            status_label.config(text="Save successful")
            user_text.config(state="disabled")
        except Exception as e:
            print(f"An error occurred: {e}")
            status_label.config(text="Save failed")

root, pdf_label, user_text, button_frame, open_button, status_label, clear_button, save_button = setup_gui()

open_button.config(command=lambda : open_file(root, user_text, status_label, pdf_label))
clear_button.config(command=lambda : clear_text(user_text))
root.mainloop()