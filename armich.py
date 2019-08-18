import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import cv2
import numpy as np
from math import sqrt,atan2,pi,asin,sin,cos,acos
class DrawArm:
    def __init__(self,bgr,lb):
        self.bgr = bgr
        self.lb = lb
        self.armA = lb[0]
        self.armB = lb[1]
        self.UL = 0
        self.LL = 0

        self.rojo,self.verde,self.azul,self.amarillo,self.negro = (0, 0, 255),(0, 255, 0),(255, 0, 0),(0, 255, 255),(0, 0, 0)
        self.rad2deg,self.deg2grad  = (180 / pi),(pi / 180)
        self.interes = (0, 0)

        self.h, self.w = self.bgr.shape[:2]
        self.h,self.w = int(self.h / 2),int(self.w / 2)
        self.h0, self.w0 = 0, 0
        self.o_aux,self.o_real = (self.w0, self.h0),(self.w, self.h)

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

    def workZone(self,POI,UL,LL):

        dis = self.distance(self.o_aux,POI)
        self.UL = UL
        self.LL = LL
        angle = self.getAngle(POI)

        #print("Angle:",angle,"Cosx:",x,"Sinx:",y)
        if dis > UL:
            x = int(cos(angle * self.deg2grad) * UL)
            y = int(sin(angle * self.deg2grad) * UL)
            #print(POI,"-",[x,y])
            cv2.circle(self.bgr, self.aux2real((x,y)), 10, (255, 0, 255), -1)
            armLeft, armRight = self.getJoint((x,y))
            self.drawArms(armLeft, armRight, (x,y), DA.verde,self.azul)
            return "OUT UP"
        elif dis < LL:
            x = int(cos(angle * self.deg2grad) * LL)
            y = int(sin(angle * self.deg2grad) * LL)
            # print(POI,"-",[x,y])
            cv2.circle(self.bgr, self.aux2real((x, y)), 10, (255, 0, 255), -1)
            armLeft, armRight = self.getJoint((x, y))
            self.drawArms(armLeft, armRight, (x, y), DA.verde,self.azul)
            return "OUT IN"
        else:
            cv2.circle(self.bgr, self.aux2real(POI), 10, (255, 0, 255), -1)
            armLeft, armRight = self.getJoint(POI)
            self.drawArms(armLeft, armRight, POI, DA.verde,self.azul)
            return "ok"

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
        gammaRO = angleRO-gamma
        xbrazo1 = int(round(self.armA * cos(alfaRO * self.deg2grad), 0))
        ybrazo1 = int(round(self.armA * sin(alfaRO * self.deg2grad), 0))
        brazo1= (xbrazo1, ybrazo1)
        xbrazo2 = int(round(self.armB * cos(gammaRO * self.deg2grad), 0))
        ybrazo2 = int(round(self.armB * sin(gammaRO * self.deg2grad), 0))
        brazo2 = (xbrazo2,ybrazo2)
        return brazo1,brazo2

    def drawArms(self,brazoA, brazoB,POI,color,color2):

        cv2.line(self.bgr, self.o_real, self.aux2real(brazoA), color, 2, cv2.LINE_AA)
        cv2.circle(self.bgr, self.aux2real(brazoA), int(6), self.amarillo, -1, cv2.LINE_AA)
        cv2.line(self.bgr, self.aux2real(brazoA), self.aux2real(POI), color2, 2, cv2.LINE_AA)

        cv2.line(self.bgr, self.o_real, self.aux2real(brazoB), color2, 2, cv2.LINE_AA)
        cv2.circle(self.bgr, self.aux2real(brazoB), int(6), self.amarillo, -1, cv2.LINE_AA)
        cv2.line(self.bgr, self.aux2real(brazoB), self.aux2real(POI), color, 2, cv2.LINE_AA)

        cv2.circle(self.bgr, self.aux2real(POI), int(6), self.rojo, -1, cv2.LINE_AA)

def por2pix(dis):
    return int((235*dis)/100)

fondo = cv2.imread("blanco.png")
DA = DrawArm(fondo,[30,70])
#print(DA.getJoint((0,50)))
#print("Hola")