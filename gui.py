from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "select a file",
                                          filetypes = (("PDF files",
                                                        "*.pdf"),
                                                        ("all files",
                                                         "*.*")))
    #label_file_explore.configure(text="file opened: "+ filename)
    return filename

# root = Tk()

# root.title("PDF to XML Converter")
# root.geometry("350x200")
# root.config(background = "white")

# label_file_explore = Label(root,
#                            text = "File Explorer")

# def button():
#     button_explore = Button(root,
#                             text = "browse files",
#                             command = browseFiles).grid(column=1, row=2)

# def Close():
#     root.destroy()

# button_exit = Button(root,
#                      text = "exit",
#                      command= Close)

# label_file_explore.grid(column = 1, row = 1)

# button()

# button_exit.grid(column = 1, row = 3)

    
# root.mainloop()