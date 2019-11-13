import cv2
import numpy as np
from time import time
import matplotlib.pyplot as plt

fondo = cv2.imread("images/NoiseRef.png",0)
refeference = cv2.imread("images/ref.png",0)

whiteReff = cv2.countNonZero(refeference)
noiseReff = cv2.countNonZero(fondo)
print(whiteReff)
print(noiseReff)

def setGaussian():
    gauss = cv2.GaussianBlur(fondo, (5, 5), 0)
    whites = cv2.countNonZero(gauss)
    #print("gauss:",whites)
    cv2.imshow("gauss", gauss)
    return whites

def setMedian():
    median = cv2.medianBlur(fondo, 3)
    whites = cv2.countNonZero(median)
    #print("median:", whites)
    cv2.imshow("median", median)
    return whites

def setOpClo():
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(fondo, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(fondo, cv2.MORPH_CLOSE, kernel)
    OpClo = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    whites = cv2.countNonZero(OpClo)
    #print("OpClo:", whites)
    cv2.imshow("OpClo", OpClo)
    return whites

def getTime(function):
    start_time = time()
    whites = function()
    elapsed_time = time() - start_time
    cv2.destroyAllWindows()
    return elapsed_time*1000,whites

def makeArray(function,iterations):
    array = []
    whites = []
    for i in range(iterations+1):
        time,white = getTime(function)
        array.append(time)
        whites.append(white)

    average = sum(array)/len(array)
    averageWhite = sum(whites)/len(whites)
    return array,average,averageWhite

def getAcc(aprox,exact):
    return 100 - (abs(aprox-exact)/exact*100)

def getError(aprox,exact):
    return (abs(aprox-exact)/exact*100)


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        height = round(height,4)
        plt.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 1),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

iteration = 10
#make arrays for each algorithm and obtain their respective average
gaussianArray, gaussinAverage,GAW = makeArray(setGaussian,iteration)
medianArray, medianAverage,MAW= makeArray(setMedian,iteration)
opCloArray, opCloAverage,OCAW = makeArray(setOpClo,iteration)

#show the different times for each iteration in each algorithm
plt.suptitle('Time List')
plt.plot(gaussianArray,label = "Gaussian")
plt.plot(medianArray,label = "Median")
plt.plot(opCloArray,label = "OP-CLO")
plt.legend(loc='upper left')
plt.xlabel("Sample List (number)")
plt.ylabel("Time taken (ms)")
plt.show()

#show the time average in a bar graph
names = ['Gauss AV', 'Median AV', 'OpClo Av']
values = [gaussinAverage, medianAverage, opCloAverage]
x = np.arange(len(names))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, values, width, label='Algorithms')
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time[ms]')
ax.set_title('Average Time')
ax.set_xticks(x)
ax.set_xticklabels(names)
#ax.legend()

#plt.bar(names, values)
#autolabel(values)
#plt.suptitle('Average Time [s]')
autolabel(rects1)
fig.tight_layout()
plt.show()

#obtain the number of white pixels
gaussianAcc = setGaussian()
medianAcc = setMedian()
opCloAcc = setOpClo()

gaussianAcc = GAW
medianAcc = MAW
opCloAcc = OCAW

print(gaussianAcc)
print(medianAcc)
print(opCloAcc)

names = ['G ACC', 'M ACC', 'OC ACC']
names2 = ['G E', 'M E', 'OC E']
values = [getAcc(gaussianAcc,whiteReff),getAcc(medianAcc,whiteReff),getAcc(opCloAcc,whiteReff)]
values2 = [getError(gaussianAcc,whiteReff),getError(medianAcc,whiteReff),getError(opCloAcc,whiteReff)]

plt.subplot(121)
acc= plt.bar(names, values)
autolabel(acc)
plt.subplot(122)
acc2=plt.bar(names2, values2)
autolabel(acc2)
plt.suptitle('Accuracy and Error [%]')


plt.show()
