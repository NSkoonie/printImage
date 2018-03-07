from PIL import Image
import math

#A black square "\u25A0"
#A white square "\u25A1"

IMG = "noah.jpg"
MAX_WIDTH = 80

HSTRETCH = 2            #Horizontal stretch

invert = True

if invert:
    CHAR_1 = " "
    CHAR_2 = "."
    CHAR_3 = "*"
    CHAR_4 = "/"
    CHAR_5 = "8"
    CHAR_6 = "#"
else:
    CHAR_1 = "#"
    CHAR_2 = "8"
    CHAR_3 = "/"
    CHAR_4 = "*"
    CHAR_5 = "."
    CHAR_6 = " "

THRESHOLD_1 = math.floor(255/6) * 1
THRESHOLD_2 = math.floor(255/6) * 2
THRESHOLD_3 = math.floor(255/6) * 3
THRESHOLD_4 = math.floor(255/6) * 4
THRESHOLD_5 = math.floor(255/6) * 5

im = Image.open(IMG, "r").convert("L")      #opens image and converts to grayscale
width, height = im.size                     #gets width and height
if width > MAX_WIDTH:
    scaleFactor = MAX_WIDTH / width               #creates scale factor
    rw = math.floor(width * scaleFactor)                #new width
    rh = math.floor(height * scaleFactor)               #new height
    rsize = (rw, rh)
    im = im.resize(rsize)
    width, height = im.size
    
IMAGE_WIDTH = width

pix_val = list(im.getdata())                        #Gets RGB for every pixel, stores in list

if (type(pix_val[0]) == int):
    single_vals = pix_val
elif (type(pix_val[0]) == list) or (type(pix_val[0]) == tuple):
    single_vals = [x[0] for x in pix_val]               #Strips R value from every set in pix_val
                                                        #in grayscale images, RGB are equivalent
else:
    print("error")
    
def getSymbol(val):
    if val <= THRESHOLD_1:
        return CHAR_1
    elif val <= THRESHOLD_2:
        return CHAR_2
    elif val <= THRESHOLD_3:
        return CHAR_3
    elif val <= THRESHOLD_4:
        return CHAR_4
    elif val <= THRESHOLD_5:
        return CHAR_5
    else:
        return CHAR_6

    
def printChar(breakLine):
    if breakLine == "doBreakLine":
        print(getSymbol(single_vals[x]))            #Prints character and breaks line
    else:
        print(getSymbol(single_vals[x]), end='')    #Prints character and does not break line

for x in range(len(single_vals)):
    for z in range(HSTRETCH - 1):                   #This just prints the character as many
        printChar("")                               #times as specified in HSTRETCH
        
    if ((x + 1) % IMAGE_WIDTH == 0):
        printChar("doBreakLine")
    else:
        printChar("")    

u = input("exit?")
