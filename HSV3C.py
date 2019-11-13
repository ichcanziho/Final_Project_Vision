'''
#-Numpy is the library that allows matrix operations to be used to make binarized masks
Once the HSV min and max values are defined.

#-cv2 openCV is the main library that allows you to do all the vision analysis by computer

#-tkinter is the visual environment library for python GUI that allows you to create windows
     It is also used to access "filedialog" and to save or select files from the windows browser

#-Pill is the library that allows you to create buttons to add to tkinter windows

#-Pandas is the library to make DataFrames and be able to read or save them in CSV format
'''

import numpy as np
import cv2
import tkinter as tk
from tkinter import Label
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import pandas as pd
datahsv = pd.read_csv("calibrations/colors/current/current.csv")

hMin = [datahsv.hMin[0],datahsv.hMin[1],datahsv.hMin[2],0]
hMax = [datahsv.hMax[0],datahsv.hMax[1],datahsv.hMax[2],0]
sMin = [datahsv.sMin[0],datahsv.sMin[1],datahsv.sMin[2],0]
sMax = [datahsv.sMax[0],datahsv.sMax[1],datahsv.sMax[2],0]
vMin = [datahsv.vMin[0],datahsv.vMin[1],datahsv.vMin[2],0]
vMax = [datahsv.vMax[0],datahsv.vMax[1],datahsv.vMax[2],0]

# initialize a new tkinter window at a certain position on the screen + 500, + 400
window = tk.Tk()
#the "final" flag indicates if the window is open or not, and I create a "cap" object to capture video
window.geometry("+500+400")
final = True
lbMascara = "Mask 1"
intMascara = 1
cap = cv2.VideoCapture(0)
#cap2 = cv2.VideoCapture(1)
# sliders or bars that are created using openCV "createTrackbar" need a call to a function to do something
#in this case the "nothing" function only occupies "pass" to indicate that the function is null
def nothing(x):
    pass
#make bars is the main function that will be responsible for drawing the HSV calibration bars so that the user can
#modify the values at your disposal, these sliders are created in the window "image" an openCV window not of tkinter
# By default when initializing the program, the last configuration used by the user that has been successful is loaded
# so you don't have to be calibrating all the time
#this is done by opening the current.csv file with pandas and assigning its value to the default value at which the bar starts
def makeBars():
    datahsv = pd.read_csv("calibrations/colors/current/current.csv")
    cv2.namedWindow('image')
    cv2.createTrackbar('Hue Min', 'image', datahsv.hMin[0], 255, nothing) #255 it's the maximum value that the bars are allowed to reach
    cv2.createTrackbar('Hue Max', 'image', datahsv.hMax[0], 255, nothing)
    cv2.createTrackbar('Sat Min', 'image', datahsv.sMin[0], 255, nothing)
    cv2.createTrackbar('Sat Max', 'image', datahsv.sMax[0], 255, nothing)
    cv2.createTrackbar('Val Min', 'image', datahsv.vMin[0], 255, nothing)
    cv2.createTrackbar('Val Max', 'image', datahsv.vMax[0], 255, nothing)
#the "use" function allows you to directly occupy the configuration that is currently available without saving the profile
#like a new document, only what is registered in USE will be what is loaded at the time of starting a new session
def use():
    global hMin, hMax, sMin, sMax, vMin, vMax
    dict = {"hMin": [hMin[0], hMin[1], hMin[2]],
            "hMax": [hMax[0], hMax[1], hMax[2]],
            "sMin": [sMin[0], sMin[1], sMin[2]],
            "sMax": [sMax[0], sMax[1], sMax[2]],
            "vMin": [vMin[0], vMin[1], vMin[2]],
            "vMax": [vMax[0], vMax[1], vMax[2]]
            }
    data = pd.DataFrame(dict)
    print(data)
    data.to_csv("calibrations/colors/current/current.csv", index=None, header=True)
#as its name indicates the "SAVE" function allows the user to save the color segmentation profile in a CSV file
#where the user can choose which path to save the file as well as what its name will be, using the function
# filedialog.asksaveasfilename () of tkinter
def save():
    global hMin,hMax,sMin,sMax,vMin,vMax
    dict = {"hMin": [hMin[0],hMin[1],hMin[2]],
            "hMax":[hMax[0],hMax[1],hMax[2]],
            "sMin": [sMin[0],sMin[1],sMin[2]],
            "sMax":[sMax[0],sMax[1],sMax[2]],
            "vMin":[vMin[0],vMin[1],vMin[2]],
            "vMax":[vMax[0],vMax[1],vMax[2]]
            }
    data = pd.DataFrame(dict)
    print(data)
    export_file_path = filedialog.asksaveasfilename(initialdir ="calibrations/colors/user profile",defaultextension='.csv')
    data.to_csv(export_file_path, index=None, header=True)
#default returns all the sliders values to their initial default position, these values can be modified
#in the default.csv file
def default():
    datahsv = pd.read_csv("default.csv")
    cv2.setTrackbarPos('Hue Min', 'image', datahsv.hMin[0])
    cv2.setTrackbarPos('Hue Max', 'image', datahsv.hMax[0])
    cv2.setTrackbarPos('Sat Min', 'image', datahsv.sMin[0])
    cv2.setTrackbarPos('Sat Max', 'image', datahsv.sMax[0])
    cv2.setTrackbarPos('Val Min', 'image', datahsv.vMin[0])
    cv2.setTrackbarPos('Val Max', 'image', datahsv.vMax[0])
#as its name indicates "load" loads a CSV file to occupy that masking profile in the same way it uses
# filedialog.askopenfilename () of tikinter to occupy the windows file explorer
def load():
    global hMin, hMax, sMin, sMax, vMin, vMax
    open_file = filedialog.askopenfilename(initialdir ="calibrations/colors/user profile")
    datahsv = pd.read_csv(open_file)
    cv2.setTrackbarPos('Hue Min', 'image', datahsv.hMin[0])
    cv2.setTrackbarPos('Hue Max', 'image', datahsv.hMax[0])
    cv2.setTrackbarPos('Sat Min', 'image', datahsv.sMin[0])
    cv2.setTrackbarPos('Sat Max', 'image', datahsv.sMax[0])
    cv2.setTrackbarPos('Val Min', 'image', datahsv.vMin[0])
    cv2.setTrackbarPos('Val Max', 'image', datahsv.vMax[0])
    hMin[0] = datahsv.hMin[0]
    hMax[0] = datahsv.hMax[0]
    sMin[0] = datahsv.sMin[0]
    sMax[0] = datahsv.sMax[0]
    vMin[0] = datahsv.vMin[0]
    vMax[0] = datahsv.vMax[0]

    hMin[1] = datahsv.hMin[1]
    hMax[1] = datahsv.hMax[1]
    sMin[1] = datahsv.sMin[1]
    sMax[1] = datahsv.sMax[1]
    vMin[1] = datahsv.vMin[1]
    vMax[1] = datahsv.vMax[1]

    hMin[2] = datahsv.hMin[2]
    hMax[2] = datahsv.hMax[2]
    sMin[2] = datahsv.sMin[2]
    sMax[2] = datahsv.sMax[2]
    vMin[2] = datahsv.vMin[2]
    vMax[2] = datahsv.vMax[2]
# the "exit" function closes all open windows and ends the program this is achieved by passing the "final" flag
#a its false state, which allows it to exit an infinite loop, this will be explained later
def exit():
    global final
    final = False
    cv2.destroyAllWindows()
# the function "show_frame" is responsible for drawing on screen what the webcam detects as well as creating a new window
# to show the mask that is created in real time when moving the sliders, likewise ask for the "final" flag
# to know if the "exit" button has been pressed or not
def next():
    global hMin, hMax, sMin, sMax, vMin, vMax
    global lbMascara,intMascara

    if intMascara ==1:
        hMin[0] = cv2.getTrackbarPos('Hue Min', 'image')
        hMax[0] = cv2.getTrackbarPos('Hue Max', 'image')
        sMin[0] = cv2.getTrackbarPos('Sat Min', 'image')
        sMax[0] = cv2.getTrackbarPos('Sat Max', 'image')
        vMin[0] = cv2.getTrackbarPos('Val Min', 'image')
        vMax[0] = cv2.getTrackbarPos('Val Max', 'image')
    elif intMascara ==2:
        hMin[1] = cv2.getTrackbarPos('Hue Min', 'image')
        hMax[1] = cv2.getTrackbarPos('Hue Max', 'image')
        sMin[1] = cv2.getTrackbarPos('Sat Min', 'image')
        sMax[1] = cv2.getTrackbarPos('Sat Max', 'image')
        vMin[1] = cv2.getTrackbarPos('Val Min', 'image')
        vMax[1] = cv2.getTrackbarPos('Val Max', 'image')
    elif intMascara ==3:
        hMin[2] = cv2.getTrackbarPos('Hue Min', 'image')
        hMax[2] = cv2.getTrackbarPos('Hue Max', 'image')
        sMin[2] = cv2.getTrackbarPos('Sat Min', 'image')
        sMax[2] = cv2.getTrackbarPos('Sat Max', 'image')
        vMin[2] = cv2.getTrackbarPos('Val Min', 'image')
        vMax[2] = cv2.getTrackbarPos('Val Max', 'image')

    if (intMascara<4):
        intMascara += 1
    else:
        intMascara = 3
    if intMascara == 4:
        lbMascara = "Final Mask"
    else:
        lbMascara = "Mask "+str(intMascara)
    cv2.setTrackbarPos('Hue Min', 'image', hMin[intMascara - 1])
    cv2.setTrackbarPos('Hue Max', 'image', hMax[intMascara - 1])
    cv2.setTrackbarPos('Sat Min', 'image', sMin[intMascara - 1])
    cv2.setTrackbarPos('Sat Max', 'image', sMax[intMascara - 1])
    cv2.setTrackbarPos('Val Min', 'image', vMin[intMascara - 1])
    cv2.setTrackbarPos('Val Max', 'image', vMax[intMascara - 1])

def prev():
    global  lbMascara,intMascara
    if (intMascara>1):
        intMascara -= 1
    else:
        intMascara = 1

    lbMascara = "Mask " + str(intMascara)
    cv2.setTrackbarPos('Hue Min', 'image', hMin[intMascara - 1])
    cv2.setTrackbarPos('Hue Max', 'image', hMax[intMascara - 1])
    cv2.setTrackbarPos('Sat Min', 'image', sMin[intMascara - 1])
    cv2.setTrackbarPos('Sat Max', 'image', sMax[intMascara - 1])
    cv2.setTrackbarPos('Val Min', 'image', vMin[intMascara - 1])
    cv2.setTrackbarPos('Val Max', 'image', vMax[intMascara - 1])

def show_frame():
    global final
    global hMin, hMax, sMin, sMax, vMin, vMax
    global lbMascara, intMascara
    #each frame recorded by the webcam is analyzed
    _, frame = cap.read()
    #_,fr2 = cap2.read()
    #fr2= cv2.flip(fr2,1)
    #fr2 = cv2.resize(fr2, (320, 240))
    #this turns to make your visualization more natural
    frame = cv2.flip(frame, 1)
    #its size is modified to make the window smaller
    frame = cv2.resize(frame,(320,240))
    # change the way of interpreting color from BGR to HSV and save it in a new object called "hsv"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if intMascara ==4:
        
        lower1 = np.array([hMin[0], sMin[0], vMin[0]])
        upper1 = np.array([hMax[0], sMax[0], vMax[0]])

        lower2 = np.array([hMin[1], sMin[1], vMin[1]])
        upper2 = np.array([hMax[1], sMax[1], vMax[1]])

        lower3 = np.array([hMin[2], sMin[2], vMin[2]])
        upper3 = np.array([hMax[2], sMax[2], vMax[2]])

        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask3 = cv2.inRange(hsv, lower3, upper3)

        binarize = cv2.add(mask1, mask2)
        binarize = cv2.add(binarize, mask3)

    else:

        lower = np.array([cv2.getTrackbarPos('Hue Min', 'image'),
                          cv2.getTrackbarPos('Sat Min', 'image'),
                          cv2.getTrackbarPos('Val Min', 'image')])
        upper = np.array([cv2.getTrackbarPos('Hue Max', 'image'),
                          cv2.getTrackbarPos('Sat Max', 'image'),
                          cv2.getTrackbarPos('Val Max', 'image')])

        binarize = cv2.inRange(hsv, lower, upper)

    # a mask is created that binarizes the image from the previously established ranges

    # The windows with the original box and the already binarized box are shown as well as the window with the sliders
    # these windows are drawn at a certain screen position

    cv2.putText(frame, lbMascara, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), lineType=cv2.LINE_AA)

    cv2.imshow("original",frame)
    #cv2.imshow("cam2", fr2)
    cv2.moveWindow("original",200,100)
    cv2.imshow("masked", binarize)
    cv2.moveWindow("masked", 540, 100)
    cv2.moveWindow("image", 880, 100)
    # If the "final" flag continues in True it is because the "exit" button has not been pressed and therefore executes again
    # show_frame function after 10ms this is done recursively so that show_frame is always updated
    # No need to use a while cycle
    if final == True:
        window.after(10, show_frame)
    # If the "exit" button was pressed then "final" is false, and closes all the windows of cv2 and destroys the sliders window
    else:
        cv2.destroyAllWindows()
        window.destroy()
#assign the "default, Save, Load, Use this Set, Exit" buttons to their corresponding functions described above

btn_default=tk.Button(window, text="Default", width=50, command=default)
btn_default.pack(anchor=tk.CENTER, expand=True)

btn_save=tk.Button(window, text="Save", width=50, command=save)
btn_save.pack(anchor=tk.CENTER, expand=True)

btn_load=tk.Button(window, text="Load", width=50, command=load)
btn_load.pack(anchor=tk.CENTER, expand=True)

btn_use=tk.Button(window, text="Use this set", width=50, command=use)
btn_use.pack(anchor=tk.CENTER, expand=True)

btn_exit=tk.Button(window, text="Exit", width=50, command=exit)
btn_exit.pack(anchor=tk.CENTER, expand=True)
btn_next=tk.Button(window, text="Next", width=50, command=next)
btn_next.pack(anchor=tk.CENTER, expand=True)
btn_prev=tk.Button(window, text="Prev", width=50, command=prev)
btn_prev.pack(anchor=tk.CENTER, expand=True)

# the function that draws the HSV bars is called
makeBars()
#frame, binarize and image windows are drawn on the screen
show_frame()
# the code starts the GUI and iterates indefinitely
window.mainloop()