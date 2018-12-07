#Sanvenirtin
#roguelike game
#programming by Sanvenir
#ver 0.0.1
#Config file
#Including global var or const, and some unimportant class and define

import math
import time
import random
import pickle
import os
from randomName import *
from graphics import *


class CCalculate:
    def createMap(w, h, a):
        m = []
        for i in range(w):
            m.append([])
            for j in range(h):
                m[i].append(a)
        return m
    def powNSqrt(x, y):
        return math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    
    def mouseTMap(q):
        if(q.getX() + 0.5 > 0):
            dx = int(q.getX() + 0.5)
        else:
            dx = int(q.getX() - 0.5)
        if(q.getY() + 0.5 > 0):
            dy = int(q.getY() + 0.5)
        else:
            dy = int(q.getY() - 0.5)
        return CDirection(dx, dy)
    
    def _findWay(tMap, cx, cy, tx, ty):
        if(tx < 0 or tx >= len(tMap) or ty < 0 or ty >= len(tMap[0])):
            return CDirection(CCalculate.getNumSymbol(tx - cx), CCalculate.getNumSymbol(ty - cy))
        tMap[tx][ty] = 0
        queue = []
        parent = CCalculate.createMap(len(tMap), len(tMap[0]), 0)
        queue.append((cx, cy))
        tMap[cx][cy] = 2
        parent[cx][cy] = (cx, cy)
        success = False
        while(queue != [] and not success):
            nx, ny = queue[0]
            del queue[0]
            if(nx == tx and ny == ty):
                success = True
            if(not success):
                for i in [2, 6, 8, 4, 3, 9, 7, 1]:
                    tnx = nx + DIRECTION[i].dx
                    tny = ny + DIRECTION[i].dy
                    if(tnx < 0 or tnx >= len(tMap)): continue
                    if(tny < 0 or tny >= len(tMap[0])): continue
                    if(tMap[tnx][tny] == 0):
                        tMap[tnx][tny] = 1
                        parent[tnx][tny] = (nx, ny)
                        queue.append((tnx, tny))
                tMap[nx][ny] = 2
        if(success):
            while(parent[nx][ny] != (cx, cy)):
                 nx, ny = parent[nx][ny]
            return CDirection(nx - cx, ny - cy)
        else:
            return CDirection(CCalculate.getNumSymbol(tx - cx), CCalculate.getNumSymbol(ty - cy))
           

    def getNumSymbol(num):
        if(num > 0):
           return 1
        elif(num == 0):
           return 0
        elif(num < 0):
           return -1
        
    def checkInMapFile(x, y, mapFile):
        if(x < 0  or x >= len(mapFile) or y < 0  or y >= len(mapFile[x])):
            return False
        else:
            return True
        
    def findWay(mapFile, cx, cy, tx, ty, intValue):
        consciousMap = []
        for i in range(2 * intValue + 1):
            consciousMap.append([])
            for j in range(2 * intValue + 1):
                consciousMap[i].append(3)
        for i in range(cx - intValue + 1, cx + intValue):
            for j in range(cy - intValue + 1, cy + intValue):
                if(not(CCalculate.outRangeCheck( intValue - cx + i, intValue - cy + j, intValue, intValue, pow(intValue, 2)) or not CCalculate.checkInMapFile(i, j, mapFile))):
                    if(mapFile[i][j].rigidbody):
                        consciousMap[intValue - cx + i][intValue - cy + j] = 4
                    else:
                        consciousMap[intValue - cx + i][intValue - cy + j] = 0
        return CCalculate._findWay(consciousMap, intValue, intValue, intValue + tx - cx, intValue + ty - cy)

    def outRangeCheck(cx, cy, tx, ty, rangeValue):
        if(pow(cx - tx, 2) + pow(cy - ty, 2) > rangeValue):
            return True
        else:
            return False
            
    
class CDirection:
    def __init__(self, x, y):
        self.dx = x
        self.dy = y

    def surround(self):
        if(self.dx > 0):
            dx = 1
        elif(self.dx == 0):
            dx = 0
        else:
            dx = -1
        if(self.dy > 0):
            dy = 1
        elif(self.dy == 0):
            dy = 0
        else:
            dy = -1
        return CDirection(dx, dy)
    
    def noMove(self):
        if(self.dx == 0 and self.dy == 0):
            return True
        else:
            return False
        
heroName = "hero"
leftScreen = -10.0
rightScreen = 10.0
bottomScreen = -8.0
topScreen = 8.0
imageBaseWidth = 48
imageBaseHeight = 48

actionButtonSize = 0.49
actionButtonDistance = 1.0

gameTime = 0.0
SEXSET = {0:"male", 1:"female", 2:"monster"}
MAPTYPESET = {0:"ocean", 1:"grass", 2:"forest", 3:"desert", 4:"snowfield", 5:"town", 6:"villiage"}
MAPCOLORSET = ["blue", "green1", "green4", "yellow1", "white", "red"]
TOWNRATIO = {0: 0.001, 1:1.0, 2:0.5, 3:0.3, 4:0.5, 5: 0.0}
EQUIPTYPE = {0:"all", 1:"bag", 2:"weapon", 3:"upwear", 4:"underwear"}
BODYTYPE = {0:"none", 1:"meat", 2:"wood", 3:"stone", 4:"metal"}
GROUNDTYPEMAX = {0:3, 1:30, 2:14, 3:46, 4:33, 5:27}
DIRECTION = {1: CDirection( -1, -1),2: CDirection(  0, -1),3: CDirection(  1, -1), \
             4: CDirection( -1,  0),5: CDirection(  0,  0),6: CDirection(  1,  0), \
             7: CDirection( -1,  1),8: CDirection(  0,  1),9: CDirection(  1,  1)}

localMapWidth = 50
localMapHeight = 50
mainMapWidth = 500
mainMapHeight = 500
#initialize;
wndWidth = (imageBaseWidth * int(rightScreen - leftScreen ))
wndHeight = (imageBaseHeight * int(topScreen - bottomScreen))
win = GraphWin("Sanvenirtin", wndWidth, wndHeight, False, 600, 50)
win.setCoords(leftScreen - 0.5, bottomScreen - 0.5, rightScreen + 0.5, topScreen + 0.5)
