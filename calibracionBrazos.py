import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np

window = tk.Tk()
b1 = 60
b2 = 55
totalDis = b1+b2
start = False
fondo = cv2.imread("blanco.png")
rojo,azul,verde,negro,amarillo = (0,0,255),(255,0,0),(0,255,0),(0,0,0),(0,255,255)

h,w= fondo.shape[:2]
h = int( h/2)
w=int(w/2)
origenReal = (w,h)
window.title("Python Tkinter Text Box")
window.minsize(200, 100)

distancia = 100
def nothing(x):
    pass
def clickMe():
    global totalDis
    label.configure(text='Hello ' + name.get())
    totalDis= int(name.get())


label = ttk.Label(window, text="Set Lon")
label.grid(column=0, row=0)

name = tk.StringVar()
nameEntered = ttk.Entry(window, width=15, textvariable=name)
nameEntered.grid(column=0, row=1)

button = ttk.Button(window, text="Send", command=clickMe)
button.grid(column=0, row=2)
def mb():
    cv2.namedWindow('original')
    cv2.createTrackbar('Radio', 'original', 0, 100, nothing)
def makeB():
    pass



def chido():
    fondo = cv2.imread("blanco.png")
    cv2.line(fondo, (0, h), (2 * w, h), negro, 1, cv2.LINE_AA)
    cv2.line(fondo, (w, 0), (w, 2 * h), negro, 1, cv2.LINE_AA)
    cv2.circle(fondo, origenReal, 235, rojo, 1, cv2.LINE_AA)
    lb = cv2.getTrackbarPos('Radio', 'original')
    lb = int((235 * lb) / 100)
    cv2.circle(fondo, origenReal, lb, azul, 1, cv2.LINE_AA)
    cv2.putText(fondo, str(totalDis), (320, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.putText(fondo, str(totalDis), (320, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.imshow('original', fondo)
    window.after(10, chido)
    #window.after(10,mb)
mb()
makeB()
chido()
window.mainloop()