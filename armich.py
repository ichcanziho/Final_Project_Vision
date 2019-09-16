import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import cv2
import numpy as np
from math import sqrt,atan2,pi,asin,sin,cos,acos
class DrawArm:

    def __init__(self, bgr, robot,tonos):
        self.bgr = bgr
        self.mask = self.setMask(tonos)
        self.robot = robot
        self.armA,self.armB,self.scale,self.dis,self.UL,self.LL = robot[0],robot[1],robot[2],robot[3],robot[4],robot[5]
        self.rojo,self.verde,self.azul,self.amarillo,self.negro,self.gris,self.naranja,self.azulito = (0, 0, 255),(0, 255, 0),(255, 0, 0),(0, 255, 255),(0, 0, 0),(130,130,130),(166,94,46),(132,195,190)         ##
        self.rad2deg,self.deg2grad  = (180 / pi),(pi / 180)
        self.interes = (0, 0)
        self.h, self.w = self.bgr.shape[:2]
        self.h,self.w = int(self.h / 2),int(self.w / 2)
        self.h0, self.w0 = 0, 0
        self.o_aux,self.o_real = (self.w0, self.h0),(self.w, self.h)

    def circleState(self,state):
        if state == 1:
            cv2.circle(self.bgr, self.aux2real([-300,220]), int(10), self.rojo, -1, cv2.LINE_AA)
        if state == 2:
            cv2.circle(self.bgr, self.aux2real([-300, 220]), int(10), self.gris, -1, cv2.LINE_AA)
        if state == 3:
            cv2.circle(self.bgr, self.aux2real([-300, 220]), int(10), self.azulito, -1, cv2.LINE_AA)
        if state == 4:
            cv2.circle(self.bgr, self.aux2real([-300, 220]), int(10), self.verde, -1, cv2.LINE_AA)
        if state == 5:
            cv2.circle(self.bgr, self.aux2real([-300, 220]), int(10), self.naranja, -1, cv2.LINE_AA)

    def getColor(self,mask):
        circle_img = np.zeros((2*self.h, 2*self.w), np.uint8)
        hsv = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2HSV)
        gauss = cv2.GaussianBlur(mask, (5, 5), 0)

        contornos, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #print(area)''''
        for c in contornos:

            M = cv2.moments(c)
            area = M['m00']
            #cv2.drawContours(self.bgr, c, -1, (0, 0, 255), 3)
            if(area>1000):
                print(area)


                #cv2.circle(image, (cX, cY), 2, (255, 255, 255), -1)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                mask2 = cv2.circle(circle_img, (cX, cY), 1, 1, thickness=-1)
                masked_img = cv2.bitwise_and(self.bgr, self.bgr, mask=circle_img)
                circle_locations = mask2 == 1
                bgr = self.bgr[circle_locations]
                rgb = bgr[..., ::-1]
                #print(rgb[0])
                # print(round(CVTRGB2HSV(rgb[0])[2]/5))

                #cv2.circle(image, (cX, cY), 2, (255, 255, 255), -1)

        #cv2.imshow("contornos", self.bgr)
        #cv2.imshow("Masked", masked_img)

        #'''''

    def setMask(self,limits):

        self.hsv = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(self.hsv, limits[0], limits[1])
        mask2 = cv2.inRange(self.hsv, limits[2], limits[3])
        mask3 = cv2.inRange(self.hsv, limits[4], limits[5])
        binarize = cv2.add(mask1, mask2)
        binarize = cv2.add(binarize, mask3)
        #binarize = cv2.resize(binarize,(320,240))
        kernel = np.ones((5, 5), np.uint8)
        gauss = cv2.GaussianBlur(binarize, (5, 5), 0)
        opening = cv2.morphologyEx(binarize, cv2.MORPH_OPEN, kernel)
        opening2 = cv2.morphologyEx(gauss, cv2.MORPH_OPEN, kernel)
        closing3 = cv2.morphologyEx(opening2, cv2.MORPH_CLOSE, kernel)

        closing = cv2.morphologyEx(binarize, cv2.MORPH_CLOSE, kernel)
        closing2 = cv2.morphologyEx(gauss, cv2.MORPH_CLOSE, kernel)
        opening3 = cv2.morphologyEx(closing2, cv2.MORPH_OPEN, kernel)

        return closing3
        #return binarize

    def aux2real(self, POI):
        xr = POI[0] + self.w
        yr = self.h - POI[1]
        return xr, yr

    def real2aux(self, POI):
        xf = POI[0] - self.w
        yf = self.h - POI[1]
        return xf, yf

    def pix2por(self,dis):

        return int((100*dis)/235)

    def por2pix(self,dis):

        return int((235*dis)/100)

    def workZoneColor(self,POI,Color1,Color2):

        dis = self.distance(self.o_aux,POI)
        UL = self.UL
        LL = self.LL
        angle = self.getAngle(POI)

        #print("Angle:",angle,"Cosx:",x,"Sinx:",y)
        if dis > UL:
            x = int(cos(angle * self.deg2grad) * UL)
            y = int(sin(angle * self.deg2grad) * UL)
            #print(POI,"-",[x,y])
            cv2.circle(self.bgr, self.aux2real((x,y)), 10, (130,130,130), -1)
            armLeft, armRight = self.getJoint((x,y))
            self.drawArms(armLeft, armRight, (x,y), Color1,Color2,(130,130,130))
            return "OUT UP"
        elif dis < LL:
            x = int(cos(angle * self.deg2grad) * LL)
            y = int(sin(angle * self.deg2grad) * LL)
            # print(POI,"-",[x,y])
            cv2.circle(self.bgr, self.aux2real((x, y)), 10, (130,130,130), -1)
            armLeft, armRight = self.getJoint((x, y))
            self.drawArms(armLeft, armRight, (x, y), Color1,Color2,(130,130,130))
            return "OUT IN"
        else:
            cv2.circle(self.bgr, self.aux2real(POI), 10, (255, 0, 255), -1)
            armLeft, armRight = self.getJoint(POI)
            self.drawArms(armLeft, armRight, POI, Color1,Color2,(130,130,130))
            return "ok"

    def workZone(self,POI):

        dis = self.distance(self.o_aux,POI)
        UL = self.UL
        LL = self.LL
        angle = self.getAngle(POI)

        #print("Angle:",angle,"Cosx:",x,"Sinx:",y)
        if dis > UL:
            x = int(cos(angle * self.deg2grad) * UL)
            y = int(sin(angle * self.deg2grad) * UL)
            #print(POI,"-",[x,y])
            cv2.circle(self.bgr, self.aux2real((x,y)), 10, (255, 0, 255), -1)
            armLeft, armRight = self.getJoint((x,y))
            self.drawArms(armLeft, armRight, (x,y), self.verde,self.azul,self.amarillo)
            return "OUT UP" , (x,y)
        elif dis < LL:
            x = int(cos(angle * self.deg2grad) * LL)
            y = int(sin(angle * self.deg2grad) * LL)
            # print(POI,"-",[x,y])
            cv2.circle(self.bgr, self.aux2real((x, y)), 10, (255, 0, 255), -1)
            armLeft, armRight = self.getJoint((x, y))
            self.drawArms(armLeft, armRight, (x, y), self.verde,self.azul,self.amarillo)
            return "OUT IN" , (x,y)
        else:
            cv2.circle(self.bgr, self.aux2real(POI), 10, (255, 0, 255), -1)
            armLeft, armRight = self.getJoint(POI)
            self.drawArms(armLeft, armRight, POI, self.verde,self.azul,self.amarillo)
            return "ok" , (POI)

    def distance(self,p1, p2):
        return sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2))

    def getAngle(self,POI):
        return atan2(POI[1], POI[0]) * self.rad2deg

    def getAlfa(self,distance):
        d = distance
        a = self.armA
        b = self.armB
        x = ((b ** 2) - (d ** 2) - (a ** 2)) / (-2 * d * a)
        return acos(x) * self.rad2deg

    def getBeta(self, distance):
        d = distance
        a = self.armA
        b = self.armB
        x = ((d ** 2) - (b ** 2) - (a ** 2)) / (-2 * b * a)
        return acos(x) * self.rad2deg

    def getGamma(self,alfa,beta):
        return 180-alfa-beta

    def getJoint(self,POI):
        angleRO =self.getAngle(POI)
        distanceRO = self.distance(self.o_aux,POI)
        alfa = self.getAlfa(distanceRO)
        beta = self.getBeta(distanceRO)
        gamma = self.getGamma(alfa,beta)
        alfaRO = alfa+angleRO
        gammaRO = angleRO-alfa
        xbrazo1 = int(round(self.armA * cos(alfaRO * self.deg2grad), 0))
        ybrazo1 = int(round(self.armA * sin(alfaRO * self.deg2grad), 0))
        brazo1= (xbrazo1, ybrazo1)
        xbrazo2 = int(round(self.armA * cos(gammaRO * self.deg2grad), 0))
        ybrazo2 = int(round(self.armA * sin(gammaRO * self.deg2grad), 0))
        brazo2 = (xbrazo2,ybrazo2)
        return brazo1,brazo2

    def drawArms(self,brazoA, brazoB,POI,color,color2,color3):

        cv2.line(self.bgr, self.o_real, self.aux2real(brazoA), color, 2, cv2.LINE_AA)
        cv2.circle(self.bgr, self.aux2real(brazoA), int(6), color3, -1, cv2.LINE_AA)
        cv2.line(self.bgr, self.aux2real(brazoA), self.aux2real(POI), color2, 2, cv2.LINE_AA)

        cv2.line(self.bgr, self.o_real, self.aux2real(brazoB), color2, 2, cv2.LINE_AA)
        cv2.circle(self.bgr, self.aux2real(brazoB), int(6), color3, -1, cv2.LINE_AA)
        cv2.line(self.bgr, self.aux2real(brazoB), self.aux2real(POI), color, 2, cv2.LINE_AA)

        cv2.circle(self.bgr, self.aux2real(POI), int(6), self.rojo, -1, cv2.LINE_AA)

    def drawArmsVideo(self):
        self.getPOI()
        self.drawArms(self.armA,self.armB,self.interes,self.azul,self.verde)

    def drawFrame(self):
        #cv2.circle(self.bgr, self.aux2real(brazoA), int(6), self.amarillo, -1, cv2.LINE_AA)
        cv2.line(self.bgr, (0, self.h), (2 * self.w, self.h), self.negro, 1, cv2.LINE_AA)
        cv2.line(self.bgr, (self.w, 0), (self.w, 2 * self.h), self.negro, 1, cv2.LINE_AA)
        cv2.circle(self.bgr, self.o_real, 235, self.rojo, 1, cv2.LINE_AA)
        cv2.circle(self.bgr, self.o_real, self.UL, self.azul, 1, cv2.LINE_AA)
        cv2.circle(self.bgr, self.o_real, self.LL, self.verde, 1, cv2.LINE_AA)

    def getPOI(self):
        moments = cv2.moments(self.mask)
        area = moments['m00']
        x = int(moments['m10'] / moments['m00'])
        y = int(moments['m01'] / moments['m00'])
        cv2.rectangle(self.bgr, (x, y), (x + 2, y + 2), (255, 0, 0), 2)
        cv2.line(self.bgr, self.o_real, (x, y), (0, 255, 0), 1, cv2.LINE_AA)
        x0, y0 = self.real2aux((x, y))
        self.interes=(x0,y0)
        #print(self.interes)
        return (x0, y0)

class readArms:
    def __init__(self):
        pass
    def makeArm(self):
        dataArm = pd.read_csv("calibrations/arms/current/currentArm.csv")
        arm_a = por2pix(dataArm.arm_a[0])
        arm_b = por2pix(dataArm.arm_b[0])
        scale = dataArm.scale[0]
        distance = por2pix(dataArm.distance[0])
        ul = por2pix(dataArm.UL[0])
        ll = por2pix(dataArm.LL[0])
        return (arm_a,arm_b,scale,distance,ul,ll)

class readHSV:
    def __init__(self):
        pass
    def makeMask(self):
        datahsv = pd.read_csv("calibrations/colors/current/current.csv")

        lower1 = np.array([datahsv.hMin[0], datahsv.sMin[0], datahsv.vMin[0]])
        upper1 = np.array([datahsv.hMax[0], datahsv.sMax[0], datahsv.vMax[0]])

        lower2 = np.array([datahsv.hMin[1], datahsv.sMin[1], datahsv.vMin[1]])
        upper2 = np.array([datahsv.hMax[1], datahsv.sMax[1], datahsv.vMax[1]])

        lower3 = np.array([datahsv.hMin[2], datahsv.sMin[2], datahsv.vMin[2]])
        upper3 = np.array([datahsv.hMax[2], datahsv.sMax[2], datahsv.vMax[2]])
        return (lower1,upper1,lower2,upper2,lower3,upper3)

def por2pix(dis):
    return int((235*dis)/100)

def CVTRGB2HSV(rgb):
    r =  rgb[0]/255
    g = rgb[1] / 255
    b = rgb[2] / 255
    Cmax = max(r,g,b)
    Cmin = min(r,g,b)
    Delta = Cmax-Cmin
    s=0
    if Cmax == r:
        h = 60 * (((g - b) / Delta) % 6)
    elif Cmax == g:
        h = 60 * (((b - r) / Delta) + 2)
    elif Cmax == b:
        h = 60 * (((r - g) / Delta) + 4)
    elif Delta == 0:
        h = 0
        s = 0

    if Delta != 0:
        s = (Delta / Cmax) * 100
    v = Cmax*100

    return round(h,1),round(s,1),round(v,1)

class EasyDraw(DrawArm):
    azul,rojo,verde,amarillo,morado,blanco  = (255, 0, 0),(0, 0, 255),(0, 255, 0),(0, 255, 255),(255, 0, 255),(255, 255, 255)
    def __init__(self,bgr,robot):
        DrawArm.__init__(self,bgr,robot,[0,0,0,0,0,0])

    def drawRobot(self,poi):
        armLeft, armRight = self.getJoint(poi)
        self.drawArms(armLeft, armRight, poi, self.verde, self.azul, self.amarillo)

    def getPoint(self,tk,color,point):
        cv2.circle(self.bgr, self.aux2real(point), tk, color, -1)
