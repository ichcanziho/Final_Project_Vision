from armich import *
from PIL import  Image,ImageTk
from tkinter import Label
import time as TIME
import serial
try:
    arduino = serial.Serial("COM9", 9600)
    print("Connect")
    TIME.sleep(1)
    print("ready")
except:
    print("can't connect")
robot = readArms()
arms = robot.makeArmDir("Trajectories/configs/default_Config.csv")
lastTime = -1
currentTime = 0
moveChido = False
moveUp, moveDown,pintar = True, False,True
datos = [[0,0]]
datosLimpioColor = [0]
def makeSliders():
    cv2.namedWindow(ventana)
    cv2.createTrackbar('Time', ventana, 0, 99, nothing)

def nothing(x):
    pass

def openFile():
    global  datos,datosLimpioColor,arms,dataPosition
    open_file = filedialog.askopenfilename(initialdir ="Trajectories")
    datos = np.load(open_file)

    file = getNameFromDirectory(open_file)
    import_file_path_colors = changeWord(open_file, file, "Colors","Colors/")

    datosColor = np.load(import_file_path_colors)
    datosLimpioColor = datosColor.tolist()

    nf = "images/snapshot/"+file+".png"
    im = Image.open(nf)
    resized = im.resize((int(640/4), int(480/4)), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(resized)
    myvar = Label(window, image=tkimage)
    myvar.image = tkimage
    myvar.grid(row=2, column=2)
    config = "Trajectories/configs/"+file+"_Config.csv"
    arms = robot.makeArmDir(config)
    config = "Trajectories/Trajectories Public/" + file + ".csv"
    dataPosition = pd.read_csv(config)

def sendFile():
    global dataPosition
    dataPosition.columns=["iter","px","py","ax","ay","angle1","bx","by","angle2"]
    #dataPosition.head()
    for angle1,angle2 in zip(dataPosition["angle1"],dataPosition["angle2"]):
        salida = "2,"+str(angle2)+","+str(angle1)
        print(salida)
        TIME.sleep(0.02)
        try:
            arduino.write((str(salida) + "\n").encode('ascii'))
        except:
            print("can't send")


def play():
    fondo = cv2.imread("blanco.png")
    ED = EasyDraw(fondo, arms)
    #ED = EasyD(fondo, arms)
    ED.drawFrame()
    paso = round(len(datos)/100)
    cuentas = 0
    time = cv2.getTrackbarPos('Time', ventana)
    time = round((time * len(datos)) / 100)

    for dato in range(len(datos)):
        #fondo = cv2.imread("blanco.png")

        if dato % paso ==0:
            cuentas+=1
        cv2.setTrackbarPos('Time', ventana, cuentas)

        if datosLimpioColor[dato]==0:
            ED.getPoint(3, ED.morado, datos[dato])
        elif datosLimpioColor[dato]==1:
            ED.getPoint(3, ED.blanco, datos[dato])
        else:
            ED.getPoint(3, ED.azul, datos[dato])
        cv2.imshow(ventana, fondo)
        cv2.waitKey(10)

def motion():
    fondo = cv2.imread("blanco.png")
    ED = EasyDraw(fondo, arms)
    #ED = EasyD(fondo, arms)
    ED.drawFrame()
    paso = round(len(datos)/100)
    cuentas = 0
    time = cv2.getTrackbarPos('Time', ventana)
    time = round((time * len(datos)) / 100)
    print(time)
    for dato in range(len(datos)):
        fondo = cv2.imread("blanco.png")
        ED = EasyDraw(fondo, arms)
        #ED = EasyD(fondo, arms)
        ED.drawFrame()
        if dato % paso ==0:
            cuentas+=1
        cv2.setTrackbarPos('Time', ventana, cuentas)
        ED.drawRobot(datos[dato])
        cv2.imshow(ventana, fondo)
        cv2.waitKey(10)

def update():
    global lastTime,currentTime,moveChido,pintar
    global moveUp, moveDown
    len(datos)
    #fondo = cv2.imread("blanco.png")
    fondo = cv2.imread("blanco.png")
    ED = EasyDraw(fondo, arms)
    #ED = EasyD(fondo, arms)
    time = cv2.getTrackbarPos('Time', ventana)
    time = round((time * len(datos))/100)
    #ED.getPoint(3, ED.morado, datos[time])
    if time == len(datos):
        time = time-1
    if time != currentTime:
        lastTime = time
        moveChido = True
        #print("movimiento")
    else:
        moveChido = False

    if moveChido:
        if lastTime > currentTime:
            for i in range(currentTime,lastTime+1):
                #ED.getPoint(3, ED.morado, datos[i])
                if datosLimpioColor[i] == 0:
                    ED.getPoint(3, ED.morado, datos[i])
                elif datosLimpioColor[i] == 1:
                    ED.getPoint(3, ED.blanco, datos[i])
                else:
                    ED.getPoint(3, ED.azul, datos[i])


            pintar =True
        elif lastTime < currentTime:
            pintar = False
            for e in range(lastTime,currentTime+1):
                ED.getPoint(5, ED.blanco, datos[e])
    else:
        if pintar:
            #ED.getPoint(3, ED.morado, datos[time])
            if datosLimpioColor[time] == 0:
                ED.getPoint(3, ED.morado, datos[time])
            elif datosLimpioColor[time] == 1:
                ED.getPoint(3, ED.blanco, datos[time])
            else:
                ED.getPoint(3, ED.azul, datos[time])
        else:
            ED.getPoint(5, ED.blanco, datos[time])



    #cv2.putText(fondo, str(time), (10, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ED.azul, lineType=cv2.LINE_AA)
    ED.drawFrame()
    cv2.imshow(ventana, fondo)
    currentTime = time
    window.after(1, update)

if __name__ == "__main__":
    fondo = cv2.imread("blanco.png")
    ED = EasyDraw(fondo,arms)
    #ED = EasyD(fondo, arms)
    #datos = np.load("pipe.npy")
    window = tk.Tk()
    window.title("Options")
    window.minsize(250, 150)
    window.geometry("+300+200")
    bPlayPath = ttk.Button(window, text="Play Trajectory", command=play).grid(row=1, column=0)
    bPlayArm = ttk.Button(window, text="Play motion", command=motion).grid(row=2, column=0)
    bOpen = ttk.Button(window, text="Open analysis", command=openFile).grid(row=3, column=0)
    bSend = ttk.Button(window, text="Send to robot", command=sendFile).grid(row=4, column=0)
    ventana = "Viewer"
    makeSliders()
    update()


    window.mainloop()
