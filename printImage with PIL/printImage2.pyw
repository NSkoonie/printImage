#printImage2.pyw
#This program opens an image, scales it, creates an ASCII representation, and writes it to a text file.
#Written by Noah Schoonover
#This file is saved with a .pyw extension (which runs with pythonw.exe) to prevent the python console from opening when running the script.

from tkinter import *
import tkinter.filedialog as filedialog
import os.path
from PIL import Image
import math

root = Tk()                                 #creates a new tkinter window named root (this should be in a class for better practice)
root.winfo_toplevel().title("PrintImage")   #changes title of tkinter window

def checkEntries():
    #checks if: path is a file, output ends in .txt, and filename is not empty
    if (os.path.isfile(pathEntry.get())) and (outputEntry.get()[-4:] == ".txt") and (outputEntry.get()[:-4] != ""):
        root.path = pathEntry.get()             #get path from entry
        root.output = outputEntry.get()         #get output path from entry
        try:
            root.width = int(widthEntry.get())  #try to convert width entry to integer
        except ValueError:
            root.width = 80                     #sets width to 80 if width entry is not integer

        #prints image using image path, output path, image width, invert boolean, and stretch boolean
        printImage(root.path, root.output, root.width, root.invert.get(), root.stretch.get())

def browse():
    #get a path from a file dialog, accepting .jpg and .png
    root.path =  filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Image Types",("*.jpg","*.png")),("all files","*.*")))
    if os.path.isfile(root.path):   #if a file is selected, sets entry to selected path
        pathEntry.delete(0,END)
        pathEntry.insert(0,root.path)
        root.output = root.path.split('.')[0] + '.txt'      #splits path at '.', keeps the part before the '.', then adds '.txt'
        outputEntry.delete(0,END)
        outputEntry.insert(0,root.output)                   #sets entry to output path

#Create widgets
    #rows 0 & 1
Label(root, text="This program prints an image in ASCII").grid(row=0,column=0,pady=10,columnspan=2)
Label(root, text="Written by Noah Schoonover").grid(row=1,column=0,pady=10,columnspan=2)
    #row 2
Label(root, text="Image:").grid(row=2,column=0,padx=10,pady=10)
pathEntry = Entry(root, width=100)
pathEntry.grid(row=2,column=1)
Button(root, text="Print", command=checkEntries).grid(row=2,column=2,padx=5)
Button(root, text="Browse", command=browse).grid(row=2,column=3,padx=5)
    #row 3
Label(root, text="Output:").grid(row=3,column=0,padx=10,pady=10)
outputEntry = Entry(root, width=100)
outputEntry.grid(row=3,column=1)
    #row 4
Label(root, text="Output must be a .txt file.  Do not specify directory to output in the script directory.").grid(row=4,column=1,pady=5)
    #row 5
Label(root, text="Width:").grid(row=5,column=0,padx=10,pady=10)
widthEntry = Entry(root, width="20")
widthEntry.insert(0,"80")
widthEntry.grid(row=5,column=1,sticky=W)
root.invert = BooleanVar()
Checkbutton(root, text="Invert", onvalue=True, offvalue=False, variable=root.invert).grid(row=5,column=1)
root.stretch = BooleanVar()
stretchCheckbutton = Checkbutton(root, text="Double Characters? (recommended)", onvalue=True, offvalue=False, variable=root.stretch)
stretchCheckbutton.grid(row=5,column=1,sticky=E)
stretchCheckbutton.select()     #checks the box by default
#end of create widgets

#printimage function handles image scaling, charset, stretch, output, and opening the output
def printImage(path, output, width, invert, stretch):
    
    printWidth = width
    
    if stretch:
        printHScale = 2
    else:
        printHScale = 1
        
    if invert:
        charSet = ['#', '8', '/', '*', '.', ' ']
    else:
        charSet = [' ', '.', '*', '/', '8', '#']
        
    rangeWidth = math.floor(255 / (len(charSet)) + 1)   #determines range for each character (255 / number-of-characters + 1)
                                                        #the '+ 1' prevents index value from being out of range

    img = Image.open(path, 'r').convert('L')            #open image and convert to grayscale
    width, height = img.size                            #get image width and height

    if width != printWidth:                             #scale image
        scaleFactor = printWidth / width
        rw = math.floor(width * scaleFactor)
        rh = math.floor(height * scaleFactor)
        rsize = (rw, rh)
        img = img.resize(rsize)
        width, height = img.size                        #get new width and height

    pixel_values =  list(img.getdata())                 #gets a list of values. sometimes this is a list of integers (grayscale) or tuples (RGB)

    if (type(pixel_values[0]) == list) or (type(pixel_values[0]) == tuple):         #checks if the list contains tuples
        pixel_values = [x[0] for x in pixel_values]                                 #strips first value from every tuple (for grayscale, RGB are equivalent)
        
    char_values = [charSet[math.floor(pixel_value / rangeWidth)]                    #create character list for image by dividing every pixel value by the range
                   for pixel_value in pixel_values]

    char_val_str = ''.join(char_values)                 #join the list into a string

    if printHScale != 1:
        stretch_char_val_str = ''
        for char in char_val_str:                                   #for every character in the character string,
            for x in range(printHScale):                            #and for the size of the stretch value,
                stretch_char_val_str = stretch_char_val_str + char  #add the indexed character
        char_val_str = stretch_char_val_str                         #then set the character string to that new string

    ascii_img = [char_val_str[index: index + (width * printHScale)] for index in        #creates a matrix from the character string
                 range(0, len(char_val_str), (width * printHScale))]                    #by separating it into rows

    ascii_img_str = '\n'.join(ascii_img)                                                #then rejoins the matrix into a string with line breaks after each row

    gotPath = False
    while not gotPath:
        try:
            with open(output, 'x+') as f:                   #creates new text file at given output path, throws error if it exists
                f.write(ascii_img_str)                      #writes image string to file
                gotPath = True                              #discontinues loop
        except FileExistsError:
            output = output.split('.')[0] + '(1).txt'       #adds '(1)' to the file path if the path already exists, keeps doing so until path doesn't exist

    os.system("notepad.exe " + output)      #open the output file with notepad

root.mainloop()     #run tkinter system, required when not running through IDLE
