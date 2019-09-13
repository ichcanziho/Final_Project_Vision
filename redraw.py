import tkinter as tk
import cv2

from tkinter import ttk
from armich import *


def makeSliders():
    cv2.namedWindow(ventana)
    cv2.createTrackbar('Tiempo', ventana, 0, 100, nothing)
    cv2.createTrackbar('Inicio', ventana, 1, 99, nothing)
    cv2.createTrackbar('Final', ventana, 2, 100, nothing)


def nothing(x):
    pass


def aIzq():
    global pos_a, f_change
    if (pos_a > 0) & (pos_a <= 100):
        pos_a -= 1
    else:
        pass
    f_change = True
    update()


def aDer():
    global pos_a, f_change, datosLimpio
    # print("hola")
    if pos_a < (len(datosLimpio)):
        pos_a += 1
    else:
        pass
    f_change = True
    update()


def update():
    global f_change, f_perc, perc_s, perc_a, pos_a, datosLimpio

    if (f_change == True):
        f_change = False
        perc_s = (pos_a * 100) // len(datosLimpio)
        perc_a = perc_s
        cv2.setTrackbarPos('Tiempo', ventana, perc_s)
        drawPoint()

    elif (f_perc == True):
        f_perc = False
        pos_a = (perc_s * len(datosLimpio) // 100)
        drawPoint()

    else:
        pass

    posicion = ttk.Label(window, text=pos_a)
    posicion.grid(row=2, column=2)
    # retrieveSlider()


def drawPoint():
    global index, pos_a, datos, datosLimpio, image, ventana
    # print(pos_a)
    # draw.getPoint(5, draw.blanco)

    print(index)
    while (index < (pos_a)) & (pos_a < 100):
        index += 1
        interes = tuple(datos[index])
        draw = Redraw(image, 180, interes)
        draw.crearMarco()
        draw.getPoint(2, draw.morado)
        cv2.imshow(ventana, image)
        cv2.waitKey(5)

    while index > (pos_a):
        index -= 1
        interes = tuple(datos[index])
        draw = Redraw(image, 180, interes)
        draw.crearMarco()
        draw.getPoint(2, draw.blanco)
        cv2.imshow(ventana, image)
        cv2.waitKey(5)


def retrieveSlider():
    global datosLimpio, perc_a, perc_s, f_perc
    time_s = cv2.getTrackbarPos('Tiempo', ventana)
    start_s = cv2.getTrackbarPos('Tiempo', ventana)
    fin_s = cv2.getTrackbarPos('Tiempo', ventana)
    '''
    dic = dict({
        'Slider': [time_s, start_s, fin_s]
        })
    '''
    slider = np.array([time_s, start_s, fin_s])
    # print(dic['Tiempo'])
    # print(dic.get('Tiempo'))
    perc_s = int((time_s * len(datosLimpio)) // 100)
    if (perc_a != perc_s):
        f_perc = True
        perc_a = perc_s
        update()
    else:
        pass


def exit():
    global final
    final = False
    cv2.destroyAllWindows()


def post_main():
    retrieveSlider()
    # update()

    if final == True:
        window.after(10, post_main)
    else:
        cv2.destroyAllWindows()
        window.destroy()
    pass


#  MAIN PROGRAM
if __name__ == "__main__":
    global pos_a, datos, datosLimpio, image, f_change, f_perc, ventana, final, perc_a, perc_s, pos_a, index

    f_change = False
    pos_a = 0

    index = -1
    final = True

    f_perc = False
    perc_a = 0
    perc_s = 0

    image = cv2.imread("blanco.png")
    ventana = "Dibujar"
    cv2.imshow(ventana, image)

    window = tk.Tk()
    window.title("Botones")
    window.minsize(300, 100)

    bIzq = ttk.Button(window, text="Prev", command=aIzq).grid(row=0, column=0)
    bDer = ttk.Button(window, text="Next", command=aDer).grid(row=0, column=1)
    btn_exit = ttk.Button(window, text="Exit", command=exit).grid(row=2, column=0)
    bCut = ttk.Button(window, text="Cut", command=nothing).grid(row=1, column=0)
    # btn_exit.pack(anchor=tk.CENTER, expand=True)
    posicion = ttk.Label(window, text=pos_a)
    posicion.grid(row=1, column=2)

    # Carga datos
    datos = np.load("record1.npy")
    datosLimpio = datos.tolist()
    # print("Array size {}".format(len(datosLimpio)))

    # init
    update()
    makeSliders()
    post_main()

    # continuous running
    window.mainloop()
