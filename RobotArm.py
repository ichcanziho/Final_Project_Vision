

from armich import*
import datetime

start = False
canWrite = False
first = False
record = False
pointsRecorded = []
stateColor = 1
coordSave = [0,0]
coord = [200,200]
int_arm_a, int_arm_b, float_scale, int_total_dis,int_upper,int_lower = 0,0,0,0,0,0
data = pd.read_csv("calibrations/arms/current/currentArm.csv")
int_arm_a = int(data.arm_a[0])
int_arm_b = int(data.arm_b[0])
float_scale = float(data.scale[0])
int_total_dis = int(data.distance[0])
int_upper = int(data.UL[0])
int_lower = int(data.LL[0])

icx = data.ICX[0]
icy = data.ICY[0]
init_Coord=[icx,icy]



def nothing(x):
    pass
def b_Use():
    global int_arm_a, int_arm_b, float_scale, int_total_dis,coordSave

    if arm_A.get() != "":
        labelA.configure(text='A = ' + arm_A.get())
        int_arm_a = int(arm_A.get())
    if arm_B.get() != "":
        labelB.configure(text='B = ' + arm_B.get())
        int_arm_b = int(arm_B.get())
    if scale.get() != "":
        labelC.configure(text='S = ' + scale.get())
        float_scale = float(scale.get())
    int_total_dis = int_arm_a + int_arm_b
    dict = {"arm_a": [int_arm_a],
            "arm_b": [int_arm_b],
            "scale": [float_scale],
            "distance": [int_total_dis],
            "UL": [cv2.getTrackbarPos('Upper', 'Draw')],
            "LL": [cv2.getTrackbarPos('Lower', 'Draw')],
            "ICX":[coordSave[0]],
            "ICY":[coordSave[1]]
            }
    data = pd.DataFrame(dict)
    print(data)
    data.to_csv("calibrations/arms/current/currentArm.csv", index=None, header=True)
def b_Save():
    global int_arm_a, int_arm_b, float_scale, int_total_dis,coordSave
    dict = {"arm_a": [int_arm_a],
            "arm_b": [int_arm_b],
            "scale": [float_scale],
            "distance": [int_total_dis],
            "UL": [cv2.getTrackbarPos('Upper', 'Draw')],
            "LL": [cv2.getTrackbarPos('Lower', 'Draw')],
            "ICX": [coordSave[0]],
            "ICY": [coordSave[1]]
            }
    data = pd.DataFrame(dict)
    print(data)
    export_file_path = filedialog.asksaveasfilename(initialdir ="calibrations/arms/user profile",defaultextension='.csv')
    data.to_csv(export_file_path, index=None, header=True)
def b_Load():
    global int_arm_a, int_arm_b, float_scale, int_total_dis,int_upper,int_lower,coordSave,init_Coord,stateColor
    stateColor = 1
    open_file = filedialog.askopenfilename(initialdir ="calibrations/arms/user profile" )
    data = pd.read_csv(open_file)
    labelA.configure(text='A = ' + str(data.arm_a[0]))
    labelB.configure(text='B = ' + str(data.arm_b[0]))
    labelC.configure(text='S = ' + str(data.scale[0]))
    int_arm_a = int(data.arm_a[0])
    int_arm_b = int(data.arm_b[0])
    float_scale = float(data.scale[0])
    int_total_dis = int(data.distance[0])
    int_upper = int(data.UL[0])
    cv2.setTrackbarPos('Upper', 'Draw', int_upper)
    int_lower = int(data.LL[0])
    cv2.setTrackbarPos('Lower', 'Draw', int_lower)
    coordSave[0] = int(data.ICX[0])
    coordSave[1] = int(data.ICY[0])
    init_Coord = coordSave
    arm_A.set(str(int_arm_a))
    arm_B.set(str(int_arm_b))
    scale.set(str(float_scale))

window = tk.Tk()

fondo = cv2.imread("blanco.png")
rojo,azul,verde,negro,amarillo = (0,0,255),(255,0,0),(0,255,0),(0,0,0),(0,255,255)

h,w= fondo.shape[:2]
h,w = int( h/2),int(w/2)
origenReal = (w,h)
window.title("Calibration")
window.minsize(300, 100)

label = ttk.Label(window, text="Set Arm A").grid(row=0)
label = ttk.Label(window, text="Set Arm B").grid(row=1)
label = ttk.Label(window, text="Scale").grid(row=2)
arm_A = tk.StringVar()
arm_B = tk.StringVar()
scale = tk.StringVar()
arm_a_Entered = ttk.Entry(window, width=15, textvariable=arm_A).grid(row=0,column=1)
arm_A.set(str(int_arm_a))
arm_B.set(str(int_arm_b))
scale.set(str(float_scale))

arm_b_Entered = ttk.Entry(window, width=15, textvariable=arm_B).grid(row=1,column=1)
scale_Entered = ttk.Entry(window, width=15, textvariable=scale).grid(row=2,column=1)
labelA = ttk.Label(window, text="A = "+str(int_arm_a))
labelA.grid(row=0,column=2)
labelB = ttk.Label(window, text="B = "+str(int_arm_b))
labelB.grid(row=1,column=2)
labelC = ttk.Label(window, text="S = "+str(float_scale))
labelC.grid(row=2,column=2)

bSave = ttk.Button(window, text="Save", command=b_Save).grid(row=3, column=0)
bUse = ttk.Button(window, text="Use", command=b_Use).grid(row=3, column=1)
bLoad = ttk.Button(window, text="Load", command=b_Load).grid(row=3, column=2)

def on_mouse(event, x, y, flags, param):
    global start,canWrite,first
    global coordSave
    pt = (x, y)
    global coord
    coord = pt
    if event == cv2.EVENT_LBUTTONDOWN:
        start = True
        canWrite = True
        first = True

    elif event == cv2.EVENT_LBUTTONUP:
        start = False
    elif start and event == cv2.EVENT_MOUSEMOVE:
        cv2.circle(param, pt, 5, (255, 0, 255), -1)

def makeSliders():
    cv2.namedWindow('Draw')
    cv2.createTrackbar('Upper', 'Draw', int_upper, 100, nothing)
    cv2.createTrackbar('Lower', 'Draw', int_lower, 100, nothing)
    cv2.setMouseCallback('Draw', on_mouse, fondo)


def drawLayout():
    global canWrite, first,coordSave,stateColor,record,pointsRecorded
    radio = 5

    fondo = cv2.imread("blanco.png")


    cv2.line(fondo, (0, h), (2 * w, h), negro, 1, cv2.LINE_AA)
    cv2.line(fondo, (w, 0), (w, 2 * h), negro, 1, cv2.LINE_AA)
    cv2.circle(fondo, origenReal, 235, rojo, 1, cv2.LINE_AA)
    posUpperSlider = cv2.getTrackbarPos('Upper', 'Draw')
    posLowerSlider = cv2.getTrackbarPos('Lower', 'Draw')

    DA = DrawArm(fondo,(por2pix(int_arm_a),por2pix(int_arm_b),float_scale,int_total_dis,por2pix(posUpperSlider),por2pix(posLowerSlider)),(0,0,0,0,0,0))
    coordAux = DA.real2aux(coord)
    message, realPoint = DA.workZone(coordAux)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        print("picado")
        #cv2.imwrite("images/snapshot/chido.png", fondo)
        if stateColor == 3:
            stateColor = 4
    if stateColor == 4:
        pointsRecorded.append(realPoint)
        if cv2.waitKey(1) & 0xFF == ord('d'):
            print("dejado")
            export_file_path = filedialog.asksaveasfilename(initialdir ="Trajectories",defaultextension='.npy')
            np.save(export_file_path, pointsRecorded)

            #dirSS = "images/snapshot/"+save
            #print(dirSS)

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
        #x = datetime.datetime.now()
        #print(x)
        #print(export_file_path)
        name = getNameFromDirectory(export_file_path)

        directorio = "images/snapshot/"+name+".png"
        #print(directorio)
        cv2.imwrite(directorio,remake)
        stateColor=1

    if not start:
        if not canWrite:
            message = DA.workZoneColor(init_Coord, DA.grisaceo, DA.grisaceo)
            cA = np.array(coordAux)
            cS = np.array(init_Coord)
            if stateColor != 4 and stateColor != 5:
                if abs(cA[0] - cS[0]) <= radio and abs(cA[1] - cS[1]) <= radio:
                    stateColor = 3
                else:
                    stateColor =1
        else:
            if first:
                coordSave = coordAux
                first = False
            message = DA.workZoneColor(coordSave, DA.grisaceo, DA.grisaceo)

            cA = np.array(coordAux)
            cS = np.array(coordSave)
            if stateColor != 4 and stateColor != 5:
                if abs(cA[0] - cS[0]) <= radio and abs(cA[1] - cS[1]) <= radio:
                    stateColor = 3
                else:
                    stateColor = 1



        """
        if stateColor == 1 or stateColor == 2:
            print("Can´t record")
        else:
            print("Record")
            record = True
            stateColor = 4
            """
    
    DA.circleState(stateColor)

    '''
    if cv2.waitKey(1) & 0xFF == ord('s'):
        if stateColor == 1 or stateColor == 2 :
            print("Can´t record")
        else:
            print("Record")
            record = True
            stateColor = 4
    if not canWrite:
        message2 = DA.workZoneColor([0,100], DA.grisaceo, DA.grisaceo)

    DA.circleState(stateColor)



    if stateColor == 4:
        pointsRecorded.append(realPoint)
        if cv2.waitKey(1) & 0xFF == ord('d'):
            #print("entre chido")
            export_file_path = filedialog.asksaveasfilename(defaultextension='.npy')
            np.save(export_file_path, pointsRecorded)
            stateColor = 5


    if canWrite:
        #print("si")
        if record == False:
            cA = np.array(coordAux)
            cS = np.array(coordSave)
            #if (cA[0] >= cS[0] * .9 and cA[0] <= cS[0] * 1.1):
            #    if cA[1] >= cS[1] * .9 and cA[1] <= cS[1] * 1.1:
            #if coordAux == coordSave:
            if abs(cA[0]-cS[0])<=radio and abs(cA[1]-cS[1])<=radio:
                stateColor = 3
            else:
                stateColor = 2
        if first:
            coordSave = coordAux
            stateColor=2
            print(coordSave)
            first = False
        message = DA.workZoneColor(coordSave,DA.grisaceo,DA.grisaceo)
        #canWrite = False

    '''
        #print(coordAux)
    cv2.putText(fondo, str(coordAux), (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, azul, lineType=cv2.LINE_AA)

    cv2.putText(fondo, message, (10, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, azul, lineType=cv2.LINE_AA)


    if posUpperSlider>90:
        cv2.setTrackbarPos('Upper', 'Draw', 90)
    if posUpperSlider<10:
        cv2.setTrackbarPos('Upper', 'Draw', 10)

    if(posLowerSlider>posUpperSlider*0.8):
        cv2.setTrackbarPos('Lower', 'Draw',int( posUpperSlider*0.8))
    if (posLowerSlider < 5):
        cv2.setTrackbarPos('Lower', 'Draw', 5)

    disUpper = posUpperSlider #0 - 100
    disLower = posLowerSlider
    posUpperSlider = int((235 * posUpperSlider) / 100) #convierte porcentaje en pixeles 100 % = 235 pixeles
    posLowerSlider = int((235 * posLowerSlider) / 100)
    disUpper = (int_total_dis * disUpper) / 100
    disLower = (int_total_dis * disLower) / 100
    cv2.circle(fondo, origenReal, posUpperSlider, azul, 1, cv2.LINE_AA)
    cv2.circle(fondo, origenReal, posLowerSlider, verde, 1, cv2.LINE_AA)
    cv2.putText(fondo, str(int_total_dis), (320, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), lineType=cv2.LINE_AA)
    y1 = int(240-disUpper)
    y2 = int(240+disLower)
    cv2.putText(fondo, str(disUpper), (320, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, azul, lineType=cv2.LINE_AA)
    cv2.putText(fondo, str(disLower), (320, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, verde, lineType=cv2.LINE_AA)
    cv2.imshow('Draw', fondo)
    window.after(1, drawLayout)

makeSliders()
drawLayout()

window.mainloop()
