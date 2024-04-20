# some problems when not input standar radius, but not always
# runs correctly with same radius
# not with limits
import pprint
import sys
from collections import deque
import random

previousCircle = {}
radius = {}
q = deque()
existsLimits = False
existItems =False
existMinMax = False
existRadius = False
existSeed = False
j = 0
for el in sys.argv:
    if el == "-i":
        kikloi = int(sys.argv[j + 1])
        existItems = True
    if el == "-r":
        aktina = int(sys.argv[j + 1])
        existRadius = True
    if el == "--min_radius":
        min_radius = int(sys.argv[j + 1])
        existMinMax = True
    if el == "--max_radius":
        max_radius = int(sys.argv[j + 1])
        existMinMax = True
    if el == "-b":
        limits_file = int(sys.argv[j + 1])
        existsLimits = True
    if el == "-s" or el == "--s":
        seed = int(sys.argv[j + 1])
        existSeed = True
    j = j + 1
nmbrArgs = int(len(sys.argv))
out = sys.argv[nmbrArgs - 1]



class Alive:
    listAlive = []
    outLimits = False
alive = Alive()

class CircleCuts:
    x = 0
    y = 0
    cuts = False
circleCuts = CircleCuts()

class Delete:
    list = []
delete = Delete()

class LastCircle:
    x = 0
    y = 0
lastCircle = LastCircle()



def findTangentCircle(mx, my, nx, ny, nextRadius, existsLimits):
    dx = nx - mx
    dy = ny - my
    sum = dx * dx + dy * dy
    d = sum**(.5)
    r1 = radius[(mx, my)] + nextRadius
    r2 = radius[(nx, ny)] + nextRadius
    r1 = round(r1, 2)
    r2 = round(r2, 2)
    l = (r1*r1 - r2*r2 +d*d)/(2 * d*d) 
    e1 = (r1*r1) / (d*d) - l*l
    e = e1**(0.5)
    kx = mx + l*dx - e*dy
    ky = my + l*dy + e*dx
    kx = kx.real
    ky = ky.real
    kx = round(kx, 2)
    ky = round(ky, 2)
    findLessDistanceStart()
    if cutsAnotherCircle(kx, ky, nextRadius) and (not OutOfLimits(kx, ky, nextRadius, existsLimits)):
        if (previousCircle[(mx,my)] == (nx, ny)):
            mx, nx = nx, mx
            my, ny = ny, my
        if CircleAfterCn(nx, ny, circleCuts.x, circleCuts.y ):
            deleteCircleAfterCn(nx, ny, mx, my, circleCuts.x, circleCuts.y)
        else:
            deleteCircleBeforeCm(mx, my, nx, ny, circleCuts.x, circleCuts.y)
            nx , ny = circleCuts.x, circleCuts.y
        circleCuts.cuts = True
    elif (OutOfLimits(kx, ky, nextRadius, existsLimits)):
        alive.listAlive.remove((mx, my))
        alive.outLimits = True
    else:
        previousCircle[(kx,ky)] = (nx, ny)
        radius[(kx, ky)] = nextRadius
        q.appendleft((kx, ky))
        lastCircle.x = kx
        lastCircle.y = ky
        start = findLessDistanceStart()
        startX = start[0]
        startY = start[1]
        previousCircle[(startX, startY)] = (kx,ky)
        alive.listAlive.append((kx, ky))
        for cntr in previousCircle:
            if cntr not in alive.listAlive:
                alive.listAlive.append(cntr)
        circleCuts.cuts = False
        alive.outLimits = False

        f = open(out, 'a')
        x = str(kx)
        y = str(ky)
        r = radius[(kx, ky)]
        r1 = str(r)
        f.write(x + " " + y + " " + r1 + "\n")
        f.close()



def OutOfLimits(x, y, r, existsLimits):
    outOfLimits = False
    if existsLimits:
        f = open('limits_file')
        for line in f.readlines():
            line = (line.split(" "))
            limits = [float(i) for i in line]
            x1 = limits[0]
            y1 = limits [1]
            x2 = limits[2]
            y2 = limits[3]
            l2 = (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
            if l2 == 0:
                d = (x1 - x)*(x1 - x) + (y1 - y)*(y1 - y)
                d = d**(.5)
            else:
                t = ((x - x1)(x2 - x1) + (y - y1)(y2 - y1)) / l2
                t = max(0, min(1,t))
                px = x1 + t(x2 - x1)
                py = y1 + t(y2 - y1)
                d = (px - x)*(px - x) + (py - y)*(py - y)
                d = d**(0.5)
            if (d < r):
                outOfLimits = True
                break
        f.close()
    return outOfLimits 



def deleteCircleBeforeCm(xm, ym, xn, yn, xj, yj):
    previousCircle[(xn, yn)] = (xj, yj)
    for cntr in previousCircle:
        if cntr[0] == xn and cntr[1] == yn:
            break
        if previousCircle[cntr] == (xj, yj):
            nextX = cntr[0]
            nextY = cntr[1]
            delete.list.append((nextX, nextY))
            xj = nextX
            yj = nextY
    


def deleteCircleAfterCn(xn, yn, xm, ym, xi, yi):
    previousCircle[(xi ,yi)] = (xm, ym)
    for cntr in previousCircle:
        if cntr[0] == xi and cntr[1] == yi:
            break
        if previousCircle[cntr] == (xm, ym):
            nextX = cntr[0]
            nextY = cntr[1]
            delete.list.append((nextX, nextY))
            xm = xn 
            ym = yn
            for c in previousCircle:
                if previousCircle[c] == (xn, yn):
                    xn = c[0]
                    yn = c[1]
    



def cutsAnotherCircle(x, y, r):
    cuts = False
    for c in previousCircle:
        x1 = c[0]
        y1 = c[1]
        x1 = round(x1, 2)
        y1 = round(y1, 2)
        sum = (x - x1)*(x - x1) + (y - y1)*(y - y1)
        distance = sum**(0.5)
        distance = round(distance,2)
        sumRadius = r + radius[(x1,y1)]
        sumRadius = round(sumRadius,2)
        if (distance  < sumRadius):
            circleCuts.x = x1
            circleCuts.y = y1
            cuts = True
            break
    return cuts

    
def findLessDistanceStart():
    less = 1000000
    for cntr in q:
        if cntr in previousCircle:
            x = cntr[0]
            y = cntr[1]
            sum = (x - 0)*(x - 0) + (y - 0)*(y - 0)
            distFromStart = sum**(0.5)
            distFromStart = round(distFromStart, 2)
            if  (distFromStart <= less):
                less = distFromStart
                cm = (x,y)
    return cm    



def CircleAfterCn(xn, yn, x, y):
    for v in q:
        if (v == (x,y)):
            after = True
            break
        if (v == (xn,yn)):
            after = False
            break
    return after
        

def findRadius(existMinMax, existRadius, aktina):
    if existMinMax:
        aktinaUse = random.uniform(min_radius ,max_radius)
        aktinaUse = round(aktinaUse, 2)
    else :
        aktinaUse = random.random()
        aktinaUse = round(aktinaUse, 2)
    if existRadius:
        aktinaUse = round(aktina, 2)
    return aktinaUse

if existSeed:
    random.seed(seed)
if not existRadius:
    aktina = -1


# 2 first circles
rad = findRadius(existMinMax, existRadius, aktina)
aktina1 = rad
radius [(0,0)] = rad
q.appendleft((0,0))
previousCircle[(0,0)] = ()
rad = findRadius(existMinMax, existRadius, aktina)
aktina2 =rad
previousCircle[(aktina1+aktina2 ,0)] = (0,0)
radius[(aktina1+aktina2,0)] = rad
q.appendleft((aktina1+aktina2,0))
alive.listAlive.append((0,0))
alive.listAlive.append((aktina1+aktina2,0))

f = open(out, 'a')
x = str(0)
y = str(0)
r = radius[(0, 0)]
r1 = str(r)
f.write(x + " " + y + " " + r1 + "\n")
x = str(aktina1+aktina2)
y = str(0)
r = radius[(aktina1+aktina2, 0)]
r1 = str(r)
f.write(x + " " + y + " " + r1 + "\n")
f.close()


# 3rd circle
rad = findRadius(existMinMax, existRadius, aktina)
findTangentCircle(0, 0 ,aktina1+aktina2, 0, rad, existsLimits)



def runProg(aktina):     
    start = findLessDistanceStart()
    startX = start[0]
    startY = start[1]
    for cntr in previousCircle:
        if (cntr[0] == startX and cntr[1] == startY):
            followX = previousCircle[cntr][0]
            followY = previousCircle[cntr][1]
    findTangentCircle(startX, startY , followX, followY, aktina, existsLimits)
    for v in delete.list:
        previousCircle.pop(v)
        radius.pop(v)
    delete.list.clear()
    if circleCuts.cuts == True or alive.outLimits == True:
        start = findLessDistanceStart()
        startX = start[0]
        startY = start[1]
        for cntr in previousCircle:
            if (cntr[0] == startX and cntr[1] == startY):
                followX = previousCircle[cntr][0]
                followY = previousCircle[cntr][1]
        findTangentCircle(startX, startY , followX, followY, aktina, existsLimits)


if existItems:
    #had already 3 circles
    for _i in range(0, kikloi - 3):
        if len(alive.listAlive) == 0:
            break
        rad = findRadius(existMinMax, existRadius, aktina)
        runProg(rad)
else :
    while len(alive.listAlive) > 0:
        rad = findRadius(existMinMax, existRadius, aktina)
        runProg(rad)

print(len(q))0 0 0.63
1.29 0 0.66
0.61 1.4 0.9
-0.36 0.79 0.24
-0.61 0.49 0.15
-1.48 -0.0 0.85
-0.52 -1.3 0.77
0.28 -0.77 0.19
0.56 -0.56 0.16
