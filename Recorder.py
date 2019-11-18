from armich import*
import datetime
import serial, time
try:
    arduino = serial.Serial("COM9", 9600)
    print("Connect")
    time.sleep(1)
    print("ready")
except:
    print("can't connect")
puntos,distancias,angulos,angulos2,joints1,joints2 = [],[],[],[],[],[]
pointsRecorded=[]
colorsRecorded=[]
allPoints=[]
rojo,azul,verde,negro,amarillo = (0,0,255),(255,0,0),(0,255,0),(0,0,0),(0,255,255)
freq = 20
wait = 1/freq
mask = readHSV()
robot = readArms()
global arms
arms = robot.makeArm()
print(arms)
stateColor = 1
initialColor = 0
blink_move = False
start,canWrite = False, False
radio = 5
coordInit = arms[6]

#print(coordInit)
tones = mask.makeMask()
longitud_brazo = 160

#video = cv2.VideoCapture("bolaVerde.wmv")
camaraLap = 0
camaraUsb = 1
video = cv2.VideoCapture(camaraUsb)
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
        _,realPoint,armLeft,armRight,posLeft,posRight=da.workZone(POI)
        message = da.workZoneColor(coordInit, da.grisaceo, da.grisaceo)
        da.circleState(stateColor)

        if cv2.waitKey(1) & 0xFF == ord('z'):
            initialColor = 0
        if cv2.waitKey(1) & 0xFF == ord('x'):
            initialColor = 1
        if cv2.waitKey(1) & 0xFF == ord('c'):
            initialColor = 2
        if cv2.waitKey(1) & 0xFF == ord('a'):
            blink_move = not blink_move
        if blink_move:
            # cv2.putText(fondo, "Follow: ON", (10, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.5, azul, lineType=cv2.LINE_AA)
            cv2.circle(da.bgr, da.aux2real([-270, 220]), int(10), da.verde, -1, cv2.LINE_AA)
            armLeft = int(armLeft)
            armRight = int(armRight)
            salida = "2," + str(armRight) + "," + str(armLeft)
            cv2.putText(fondo, salida, (10, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.5, azul, lineType=cv2.LINE_AA)
            startTime = time.time()
            elapsed = time.time() - startTime
            if elapsed <= wait:
                time.sleep(wait - elapsed)
            print(salida)
            try:
                arduino.write((str(salida) + "\n").encode('ascii'))
            except:
                print("can't send")

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
            results = [realPoint[0], realPoint[1], posLeft[0], posLeft[1], armLeft, posRight[0], posRight[1], armRight]
            allPoints.append(results)
            colorsRecorded.append(initialColor)
            if cv2.waitKey(1) & 0xFF == ord('d'):
                export_file_path = filedialog.asksaveasfilename(initialdir="Trajectories", defaultextension='.npy')
                np.save(export_file_path, pointsRecorded)
                file = getNameFromDirectory(export_file_path)
                export_file_path_colors = changeWord(export_file_path, file, "Colors", "Colors/")
                np.save(export_file_path_colors, colorsRecorded)
                name = getNameFromDirectory(export_file_path)
                directorio = "Trajectories/Trajectories Public/" + name + ".csv"
                pd.DataFrame(allPoints).to_csv(directorio,header=None)

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
            stateColor = 6
        if stateColor == 6:
            print("paso 6")
            cv2.destroyWindow("remake")
            name = getNameFromDirectory(export_file_path)
            directorio = "images/snapshot/" + name + ".png"
            cv2.imwrite(directorio, remake)


            dict = {"arm_a": [pix2por(arms[0])],
                    "arm_b": [pix2por(arms[1])],
                    "scale": [arms[2]],
                    "distance": [pix2por(arms[3])],
                    "UL": [pix2por(arms[4])],
                    "LL": [pix2por(arms[5])],
                    "ICX": [pix2por(arms[6][0])],
                    "ICY": [pix2por(arms[6][1])]
                    }
            data = pd.DataFrame(dict)
            print(data)
            dirConfig = "Trajectories/configs/" + name + "_Config.csv"
            data.to_csv(dirConfig, index=None, header=True)

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