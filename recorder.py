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
lastPOI = [0,0]
while(1):
    try:
        _, fondo = video.read()
        fondo = cv2.flip(fondo, 1)
        da = DrawArm(fondo,arms,tones)
        bin = da.setMask(tones)
        da.getColor(bin)
        da.drawFrame()
        POI=da.getPOI()
        da.workZone(POI)
        cv2.imshow("Procesado",fondo)
        #cv2.imshow("mask", bin)
        #puntos.append(punto)
        lastPOI = POI
        if cv2.waitKey(20) & 0xFF == 27:
            break
    except:
        #cv2.waitKey(0)
        #break;
        POI = lastPOI
        da.drawFrame()
        da.workZone(POI)
        cv2.imshow("Procesado", fondo)
        cv2.imshow("mask", bin)
video.release()
cv2.destroyAllWindows()