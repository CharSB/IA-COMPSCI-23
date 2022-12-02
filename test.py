import asyncio
from email.mime import image
import io
import glob
import os
import sys
import time
from turtle import color
from urllib import response
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from PIL import ImageDraw, ImageTk
import PIL.Image
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
# ZIP file management
from zipfile import ZipFile
#TKINTER GUI Window stuff
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo

import typing

# IMAGE FILE EXTENSIONS
img_extensions = ['.jpg','.jpeg','.png','.bmp']

# https://www.youtube.com/watch?v=H8-CckgZFzw reference

# Abstracting my KEY and ENDPOINT away from this file :D
# They are stored in a .gitignore file with the information on seperate lines
APIstuff = 'API.txt'
def setup_API(filepath):
    f = open(filepath, "r")
    read = f.read().splitlines()
    return read

credz = setup_API(APIstuff)
# This key will serve all examples in this document.
KEY = credz[0]
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = credz[1]

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# PUT IN ANY IMAGE YOU WANT!!!!! IT WORKS
image_url = 'https://www.business2community.com/wp-content/uploads/2015/10/42454567_m.jpg.jpg'

# last used directory - where the .ZIP is selected from
zip_location = ""

def retrive_images(dir):
    for path in os.listdir(dir):
        proper_path = dir + '/' + path
        imgs_to_check.append(proper_path)
    # Used to debug and confirm all files are retrieved
    # print(imgs_to_check)
    # print('got da images :D')

# Who do we want to find
target_person = 'test_images/Noah#1.jpeg'
# What images do we want to check
imgs_to_check = []
# Matched images of the target
matches = []

A4 = (3508,2480)
MIN_SIZE = (863,308)

# Taking out all of the image files
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
                    zip.extract(file,path='store/storage') # We store all the images in a temporary space called store
            
    else:
        print("That Ain't a ZIP buddy")

def zipem(f2z, dir):
    if not f2z:
        print('No Files to ZIP')
        return 
    else:
        print(dir + 'matches.zip')
        zipObj = ZipFile(dir + '/matches.zip', 'w')

        for file in f2z:
            zipObj.write(file)

        zipObj.close()

# File management at it's finest
def clear_dir(dir_path):
    files = os.listdir(dir_path)
    for file in files:
        try:
            # remove the files
            os.remove(dir_path+'/'+file)
        except:
            # here it isn't a file so it can only be a dir
            os.rmdir(dir_path+'/'+file)
    print(dir_path + ' was cleared')

# Based on EXAMPLE #4
def comparison(target_img, compare_img):

    # This is the image that we want to check
    compared_to = compare_img
    response_detected_faces = face_client.face.detect_with_stream(
        image=open(compared_to,'rb'),
        detection_model='detection_03',
        recognition_model='recognition_04'
    )

    # faces to check against
    face_ids = [ face.face_id for face in response_detected_faces]
        
    # This would be the image of the student we want to find
    # a clean image with just them is what we need to be inputed
    img_target = open(target_img, 'rb')
    response_face_target = face_client.face.detect_with_stream(
        image = img_target,
        detection_model='detection_03',
        recognition_model='recognition_04'
    )
    target_face_id = response_face_target[0].face_id

    # Now we have both our target face id,
    # And we compare it against all the face ids from face_ids
    matched_face_ids = face_client.face.find_similar(
        face_id=target_face_id,
        face_ids=face_ids
    )

    # Open the group image / one you want to check if the student is in
    # img = PIL.Image.open(open(compared_to, 'rb'))
    # draw = ImageDraw.Draw(img)

    #Flag raising for if we find a match
    matched = False

    # draw a box around all matches of the face
    for matched_face in matched_face_ids:
        for face in response_detected_faces:
            if face.face_id == matched_face.face_id:
                # rect = face.face_rectangle
                # left = rect.left
                # top = rect.top
                # right = rect.width + left
                # bottom = rect.height + top
                # draw.rectangle(((left, top), (right, bottom)), outline='green', width=5)
                matched = True
    
    # if matched == False:
    #     draw.line([(0,0),(img.size[0],img.size[1])],fill='red', width=5)

    # img.show()

    if matched:
        update_text(tgt_status, "MATCHES FOUND")
        return compare_img


# WHERE TO RUN ANY METHODS YOU MAKE :DDD What's in here is what runs
def find_matches():
    # Getting all files
    # extract_compare(tgtzip)
    # now they are in store
    
    # TO DO: Get them out of store and run 
    update_text(tgt_status, "FINDING MATCHES")
    retrive_images('store/storage')
    for img in imgs_to_check:
        print(img)
        match = comparison(target_person, img)
        if match: matches.append(match)


def download_matches():
    if matches:
            dirname = filedialog.askdirectory(
                title='Open a folder',
                initialdir=os.path.dirname(os.path.realpath(__file__)))
            print(dirname)
            zipem(matches, dirname)
            update_text(download_status, "DOWNLOADED")
    

root = Tk()
root.title("Personal Yeerbook")
root.minsize(width=MIN_SIZE[0], height=MIN_SIZE[1])

def select_zip():
    filetypes = (
        ('zip files', '*.zip'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir=os.path.dirname(os.path.realpath(__file__)),
        filetypes=filetypes)

    # Used to confirm what file you have selected
    # showinfo(
    #     title='Selected File',
    #     message=filename
    # )
    extract_compare(filename)

    # Try to get the dir that the file was taken from
    dir = ""
    split = filename.split('/')
    for i in range(0, len(split)-1):
        dir += split[i] + "/"

    print(filename)
    print(dir)
    zip_location = dir
    if filename:
        update_text(zip_status, filename)

def select_img():
    print(root.winfo_width())
    print(root.winfo_height())
    filetypes = (
        ('jpg files', '*.jpg'),
        ('jpeg files', '*.jpeg'),
        ('png files', '*.png'),
        ('heif files', '*.heif'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir=os.path.dirname(os.path.realpath(__file__)),
        filetypes=filetypes)

    # Used to confirm what file you have selected
    # showinfo(
    #     title='Selected File',
    #     message=filename
    # )

    print(filename)
    target_person = filename
    update_target(filename, target_placeholder, (750,750))
    update_text(tgt_button, "Change Target Person")

def update_target(img_path, place:Label, size:tuple):
    img = PIL.Image.open(img_path)
    img.thumbnail(size)
    imgtk=ImageTk.PhotoImage(img)
    place.configure(image=imgtk)
    place.image=imgtk

def update_text(label: typing.Union[Label, ttk.Button], text):
    label.configure(text=text)
    label.text=text

def swap_frame(close:Frame, open:Frame):
    close.grid_forget()
    open.grid(row=0, column=0, padx=5, pady=5)

def generate_template():
    swap_frame(default_frame, template_frame)
    default_frame.grid_forget()
    return "do it yourself"

def quit():
    clear_dir('store/storage')
    root.destroy()

 
# Specify Grid
Grid.rowconfigure(root,0,weight=1)
Grid.columnconfigure(root,0,weight=1)



# DEFAULT GUI 
    #region FRAMES
default_frame = LabelFrame(root, padx=5, pady=5)
default_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ESWN")

Grid.rowconfigure(default_frame,0,weight=1)
Grid.columnconfigure(default_frame,0,weight=1)

b_frame1 = LabelFrame(default_frame, padx=20, pady=10)
b_frame1.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="ESWN")

tgt_frame1 = LabelFrame(default_frame, padx=20, pady=10)
tgt_frame1.grid(row=0, column=0, padx=10, pady=10, sticky="ESWN")

Grid.rowconfigure(b_frame1,0,weight=1)
Grid.columnconfigure(b_frame1,0,weight=1)

Grid.rowconfigure(tgt_frame1,0,weight=1)
Grid.columnconfigure(tgt_frame1,0,weight=1)
    #endregion

    #region IMAGES / STATUS
target_placeholder = Label(tgt_frame1, text="[ TARGET PERSON ]")
target_placeholder.grid(row=0, column=0, padx=10, pady=10)

zip_status = Label(b_frame1, text="[ ZIP FILE ]")
zip_status.grid(row=0, column=1, padx=10, pady=10)

tgt_status = Label(b_frame1, text="[ TARGET NOT FOUND ]")
tgt_status.grid(row=2, column=1, padx=10, pady=10)

download_status = Label(b_frame1, text="[ ... ]")
download_status.grid(row=3, column=1, padx=10, pady=10)
    #endregion

    #region  BUTTONS
tgt_button = ttk.Button(
    tgt_frame1,
    text='Select a Target Person',
    command=select_img
)
tgt_button.grid(row=1, column=0, padx= 50, pady= 10)

zip_button = ttk.Button(
    b_frame1,
    text='Select target Zip',
    command=select_zip
)
zip_button.grid(row=0, column=0, padx= 50, pady= 10)

comp_button = ttk.Button(
    b_frame1,
    text='Find target in ZIP',
    command=find_matches
)
comp_button.grid(row=2, column=0, padx= 50, pady= 10)

download_button = ttk.Button(
    b_frame1,
    text='Download Matches',
    command=download_matches
)
download_button.grid(row=3, column=0, padx= 50, pady= 10)

generate_temp_button = ttk.Button(
    b_frame1,
    text='Generate Template',
    command=generate_template
)
generate_temp_button.grid(row=4, column=0, padx= 50, pady= 10)

quit_button = Button(b_frame1, text="Quit", command=quit)
quit_button.grid(row=5, column=0, padx= 50, pady= 10)


    #endregion

#TEMPLATE GUI
    #region Frames
template_frame = LabelFrame(root, padx=5, pady=5)
template_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ESWN")

Grid.rowconfigure(template_frame,0,weight=1)
Grid.columnconfigure(template_frame,0,weight=1)

layout_frame = LabelFrame(template_frame, padx=5, pady=5)
layout_frame.grid(row=0, column=0, padx=5, pady=5)

selection_frame = LabelFrame(template_frame, padx=5, pady=5)
selection_frame.grid(row=0, column=1, padx=5, pady=5)

img_frame = LabelFrame(selection_frame, padx=5, pady=5)
img_frame.grid(row=0, column=0, padx=5, pady=5)

btn_frame = LabelFrame(selection_frame, padx=5, pady=5)
btn_frame.grid(row=1, column=0, padx=5, pady=5)
    #endregion

#region IMAGES / STATUS
    #Images
img1 = Label(img_frame, text="[ ... ]")
img1.grid(row=0, column=0, padx=10, pady=10)
img2 = Label(img_frame, text="[ ... ]")
img2.grid(row=0, column=1, padx=10, pady=10)
img3 = Label(img_frame, text="[ ... ]")
img3.grid(row=0, column=2, padx=10, pady=10)

img4 = Label(img_frame, text="[ ... ]")
img4.grid(row=1, column=0, padx=10, pady=10)
img5 = Label(img_frame, text="[ ... ]")
img5.grid(row=1, column=1, padx=10, pady=10)
img6 = Label(img_frame, text="[ ... ]")
img6.grid(row=1, column=2, padx=10, pady=10)

img7 = Label(img_frame, text="[ ... ]")
img7.grid(row=2, column=0, padx=10, pady=10)
img8 = Label(img_frame, text="[ ... ]")
img8.grid(row=2, column=1, padx=10, pady=10)
img9 = Label(img_frame, text="[ ... ]")
img9.grid(row=2, column=2, padx=10, pady=10)
    #Template
template = Label(layout_frame, text="[ ... ]")
template.grid(row=0, column=0, padx=10, pady=10)
#endregion

    #region  BUTTONS
back_button = ttk.Button(
    btn_frame,
    text='Back',
    command=lambda: swap_frame(template_frame, default_frame)
)
back_button.grid(row=0, column=0, columnspan = 3,padx= 50, pady= 10)
    #endregion

swap_frame(template_frame, default_frame)
root.mainloop()

# e book for build!!!!