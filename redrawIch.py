from armich import *
import time as TIME
robot = readArms()
arms = robot.makeArm()
lastTime = -1
currentTime = 0
moveChido = False
moveUp, moveDown,pintar = True, False,True
datos = [[100,100]]
def makeSliders():
    cv2.namedWindow(ventana)
    cv2.createTrackbar('Time', ventana, 0, 100, nothing)

def nothing(x):
    pass

def openFile():
    global  datos
    open_file = filedialog.askopenfilename()
    datos = np.load(open_file)


def play():
    fondo = cv2.imread("blanco.png")
    ED = EasyDraw(fondo, arms)
    ED.drawFrame()
    paso = round(len(datos)/100)
    cuentas = 0
    time = cv2.getTrackbarPos('Time', ventana)
    time = round((time * len(datos)) / 100)
    print(time)
    for dato in range(len(datos)):
        #fondo = cv2.imread("blanco.png")

        if dato % paso ==0:
            cuentas+=1
        cv2.setTrackbarPos('Time', ventana, cuentas)
        ED.getPoint(3, ED.morado, datos[dato])
        cv2.imshow(ventana, fondo)
        cv2.waitKey(10)

def motion():
    fondo = cv2.imread("blanco.png")
    ED = EasyDraw(fondo, arms)
    ED.drawFrame()
    paso = round(len(datos)/100)
    cuentas = 0
    time = cv2.getTrackbarPos('Time', ventana)
    time = round((time * len(datos)) / 100)
    print(time)
    for dato in range(len(datos)):
        fondo = cv2.imread("blanco.png")
        ED = EasyDraw(fondo, arms)
        ED.drawFrame()
        if dato % paso ==0:
            cuentas+=1
        cv2.setTrackbarPos('Time', ventana, cuentas)
        ED.drawArmsVideo(datos[dato])
        cv2.imshow(ventana, fondo)
        cv2.waitKey(10)

def update():
    global lastTime,currentTime,moveChido,pintar
    global moveUp, moveDown
    len(datos)
    #fondo = cv2.imread("blanco.png")

    ED = EasyDraw(fondo, arms)

    time = cv2.getTrackbarPos('Time', ventana)
    time = round((time * len(datos))/100)
    #ED.getPoint(3, ED.morado, datos[time])

    if time != currentTime:
        lastTime = time
        moveChido = True
        #print("movimiento")
    else:
        moveChido = False

    if moveChido:
        if lastTime > currentTime:
            print("derecha")
            for i in range(currentTime,lastTime+1):
                ED.getPoint(3, ED.morado, datos[i])


            pintar =True
        elif lastTime < currentTime:
            print("izquierda")
            pintar = False
            for e in range(lastTime,currentTime+1):
                ED.getPoint(5, ED.blanco, datos[e])
    else:
        if pintar:
            ED.getPoint(3, ED.morado, datos[time])
        else:
            ED.getPoint(5, ED.blanco, datos[time])

    if time == len(datos):
        time = time-1

    #cv2.putText(fondo, str(time), (10, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ED.azul, lineType=cv2.LINE_AA)
    ED.drawFrame()
    cv2.imshow(ventana, fondo)
    currentTime = time
    window.after(1, update)

if __name__ == "__main__":
    fondo = cv2.imread("blanco.png")
    ED = EasyDraw(fondo,arms)
    #datos = np.load("pipe.npy")
    window = tk.Tk()
    window.title("Options")
    window.minsize(250, 150)
    window.geometry("+300+200")
    bPlayPath = ttk.Button(window, text="Play Trajectory", command=play).grid(row=1, column=0)
    bPlayArm = ttk.Button(window, text="Play motion", command=motion).grid(row=2, column=0)
    bOpen = ttk.Button(window, text="Open analysis", command=openFile).grid(row=3, column=0)

    ventana = "Recorder"
    makeSliders()
    update()


    window.mainloop()
