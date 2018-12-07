#Sanvenirtin
#roguelike game
#programming by Sanvenir
#ver 0.0.1
#Scene file
#Including scene and scene manager classes

from spirit import *

class CGameScene:
    def __init__(self, x, y, localMap, raceList, hero, gui):
        CHero.cameraX = x
        CHero.cameraY = y
        self.hero = hero
        self.localMap = localMap
        self.width = self.localMap.width
        self.height = self.localMap.height
        self.mapFile = self.localMap.mapFile
        self.hero.mapFile = self.mapFile
        random.seed(time.time())
        self.spiritList = []
        self.race = raceList
        self.spiritList.append(self.hero)
        self.hero.moveTo(x, y)
        for i in range(20):
            race = 0
            age = random.randint(1, self.race[race].longevity)
            self.randomAddNPC(0, age, self.race[race])
        for i in range(20):
            race = 0
            age = random.randint(1, self.race[race].longevity)
            self.randomAddNPC(1, age, self.race[race])
        for i in range(50):
            race = random.randrange(len(self.race))
            age = random.randint(1, self.race[race].longevity)
            self.randomAddNPC(random.randrange(2), age, self.race[race])
        self.conditionDisplay = gui

    def undraw(self):  
        try:
            for i in self.drawingText:
                try:
                    i.undraw()
                except AttributeError:
                    pass
        except AttributeError:
            pass
        self.drawingText = []
        try:
            for i in self.drawingItem:
                try:
                    i.undraw()
                except AttributeError:
                    pass
        except AttributeError:
            pass
        self.drawingItem = []
        for i in self.mapFile:
            for j in i:
                j.undraw()
                try:
                    j.rigidbody.invisible = False
                except AttributeError:
                    continue
        
    def randomAddNPC(self, sex, age, race):
        fail = True
        for i in range(1000):
            x = random.randint( min(-1, -(self.width - (self.hero.x + self.hero.getSightValue()))), max(1, self.hero.x - self.hero.getSightValue()))
            y = random.randint( min(-1, -(self.height- (self.hero.y + self.hero.getSightValue()))), max(1, self.hero.y - self.hero.getSightValue()))
            if(x < 0):
                x += self.width
            if(y < 0):
                y += self.height
            if(not self.mapFile[x][y].rigidbody and CCalculate.checkInMapFile(x, y, self.mapFile)):
                fail = False
                break
        if(fail):
            print("NPC creating fail.Please check map file setting or retry.")
            return False
        identity = len(self.spiritList)
        name = ""
        if(age < race.longevity / 5):
            name += "新生的"
        elif(age < 2 * race.longevity / 5):
            name += "幼年的"
        elif(age < 3 * race.longevity / 5):
            name += "年轻的"
        elif(age < 4 * race.longevity / 5):
            name += "成熟的"
        else:
            name += "老成的"
        if(sex == 0):
            name += "男性"
        elif(sex == 1):
            name += "女性"
        else:
            name += "性别不明的"
        self.spiritList.append(0)
        if(race.identity == 0):
            imageName = random.randint(1, 100)
            self.spiritList[identity] = CNPC(identity, SEXSET[sex] + '(' + str(imageName) + ')', x, y, self.mapFile, self.spiritList, sex, age, race)
            if(sex == 0):
                for i in range(random.randint(2, 5)):
                    name += randomMaleNameList[random.randrange(len(randomMaleNameList))]
            elif(sex == 1):
                for i in range(random.randint(2, 5)):
                    name += randomFemaleNameList[random.randrange(len(randomFemaleNameList))]
            self.spiritList[identity].changeName(name)
            self.spiritList[identity].aiFlag = 2
        else:
            self.spiritList[identity] = CNPC(identity, SEXSET[2] + '(' + str(race.identity) + ')', x, y, self.mapFile, self.spiritList, sex, age, race)
            name += race.name
            self.spiritList[identity].changeName(name)
            self.spiritList[identity].aiFlag = 2
        self.spiritList[identity] += self.spiritList[identity].race.randomCreateProperty(self.spiritList[identity].age, self.spiritList[identity].sex)
        self.spiritList[identity].initialize()
        self.spiritList[identity].nextMoveTime = self.hero.nextMoveTime
        self.spiritList[identity].createHumanBody()
        return True
    
    def randomMakeMap(self, width, height):
        self.width = width
        self.height = height
        for i in range(width):
            rawMap = []
            for j in range(height):
                rawMap.append(CMapBrick(0, CGround("(" + str(random.randrange(38)) + ")", i, j)))
            self.mapFile.append(rawMap)
        for i in range(width):
            for j in range(height):
                check = random.randrange(20)
                if(not check):
                    rigidType = random.randint(1, 13)
                    self.mapFile[i][j].rigidbody = CObstacle("(" + str(rigidType) + ")", i, j)

    def draw(self):
        self.undraw()
        try:
            for i in range(max(0, int(CHero.cameraX + leftScreen)), int(CHero.cameraX + rightScreen) + 1):
                try:
                    for j in range(max(0, int(CHero.cameraY + bottomScreen)), int(CHero.cameraY + topScreen) + 1):
                        if(CCalculate.checkInMapFile(i, j, self.mapFile) and not CCalculate.outRangeCheck(CHero.cameraX, CHero.cameraY, i, j, pow(self.hero.getSightValue(), 2))):
                            self.mapFile[i][j].draw(CHero.cameraX, CHero.cameraY)
                            try:
                                self.mapFile[i][j].rigidbody.invisible = True
                                self.drawingText.append(self.mapFile[i][j].rigidbody.text)
                            except AttributeError:
                                for k in range(len(self.mapFile[i][j].item)):
                                    self.mapFile[i][j].item[k].setDrawing(i, j, k, CHero.cameraX, CHero.cameraY)
                                    self.drawingItem.append(self.mapFile[i][j].item[k])
                except IndexError:
                    pass
            for i in self.drawingText:
                i.draw(win)
            for i in self.drawingItem:
                i.draw()
        except IndexError:
            return

    def update(self):
        for i in self.spiritList[1:]:
            while(self.hero.nextMoveTime > i.nextMoveTime and not i.dead):
                i.AI_update()
        self.conditionDisplay.update(self.hero)
