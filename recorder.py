from armich import*
puntos,distancias,angulos,angulos2,joints1,joints2 = [],[],[],[],[],[]
mask = readHSV()
robot = readArms()
arms = robot.makeArm()
tones = mask.makeMask()
longitud_brazo = 160

#video = cv2.VideoCapture("bolaVerde.wmv")
video = cv2.VideoCapture(0)
_, fondo = video.read()

while(1):
    try:
        _, fondo = video.read()
        da = DrawArm(fondo,arms)
        da.drawFrame()
        #db = DibujarBrazo(tonos, fondo, longitud_brazo)
        #db.crearMarco()
        #punto, distancia, angulo, joint1, joint2, angulo2 = db.getData()
        cv2.imshow("Procesado",fondo)
        #puntos.append(punto)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    except:
        cv2.waitKey(0)
        break;
video.release()
cv2.destroyAllWindows()