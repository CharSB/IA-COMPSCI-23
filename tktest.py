import os
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
from zipfile import ZipFile

# IMAGE FILE EXTENSIONS
img_extensions = ['.jpg','.jpeg','.png','.heif']
# Last retrived File
lastFile = ""

def extract_compare(zip_address):
    file_name, file_extension = os.path.splitext(zip_address)
    if(file_extension == '.zip'):
        # VALID ZIP FILE
        with ZipFile(zip_address, 'r') as zip:
            # printing all the contents of the zip file
            # file.printdir()
            zip_files = zip.namelist() # list of all the file names :D
            imgs = [] #empty list to store VALID files we want to extract
            for file in zip_files:
                file_name, file_extension = os.path.splitext(file)
                if(file_extension in img_extensions):
                    imgs.append(file)
                    zip.extract(file,path='store') # We store all the images in a temporary space called store
            
    else:
        print("That Ain't a ZIP buddy")

def get_store():
    file = open(os.listdir('store')[0], 'rb')
    return file

root = Tk()
root.title("Open a file")

def select_file():
    filetypes = (
        ('zip files', '*.zip'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/Users/noah/IA-COMPSCI-23',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )
    extract_compare(filename)

    # Try to get the dir that the file was taken from
    dir = ""
    split = filename.split('/')
    for i in range(0, len(split)-1):
        dir += split[i] + "/"

    print(filename)
    print(dir)
    lastFile = dir
    

def save_file(path=lastFile):
    file = filedialog.asksaveasfile(
        initialdir=path,
        defaultextension='.jpg'
        )

    if file is None:
        return

open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)
open_button.pack(expand=True)

save_button = ttk.Button(
    root,
    text='save',
    command=save_file
)
save_button.pack(expand=True)


Button(root, text="Quit", command=root.destroy).pack()

root.mainloop()