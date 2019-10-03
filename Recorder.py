from armich import*
puntos,distancias,angulos,angulos2,joints1,joints2 = [],[],[],[],[],[]
pointsRecorded=[]
colorsRecorded=[]
mask = readHSV()
robot = readArms()
arms = robot.makeArm()
stateColor = 1
initialColor = 0
start,canWrite = False, False
radio = 5
coordInit = arms[6]

print(coordInit)
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
        ED = EasyDraw(fondo, arms)
        bin = da.setMask(tones)
        da.getColor(bin)
        da.drawFrame()
        POI=da.getPOI()
        _,realPoint=da.workZone(POI)
        message = da.workZoneColor(coordInit, da.grisaceo, da.grisaceo)
        da.circleState(stateColor)

        if cv2.waitKey(1) & 0xFF == ord('z'):
            initialColor = 0
        if cv2.waitKey(1) & 0xFF == ord('x'):
            initialColor = 1
        if cv2.waitKey(1) & 0xFF == ord('c'):
            initialColor = 2

        if initialColor == 0:
            ED.getPoint(15, ED.morado, realPoint)
        elif initialColor == 1:
            ED.getPoint(15, ED.rojo, realPoint)
        else:
            ED.getPoint(15, ED.verde, realPoint)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            print("picado")
            if stateColor == 3:
                stateColor = 4
        if stateColor == 4:
            #pointsRecorded.append(realPoint)
            #if cv2.waitKey(1) & 0xFF == ord('d'):
            #    print("dejado")
            #    export_file_path = filedialog.asksaveasfilename(initialdir ="Trajectories",defaultextension='.npy')
            #    np.save(export_file_path, pointsRecorded)
            #    stateColor = 5
            pointsRecorded.append(realPoint)
            colorsRecorded.append(initialColor)
            if cv2.waitKey(1) & 0xFF == ord('d'):
                export_file_path = filedialog.asksaveasfilename(initialdir="Trajectories", defaultextension='.npy')
                np.save(export_file_path, pointsRecorded)
                file = getNameFromDirectory(export_file_path)
                export_file_path_colors = changeWord(export_file_path, file, "Colors", "Colors/")
                np.save(export_file_path_colors, colorsRecorded)
                stateColor = 5
        if stateColor == 5:
            remake = cv2.imread("blanco.png")
            robot = readArms()
            arms = robot.makeArm()
            ED = EasyDraw(remake, arms)
            ED.drawFrame()
            for dato in range(len(pointsRecorded)):
                ED.getPoint(3, ED.morado, pointsRecorded[dato])
                cv2.imshow("remake", remake)
            name = getNameFromDirectory(export_file_path)
            directorio = "images/snapshot/" + name + ".png"
            cv2.imwrite(directorio, remake)
            stateColor = 1

        if not start:
            if not canWrite:
                message = da.workZoneColor(coordInit, da.grisaceo, da.grisaceo)
                cA = np.array(POI)
                cS = np.array(coordInit)
                if stateColor != 4 and stateColor != 5:
                    if abs(cA[0] - cS[0]) <= radio and abs(cA[1] - cS[1]) <= radio:
                        stateColor = 3
                    else:
                        stateColor = 1

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
        #cv2.imshow("mask", bin)
video.release()
cv2.destroyAllWindows()