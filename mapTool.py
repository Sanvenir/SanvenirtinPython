#Sanvenirtin
#roguelike game
#programming by Sanvenir
#ver 0.0.1
#map file
#Everyting about map is included
from config import *
from drawing import *

class CMapBrick:
    def __init__(self, x, y, rigidbody, ground):
        self.x = x
        self.y = y
        self.rigidbody = rigidbody
        self.ground = ground
        self.transform = 0
        self.transformMap = 0
        self.item = []

    def checkTransform(self):
        if(self.transform):
            return True
        else:
            return False

    def draw(self, cameraX, cameraY):
        if(self.rigidbody != 0):
            self.rigidbody.draw(cameraX, cameraY)
        else:
            try:
                self.ground.draw(cameraX, cameraY)
            except AttributeError:
                pass

    def undraw(self):
        try:
            self.ground.undraw()
        except AttributeError:
            pass
        try:
            self.rigidbody.undraw()
        except AttributeError:
            return

    def reset(self):
        try:
            self.rigidbody.reset()
        except AttributeError:
            pass
        try:
            if(self.rigidbody.movable):
                self.rigidbody = 0
        except AttributeError:
            pass
        try:
            self.ground.reset()
        except AttributeError:
            pass
        
class CLocalMap:
    def __init__(self, mapType, x, y, mainMap):   
        self.mapType = mapType  #0:ocean
        self.mainMap = mainMap
        self.mapFile = [[CMapBrick(0, 0, 0, 0)]]
        self.layout = [[0]]
        self.x = x
        self.y = y

    def reset(self):
        for i in self.mapFile:
            for j in i:
                j.reset()
                
    def save(self):
        self.reset()
        localFile = open("sav//map//l%04d%04d.sav"%(self.x, self.y), 'wb')
        pickle.dump(self.layout, localFile)
        localFile.close()

    def load(self):
        try:
            localFile = open("sav//map//l%04d%04d.sav"%(self.x, self.y), 'rb')
            t = pickle.load(localFile)
            localFile.close()
            self.layout = t
            self.createBlankMap()
            self.createMapFromLayout()
            return True
        except FileNotFoundError:
            return False
        
    def createBlankMap(self):
        self.mapFile = []
        self.width = localMapWidth
        self.height = localMapHeight
        for i in range(self.width):
            self.mapFile.append([])
            self.layout.append([])
            for j in range(self.height):
                self.mapFile[i].append(CMapBrick(i, j, 0, CGround("(0)", i, j, self.mapType)))
                self.layout[i].append(0)
        for i in range(1, self.width - 1):
            self.mapFile[i][0].transformMap = self.mainMap.transformMap(self.x, self.y - 1)
            self.mapFile[i][0].transform = (i, localMapHeight - 2)
            self.mapFile[i][-1].transformMap = self.mainMap.transformMap(self.x, self.y + 1)
            self.mapFile[i][-1].transform = (i, 1)
        for i in range(1, self.height - 1):
            self.mapFile[0][i].transformMap = self.mainMap.transformMap(self.x - 1, self.y)
            self.mapFile[0][i].transform = (localMapWidth - 2, i)
            self.mapFile[-1][i].transformMap = self.mainMap.transformMap(self.x + 1, self.y)
            self.mapFile[-1][i].transform = (1, i)
        self.mapFile[0][0].transformMap = self.mainMap.transformMap(self.x - 1, self.y - 1)
        self.mapFile[0][0].transform = (localMapWidth - 2, localMapHeight - 2)
        self.mapFile[0][-1].transformMap = self.mainMap.transformMap(self.x - 1, self.y + 1)
        self.mapFile[0][-1].transform = (localMapWidth - 2, 1)
        self.mapFile[-1][0].transformMap = self.mainMap.transformMap(self.x + 1, self.y - 1)
        self.mapFile[-1][0].transform = (1, localMapHeight - 2)
        self.mapFile[-1][-1].transformMap = self.mainMap.transformMap(self.x + 1, self.y + 1)
        self.mapFile[-1][-1].transform = (1, 1)

    def createLayout(self):
        for i in range(self.width):
            for j in range(self.height):
                self.layout[i][j] = random.randrange(GROUNDTYPEMAX[self.mapType])
                
    def createRandomMap(self):
        self.createBlankMap()
        self.createLayout()
        self.createMapFromLayout()
                
    def createMapFromLayout(self):
        for i in range(self.width):
            for j in range(self.height):
                groundType = "(%d)"%self.layout[i][j]
                self.mapFile[i][j].ground.changeImage(groundType)
        
class CTownMap(CLocalMap):
    def __init__(self, identity, name, x, y, environment, mainMap):
        CLocalMap.__init__(self, 5, x, y, mainMap)
        self.identity = identity
        self.name = name
        self.layout = [[0]]
        self.house = []
        self.position = []
        self.regular = False
        self.environment = environment
        #layout instruction:
        #0:undefined
        #1x:ground
        #2x:ground sides
        #3x:roads
        #4x:house floor
        #5x:house outline
        #6x:house inline
        #7x:town wall
        #8x:decoration
        #9x:door

    def createLayoutHouse(self, cx, cy, width, height):
        left = cx - width
        right = cx + width
        top = cy + height
        bottom = cy - height
        if(CCalculate.checkInMapFile(left - 1,  top + 1,    self.layout) and \
           CCalculate.checkInMapFile(left - 1,  bottom - 1, self.layout) and \
           CCalculate.checkInMapFile(right + 1, top + 1,    self.layout) and \
           CCalculate.checkInMapFile(right + 1, bottom - 1, self.layout)):
            floorType = random.randrange(10)
            wallType = random.randrange(10)
            for i in range(left - 1, right + 2):
                for j in range(bottom - 1, top + 2):
                    if(self.layout[i][j] >= 30):
                        return False
            for i in range(left, right + 1):
                for j in range(bottom, top + 1):
                    self.layout[i][j] = 50 + wallType
            for i in range(left + 1, right):
                for j in range(bottom + 1, top):
                    self.layout[i][j] = 40 + floorType
            return True
        return False

    def createMapFromLayout(self):
        for i in range(localMapWidth):
            for j in range(localMapHeight):
                floorType = random.randint(10, 19)
                if(self.layout[i][j] < 10):
                    groundType =  "%s\\(%d)"%(MAPTYPESET[self.environment], self.layout[i][j])
                    self.mapFile[i][j].ground.changeImage(groundType)
                elif(self.layout[i][j] < 40):
                    groundType =  "ground\\(%d)"%(self.layout[i][j] % 10)
                    self.mapFile[i][j].ground.changeImage(groundType)
                else:#(self.layout[i][j] < 50):
                    groundType =  "floor\\(%d)"%(self.layout[i][j] % 10)
                    self.mapFile[i][j].ground.changeImage(groundType)
                    
        
    def createRandomMap(self):
        self.createBlankMap()
        self.createLayout(20)
        self.createMapFromLayout()
                    
        
    def createBlankMap(self):
        CLocalMap.createBlankMap(self)
        for i in range(0, self.width):
            for j in range(0, self.height):
                self.layout[i].append(0)
            self.layout.append([])
            
    def createLayout(self, houseNum):
        for i in range(localMapWidth):
            for j in range(localMapHeight):
                self.layout[i][j] = random.randrange(10)
        for i in range(houseNum):
            for j in range(1000):
                width = random.randint(2, 10)
                height = random.randint(2, 10)
                cx = random.randint(width + 1, localMapWidth - width - 1)
                cy = random.randint(height + 1, localMapHeight - height - 1)
                if(self.createLayoutHouse(cx, cy, width, height)):
                    break
        
class CTown:
    def __init__(self, identity, name, x1, y1, x2, y2, environment, mainMap):
        self.identity = identity
        self.environment = environment
        self.name = name
        self.mainMap = mainMap
        self.x = (x1 + x2) / 2
        self.y = (y1 + y2) / 2
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.mainMap.mainMap[i][j] = CTownMap(identity, name, i, j, self.environment, mainMap)
        for i in range(x1, x2 + 1):
            self.mainMap.mainMap[i][y1].position.append(8)
            self.mainMap.mainMap[i][y2].position.append(2)
        for j in range(y1, y2 + 1):
            self.mainMap.mainMap[x1][j].position.append(4)
            self.mainMap.mainMap[x2][j].position.append(6)


        
            
class CMainMap:
    def loadLocalMap(self, x, y):
        t = self.mainMap[x][y].load()
        if(not t):
            self.mainMap[x][y].createRandomMap()
        return self.mainMap[x][y]
            
    def __init__(self):
        self.width = 0
        self.height = 0
        self.mainMap = []
        self.town = []
        
    def save(self):
        mapFile = open("sav//map//mainMap.sav", 'wb')
        pickle.dump(self, mapFile)
        mapFile.close()

    def load():
        try:
            mapFile = open("sav//map//mainMap.sav", 'rb')
            t = pickle.load(mapFile)
            mapFile.close()
            return t
        except FileNotFoundError:
            return False
        
    def transformMap(self, x, y):
        if(x >= len(self.mainMap)):
            rx = x - len(self.mainMap)
        elif(x < 0):
            rx = x + len(self.mainMap)
        else:
            rx = x
        if(y >= len(self.mainMap[rx])):
            ry = y - len(self.mainMap[rx])
        elif(y < 0):
            ry = y + len(self.mainMap[rx])
        else:
            ry = y
        return rx, ry
    
    #this function is not supposed to create land in empty mapFile
    def randomPositionCreateLand(self, landMinSize, landMaxSize, landType, complexity):
        left = random.randrange(0, len(self.mainMap))
        bottom = random.randrange(0, len(self.mainMap[left]))
        self.randomCreateLand(landMinSize, landMaxSize, landType[0], left, bottom)
        for i in range(complexity):
            l = random.randrange(left, left + landMinSize)
            b = random.randrange(bottom, bottom + landMinSize)
            self.randomCreateLand(2, landMaxSize, landType[random.randrange(len(landType))], l, b)
            
    def randomCreateLand(self, landMinSize, landMaxSize, landType, left, bottom):
        right = landMinSize + left
        top = landMinSize + bottom
        for i in range(left, right + 1):
            for j in range(bottom, top + 1):
                x, y = self.transformMap(i, j)
                self.mainMap[x][y] = CLocalMap(landType, x, y, self)
        side = []
        for i in range(left, right):
            x, y = self.transformMap(i, bottom)
            side.append(self.mainMap[x][y])
            x, y = self.transformMap(i + 1, top)
            side.append(self.mainMap[x][y])
        for i in range(bottom, top):
            x, y = self.transformMap(left, i)
            side.append(self.mainMap[x][y])
            x, y = self.transformMap(right, i + 1)
            side.append(self.mainMap[x][y])
        for i in range(landMaxSize - landMinSize):
            newside = []
            for j in side:
                expand = random.randrange(3)
                if(not expand):
                    for k in [1, 2, 3, 6, 9, 8, 7, 4]:
                        tx, ty = self.transformMap(j.x + DIRECTION[k].dx, j.y + DIRECTION[k].dy)
                        if(self.mainMap[tx][ty].mapType != landType):
                            self.mainMap[tx][ty] = CLocalMap(landType, tx, ty, self)
                            newside.append(self.mainMap[tx][ty])
            side = newside                
                
    def randomCreateMap(self, totalWidth, totalHeight, landNum, landMinSize, landMaxSize, landTotalType, maxComplexity):
        self.mainMap = []
        self.width = totalWidth
        self.height = totalHeight
        for i in range(totalWidth):
            self.mainMap.append([])
            for j in range(totalHeight):
                self.mainMap[i].append(CLocalMap(0, i, j, self))
        for i in range(landNum):
            self.randomPositionCreateLand(landMinSize, landMaxSize, range(1, landTotalType), random.randrange(maxComplexity))

    def randomCreateTown(self, totalNum):
        self.town.append(CTown(0, "test", 0, 0, 2, 2, 1, self))
        for i in range(1, totalNum):
            name = ""
            namelength = random.randint(2, 5)
            sex = random.randrange(2)
            width = random.randint(1, 3)
            height = random.randint(1, 3)
            for j in range(namelength):
                if(sex):
                    name += randomMaleNameList[random.randrange(len(randomMaleNameList))]
                else:
                    name += randomFemaleNameList[random.randrange(len(randomFemaleNameList))]
            name += randomTownNameList[random.randrange(len(randomTownNameList))]
            for j in range(1000):
                x1 = random.randint(3, mainMapWidth - width - 3)
                x2 = x1 + width
                y1 = random.randint(3, mainMapHeight - height - 3)
                y2 = y1 + width
                checkPosition = random.randrange(4)
                if(checkPosition == 0):
                    x, y = x1, y1
                elif(checkPosition == 1):
                    x, y = x1, y2
                elif(checkPosition == 2):
                    x, y = x2, y1
                else:
                    x, y = x2, y2
                check = random.random()
                environment = self.mainMap[x][y].mapType
                if(check < TOWNRATIO[environment]):
                    print(i, name, x1, y1, x2, y2)
                    self.town.append(CTown(i, name, x1, y1, x2, y2, environment, self))
                    break
