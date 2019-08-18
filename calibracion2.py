

from armich import*

start = False
coord = (200,200)
int_arm_a, int_arm_b, float_scale, int_total_dis,int_upper,int_lower = 0,0,0,0,0,0
data = pd.read_csv("calibrations/arms/current/currentArm.csv")
int_arm_a = int(data.arm_a[0])
int_arm_b = int(data.arm_b[0])
float_scale = float(data.scale[0])
int_total_dis = int(data.distance[0])
int_upper = int(data.UL[0])
int_lower = int(data.LL[0])


def nothing(x):
    pass
def b_Use():
    global int_arm_a, int_arm_b, float_scale, int_total_dis

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
            "LL": [cv2.getTrackbarPos('Lower', 'Draw')]
            }
    data = pd.DataFrame(dict)
    print(data)
    data.to_csv("calibrations/arms/current/currentArm.csv", index=None, header=True)
def b_Save():
    global int_arm_a, int_arm_b, float_scale, int_total_dis
    dict = {"arm_a": [int_arm_a],
            "arm_b": [int_arm_b],
            "scale": [float_scale],
            "distance": [int_total_dis],
            "UL": [95],
            "LL": [5]
            }
    data = pd.DataFrame(dict)
    print(data)
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    data.to_csv(export_file_path, index=None, header=True)
def b_Load():
    global int_arm_a, int_arm_b, float_scale, int_total_dis
    open_file = filedialog.askopenfilename()
    data = pd.read_csv(open_file)
    labelA.configure(text='A = ' + str(data.arm_a[0]))
    labelB.configure(text='B = ' + str(data.arm_b[0]))
    labelC.configure(text='S = ' + str(data.scale[0]))
    int_arm_a = int(data.arm_a[0])
    int_arm_b = int(data.arm_b[0])
    float_scale = float(data.scale[0])
    int_total_dis = int(data.distance[0])

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
    global start
    pt = (x, y)
    global coord
    coord = pt
    if event == cv2.EVENT_LBUTTONDOWN:
        start = True
        print("x = ", x)
        print("y = ", y)
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
    fondo = cv2.imread("blanco.png")

    DA = DrawArm(fondo,(por2pix(int_arm_a),por2pix(int_arm_b)))

    cv2.line(fondo, (0, h), (2 * w, h), negro, 1, cv2.LINE_AA)
    cv2.line(fondo, (w, 0), (w, 2 * h), negro, 1, cv2.LINE_AA)
    cv2.circle(fondo, origenReal, 235, rojo, 1, cv2.LINE_AA)
    posUpperSlider = cv2.getTrackbarPos('Upper', 'Draw')
    posLowerSlider = cv2.getTrackbarPos('Lower', 'Draw')



    coordAux = DA.real2aux(coord)

    message = DA.workZone(coordAux,DA.por2pix(posUpperSlider),DA.por2pix(posLowerSlider))
    #print(coordAux)
    cv2.putText(fondo, str(coordAux), (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, azul, lineType=cv2.LINE_AA)

    cv2.putText(fondo, message, (10, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, azul, lineType=cv2.LINE_AA)


    if posUpperSlider>98:
        cv2.setTrackbarPos('Upper', 'Draw', 98)
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
    window.after(10, drawLayout)

makeSliders()
drawLayout()

window.mainloop()
