#Sanvenirtin
#roguelike game
#programming by Sanvenir
#ver 0.0.1
#Spirit file
#Including drawing objects and rigidbody, especially spirits classes

from mapTool import *
from gui import *

class CBodyPart:
    def __init__(self, name, construction, equipType, strength):
        self.name = name
        self.construction = construction
        self.equipType = equipType
        self.strength = strength
        self.equipment = []
        self.totalWeight = 0

    def equiping(self, equipment):
        self.equipment.append(equipment)
        self.totalWeight += equipment.weight

    def unequiping(self, identity):
        try:
            unequipment = self.equipment[identity]
            del self.equipment[identity]
            self.equipment -= unequipment.weight
            return unequipment
        except AttributeError:
            print("Unequiping error items.Please check your settings.")
            return False

    def checkOverWeight(self):
        if(self.strength < self.totalWeight):
            return True
        else:
            return False

    def reset(self):
        for i in self.construction:
            i.reset()
        for i in self.equipment:
            i.reset()
        

        
class CRigidbody(CDrawingObject):
    def __init__(self, imageName, x, y, mapFile):
        CDrawingObject.__init__(self, imageName, x, y)
        self.mapFile = mapFile
        self.bodyPart = []
        self.movable = False

    def addBodyPart(self, name, construction, strength):
        if(name == "手部"):
            self.bodyPart.append(CBodyPart(name, construction, [0], strength))
        if(name == "身体"):
            self.bodyPart.append(CBodyPart(name, construction, [1, 2, 3], strength))

    def destroyed(self):
        for i in self.bodyPart:
            for j in i.equipment:
                self.mapFile[self.x][self.y].item.append(j)
            for j in i.construction:
                self.mapFile[self.x][self.y].item.append(j)
        
class CObstacle(CDrawingObject):
    def __init__(self, win, imageName, x, y, obstacleType, mapFile):
        CDrawingObject.__init__(self, imageName, x, y)
        self.movable = False

    def draw(self, cameraX, cameraY):
        CDrawingObject.draw(self, cameraX, cameraY, ".//res//image//obstacle//" + self.imageName + ".gif")

class CItem:
    def __init__(self, name, weight, volume, imageType = "", imageID = 0):
        self.name = name
        self.weight = weight
        self.volume = volume
        self.imageName = ".//res//image//item//" + imageType + "//(" + str(imageID) + ").gif"
        self.introduction = "此物品还没有介绍。"

    def setDrawing(self, x, y, z, cameraX, cameraY):
        self.drawing =  CDrawingObject(self.imageName, x, y + float(z)/5.0)
        self.cameraX = cameraX
        self.cameraY = cameraY

    def setIntroduction(self, text):
        self.introduction = text

    def draw(self):
        self.drawing.draw(self.cameraX, self.cameraY, self.imageName)

    def undraw(self):
        try:
            self.drawing.undraw()
            del self.drawing
        except AttributeError:
            return

    def reset(self):
        try:
            del self.drawing
        except AttributeError:
            return

class CFood(CItem):
    def __init__(self, name, weight, volume, category, imageID):
        CItem.__init__(self, name, weight, volume, "food//" + category, imageID)

    def setEffect(self, addHunger, addHealth, addInjure, addEndure, addProperty, consume):#Be careful about the injure count
        self.addHunger = addHunger
        self.addHealth = addHealth
        self.addInjure = addInjure
        self.addEndure = addEndure
        self.addProperty = addProperty
        self.consume = consume

    def using(self, target, usingList):
        target.hunger[0] += self.addHunger
        target.health[0] += self.addHealth
        target.injure[0] += self.addInjure
        target.endure[0] += self.addEndure
        target += self.addProperty
        self.weight -= self.consume
        text = ""
        if(self.weight > 10.0 * self.consume):
            text = "，剩下的还可以饱餐一顿。"
        elif(self.weight > 5.0 * self.consume):
            text = "，还剩下不少。"
        elif(self.weight > 1.0 * self.consume):
            text = ", 这玩意快吃完了。"
        elif(self.weight > 0.0):
            text = "，还剩最后一口。"
        else:
            text = "，把" + self.name + "吃光了。"
        print(target.name + "吃起了" + self.name + text)
        if(self.weight <= 0.0):
            del usingList[usingList.index(self)]
            return False
        return target.getEatingValue()
        
class CProperty:
    def __init__(self,
                 conValue = 1.0,
                 armStrValue = 1.0,
                 legStrValue = 1.0,
                 touValue = 1.0,
                 intValue = 1.0,
                 wilValue = 1.0,
                 dexValue = 1.0,
                 senValue = 1.0,
                 recValue = 1.0,
                 bodyHeight = 1.0,
                 bodyWeight = 1.0):
        self.conValue = conValue
        self.armStrValue = armStrValue
        self.legStrValue = legStrValue
        self.touValue = touValue
        self.intValue = intValue
        self.wilValue = wilValue
        self.dexValue = dexValue
        self.senValue = senValue
        self.recValue = recValue
        self.bodyHeight = bodyHeight
        self.bodyWeight = bodyWeight
        self.hunger = [self.getHunger(), self.getHunger()]
        self.health = [self.getHealth(), self.getHealth()]
        self.injure = [0.0, self.getInjure()]
        self.endure = [self.getEndure(), self.getEndure(), self.getEndureMax()]
        self.paralysis = False

    #Assist Function
    def totalLevel(self):
        return self.conValue + self.armStrValue + self.legStrValue + self.touValue + self.intValue + self.wilValue + self.dexValue + self.senValue
    
    def initialize(self):
        self.endure[1] = self.getEndure()
        self.health[1] = self.getHealth()
        self.hunger[1] = self.getHunger()
        self.injure[1] = self.getInjure()
        self.endure[2] = self.getEndureMax()
        self.injure[0] = 0.0
        self.health[0] = self.health[1]
        self.hunger[0] = self.hunger[1]
        self.endure[0] = self.endure[1]
        
    def getDamage(self, attack, defend):
        if(attack < defend):
            return False
        else:
            return attack - defend

    def checkInPropertyRange(self):
        if(self.health[0] > self.health[1]):
            self.health[0] = self.health[1]
        if(self.endure[0] > self.endure[1]):
            self.endure[0] = self.endure[1]
        if(self.injure[0] < 0.0):
            self.injure[0] = 0.0
            
    def _outOfSight(self, spirit):
        if(CCalculate.outRangeCheck(spirit.x, spirit.y, self.x, self.y, pow(self.getSightValue(), 2))):
            return True
        else:
            return False
        
    def __add__(self, other):
        self.conValue += other.conValue
        self.armStrValue += other.armStrValue
        self.legStrValue += other.legStrValue
        self.touValue += other.touValue
        self.intValue += other.intValue
        self.wilValue += other.wilValue
        self.dexValue += other.dexValue
        self.senValue += other.senValue
        self.recValue += other.recValue
        self.bodyHeight += other.bodyHeight
        self.bodyWeight += other.bodyWeight
        return self

    def __mul__(self, other):
        self.conValue *= other.conValue
        self.armStrValue *= other.armStrValue
        self.legStrValue *= other.legStrValue
        self.touValue *= other.touValue
        self.intValue *= other.intValue
        self.wilValue *= other.wilValue
        self.dexValue *= other.dexValue
        self.senValue *= other.senValue
        self.recValue *= other.recValue
        self.bodyHeight *= other.bodyHeight
        self.bodyWeight *= other.bodyWeight
        return self
    
    def randomize(self):
        return CProperty(self.conValue * random.random(),
                         self.armStrValue * random.random(),
                         self.legStrValue * random.random(),
                         self.touValue * random.random(),
                         self.intValue * random.random(),
                         self.wilValue * random.random(),
                         self.dexValue * random.random(),
                         self.senValue * random.random(),
                         self.recValue * random.random(),
                         self.bodyHeight * random.random(),
                         self.bodyWeight * random.random())
    #END
        
    #Property Calculation Function
    def getHealthRecover(self):
        if(self.hunger[0] <= 0):
            return -1.0
        else:
            return self.recValue * self.hunger[0] / self.hunger[1] / 100.0

    def getInjureRecover(self):
        return self.recValue * self.recValue / 25.0

    def getEndureRecover(self):
        return self.recValue * self.recValue * self.hunger[0] / self.hunger[1] / 2.0

    def getEndureMax(self):
        return 5.0 * self.conValue * self.conValue * math.log(self.conValue + 5.0,  5.0)
    
    def getEndure(self):
        if(self.hunger[0] > self.hunger[1]):
            hungerEffect = pow(self.hunger[1] / self.hunger[0], 2)
        elif(self.hunger[0] <= 0.5 * self.hunger[1]):
            hungerEffect = (self.hunger[0] + self.wilValue * self.hunger[1] / 5.0) /( (1.0 + self.wilValue / 5.0) * self.hunger[1])
        else:
            hungerEffect = 1.0
        return self.getEndureMax() * ((self.health[0] + self.health[1])/(self.health[1] * 2.0)) *\
               (self.wilValue / 2.0 * self.injure[1] / (self.injure[0] + self.wilValue / 2.0 * self.injure[1])) * hungerEffect

    def getHealth(self):
        return 5.0 * self.conValue * self.conValue * math.log(self.conValue + 2.0, 2.0)

    def getInjure(self):
        return 5.0 * self.conValue * self.conValue

    def getHunger(self):
        return 10.0 * self.conValue

    def getAttackValue(self):
        return self.armStrValue * (self.endure[0] + self.endure[2]) / (2.0 * self.endure[2]) * (1 + 2.0 * random.random() * math.log(self.wilValue + 2.0, 2.0))

    def getDefendValue(self):
        return self.touValue

    def getAttackTime(self):
        return 10.0 / math.log(self.armStrValue + 5.0, 5.0) + 10.0 / math.log(self.dexValue + 5.0, 5.0) * (1.5 * self.endure[2])  / (self.endure[0] + 0.5 * self.endure[1])

    def getArmStrength(self):
        return self.armStrValue * (self.endure[0] + self.endure[2]) / (2.0 * self.endure[2])

    def getBodyStrength(self):
        return self.conValue * self.legStrValue * math.log(self.wilValue + 2.0, 2.0)

    def getMoveTime(self):
        return 10.0 / math.log(self.legStrValue + 5.0, 5.0) + 10.0 / math.log(self.dexValue + 5.0, 5.0) * (2.0 * self.endure[2])  / (self.endure[0] + self.endure[1])

    def getHitRate(self):
        return (self.endure[0] + self.endure[2]) / (self.endure[2] * 2.0) * self.wilValue * self.senValue

    def getDodgeRate(self):
        if(self.paralysis):
            return 0.0
        return (self.endure[0] + self.endure[2]) / (self.endure[2] * 2.0) * self.dexValue * self.senValue * 0.2

    def getFindwayValue(self):
        return int(math.log(self.intValue + 4.0, 2.0))

    def getSightValue(self):
        return int(math.log(self.senValue + 4.0, 2.0))

    def getLearnValue(self):
        return math.log(self.intValue + self.wilValue + 5.0, 5.0)

    def getCatchItemValue(self):
        return 10.0 / math.log(self.dexValue + 5.0, 5.0)

    def getEatingValue(self):
        return 20.0 / math.log(self.dexValue + 5.0, 5.0) * (self.hunger[0] + 10.0) / self.hunger[1]
    #END

    #Action Effect Function
    def moveEffect(self, distance):
        self.endure[0] -= 0.5 * distance
        self.hunger[0] -= 0.1 * distance
        self.legStrValue += 0.001 * distance
        self.conValue += 0.0001* distance

    def attackEffect(self, targetLevel):
        self.endure[0] -= 1.0 * targetLevel
        self.hunger[0] -= 0.2 * targetLevel
        self.armStrValue += 0.02 * targetLevel
        self.conValue += 0.005 * targetLevel
        self.dexValue += 0.005 * targetLevel
        self.senValue += 0.005 * targetLevel

    def attackedEffect(self, damage):
        if(damage >= 0):
            self.injure[0] += damage
            self.wilValue += 0.2 * damage / self.injure[1]
            self.touValue += 0.0001

    def dodgeEffect(self, enemyLevel):
        self.wilValue += 0.1 * enemyLevel
        self.dexValue += 0.1 * enemyLevel
        self.senValue += 0.1 * enemyLevel

    def recoverEffect(self):
        self.endure[1] = self.getEndure()
        self.health[1] = self.getHealth()
        self.hunger[1] = self.getHunger()
        self.injure[1] = self.getInjure()
        self.endure[0] += self.getEndureRecover()
        if(self.endure[0] > 0.001 * self.endure[1]):
            self.conValue += 0.000001 * self.endure[1] / self.endure[0]
            self.recValue += 0.000001 * self.endure[1] / self.endure[0]
            self.wilValue += 0.000001 * self.endure[1] / self.endure[0]
        else:
            self.conValue += 0.01
            self.recValue += 0.01
            self.wilValue += 0.01
        self.health[0] += self.getHealthRecover()
        if(self.health[0] > 0.001 * self.health[1]):
            self.conValue += 0.000001 * self.health[1] / self.health[0]
            self.recValue += 0.000001 * self.health[1] / self.health[0]
        else:
            self.conValue += 0.01
            self.recValue += 0.01
            self.wilValue += 0.01
        self.injure[0] -= self.getInjureRecover()
        self.conValue +=  0.0001 * self.injure[0] / self.injure[1]
        self.recValue +=  0.0001 * self.injure[0] / self.injure[1]
        self.wilValue +=  0.0001 * self.injure[0] / self.injure[1]
        self.touValue += 0.00001 * self.injure[0] / self.injure[1]
        if(self.injure[0] > self.injure[1]):
            self.health[0] -= self.injure[0] - self.injure[1]

        if(self.endure[0] < 0.0):
            self.health[0] -= self.endure[0]
            
        if(self.hunger[0] > 0.0):
            self.hunger[0] -= 0.1
        else:
            self.hunger[0] = -1.0
            self.wilValue += 0.01
        self.checkInPropertyRange()
        if(not self.paralysis):
            if(self.injure[0] > self.injure[1]):
                #print("%d knocked down"%(self.identity))
                if(self.invisible):
                    print(self.name + "重伤倒地")
                    self.paralysis = True
        else:
            if(self.injure[0] < self.injure[1]):
                #print("%d recovering"%(self.identity))
                if(self.invisible):
                    print(self.name + "艰难地从地上爬起")
                    self.paralysis = False
            
class CRace:
    def __init__(self, identity, name):
        self.identity = identity
        self.name = name

    def setProperty(self, longevity, startProperty, increaseProperty, maleProperty, femaleProperty):
        self.longevity = longevity
        self.startProperty = startProperty
        self.increaseProperty = increaseProperty
        self.sexProperty = [maleProperty, femaleProperty, CProperty()]

    def randomCreateProperty(self, age, sex):
        currentProperty = self.startProperty.randomize() * self.sexProperty[sex]
        for i in range(age):
            currentProperty += self.increaseProperty.randomize()
        return currentProperty
    
class CSpirit(CRigidbody, CProperty):
    def __init__(self, identity, imageName, x, y, mapFile, sex, age, race):
        CRigidbody.__init__(self, imageName, x, y, mapFile)
        CProperty.__init__(self)
        self.identity = identity
        self.mapFile[x][y].rigidbody = self
        self.dead = False
        self.invisible = False
        self.sex = sex
        self.age = age
        self.race = race
        self.nextMoveTime = 0.0
        self.item = []
        self.movable = True
        try:
            mapFile[x][y].spirit = self
        except IndexError:
            print("CSpirit maplist initialize out of range")

    def setPosition(self, x, y):
        if(self.mapFile[x][y].rigidbody):
            for i in range(1000):
                x = random.randint(1, len(self.mapFile))
                y = random.randint(1, len(self.mapFile[x]))
                if(not self.mapFile[x][y].rigidbody):
                    self.mapFile[x][y].rigidbody = self
        else:
            self.mapFile[x][y].rigidbody = self

    def createHumanBody(self):
        legMeat = CFood(self.name + "的肱二头肌",self.bodyWeight / 10.0, self.bodyHeight / 20.0, "meat", 0)
        legMeat.setIntroduction(self.name + "的胳膊肉。在圣文尼亚汀的世界里算是比较好吃的。")
        legMeat.setEffect(10, 0, 0, 10, CProperty(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1.0, 1.0).randomize(), 10.0)
        chestMeat = CFood(self.name + "的胸肌", self.bodyWeight / 3.0, self.bodyHeight / 6.0, "meat", 0)
        if(self.sex == 1 and self.race.identity == 0):
            chestMeat.setIntroduction(self.name + "的胸肌肉。有种令人向往的味道。")
        else:
            chestMeat.setIntroduction(self.name + "的胸肌肉。还是烹饪起来比较好的样子。")
        chestMeat.setEffect(5, 0, 0, 0, CProperty(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1.0, 1.0).randomize(), 5.0)
        self.addBodyPart("手部", [legMeat], self.getArmStrength())
        self.addBodyPart("身体", [chestMeat], self.getBodyStrength())
        
    #System Function
    def changeName(self, name):
        self.name = name
        
    def draw(self, cameraX, cameraY):
        CDrawingObject.draw(self, cameraX, cameraY, ".//res//image//spirit//" + self.imageName + ".gif")
        self.setText(cameraX, cameraY, self.name)
        self.text.setTextColor(color_rgb(min(255,int(255.0 * self.injure[0] / self.injure[1])), 0, 0))
    #END

    #Assist Function
    def moveTo(self, x, y):
        try:
            if(not CCalculate.checkInMapFile(x, y, self.mapFile) or self.mapFile[x][y].rigidbody != 0):
                return False
            else:
                self.mapFile[self.x][self.y].rigidbody = 0
                self.x = x
                self.y = y
                self.mapFile[x][y].rigidbody = self
                return True
        except IndexError:
            return False

    def _attack(self, target):
        try:
            hitValue = self.getHitRate() * random.random()
            dodgeValue = target.getDodgeRate() * random.random()
            if(hitValue > dodgeValue):
                value = self.getDamage(self.getAttackValue(), target.getDefendValue())
                self.attackEffect(1.0)
                target.attackedEffect(value)
                if(self.invisible and target.invisible):
                    if(target.paralysis):
                        talk = random.randrange(3)
                        if(talk == 0):
                            print(self.name + "狂笑着痛击倒在地上的" + target.name)
                        elif(talk == 1):
                            print(self.name + "用脚踩着" + target.name + "的脸， 哈哈大笑")
                        elif(talk == 2):
                            print(self.name + "任意地虐待着" + target.name)
                    elif(value < 0.1):
                        print(self.name + "的攻击对" + target.name + "完全无效！")
                    elif(value < 0.01 * target.injure[1]):
                        print(self.name + "攻击了" + target.name + "， 然而并没有什么卵用")
                    elif(value < 0.1 * target.injure[1]):
                        print(self.name + "的攻击擦伤了" + target.name)
                    elif(value < 0.3 * target.injure[1]):
                        print(self.name + "击中了" + target.name)
                    elif(value < 0.5 * target.injure[1]):
                        print(self.name + "狠狠地击中了" + target.name)
                    elif(value < 1.0 * target.injure[1]):
                        print(self.name + "的一击就让" + target.name + "浑身快散架了")
                    else:
                        print(self.name + "直接将" + target.name + "击倒在地，几乎失去反抗能力")
                return value
            else:
                if(self.invisible):
                    if(hitValue < 0.5 * dodgeValue):
                        print(target.name + "轻松地闪开" + self.name + "的攻击")
                    else:
                        print(target.name + "闪避了" + self.name + "的攻击")
                return 1
        except AttributeError:
            return -1
    #END

    #Basic Action Function
    def useItem(self, item, itemList):
        if(self.paralysis):
            self.nextMoveTime += self.getMoveTime()
            if(self.invisible):
                print(self.name + "拿着" + item.name + "，却因为伤势而没办法使用它。")
            return False
        try:
            item.using(self, itemList)
        except ValueError:
            return False
        if(item in itemList):
            return True
        return False
    
    def catchItem(self, item, originList):
        if(self.paralysis):
            self.nextMoveTime += self.getMoveTime()
            if(self.invisible):
                print(self.name + "把手艰难地伸向" + item.name + "但在重伤之下却以失败告终。")
            return False
        for i in self.bodyPart:
            if(i.name == "手部"):
                del originList[originList.index(item)]
                i.equiping(item)
                self.nextMoveTime += self.getCatchItemValue()
                print(self.name + "抓起了" + item.name + "。")
                return False
        if(self.invisible):
            print(self.name + "想用手抓起" + item.name + "，然而却并没有手。")
        return False
        
    def move(self, direction):
        if(self.paralysis):
            self.nextMoveTime += self.getMoveTime()
            if(self.invisible):
                print(self.name + "挣扎着想爬起来，但是却又虚弱地倒在了地上。")
            return False
        #print("%d moving"%(self.identity))
        if(self.moveTo(self.x + direction.dx, self.y + direction.dy)):
            t = CCalculate.powNSqrt(direction.dx, direction.dy)
            if(t >= 0.01):
                self.moveEffect(t)
                self.nextMoveTime += t * self.getMoveTime()
                return True
            else:
                self.nextMoveTime += self.getMoveTime()
                return False
        else:
            self.nextMoveTime += self.getMoveTime()
            return False
      
    def attack(self, direction):
        if(self.paralysis):
            self.nextMoveTime += self.getMoveTime()
            if(self.invisible):
                print(self.name + "发出了愤怒的吼叫，却只能在地上无力地挣扎。")
            return False
        success = False
        x = self.x + direction.dx
        y = self.y + direction.dy
        t = 0
        try:
            if(self.mapFile[x][y].rigidbody != 0):
                t = self._attack(self.mapFile[x][y].rigidbody)
                if(t >= 0):
                    try:
                        self.mapFile[x][y].rigidbody.affectionList[self.identity] -= 10
                    except AttributeError:
                        pass
                    except KeyError:
                        self.mapFile[x][y].rigidbody.addAffection(self, -50)
                success = True
        except IndexError:
            pass
        self.nextMoveTime += self.getAttackTime()
        return success


class CNPC(CSpirit):
    def __init__(self, identity, name, x, y, mapFile, spiritList, sex, age, race):
        CSpirit.__init__(self, identity, name, x, y, mapFile, sex, age, race)
        self.spiritList = spiritList
        self.affectionList = {}
        self.attackTarget = 0
        self.followTarget = 0
        self.aiFlag = 0 #the way of AI, 0 is standstill,
                        #1 is random moving without attack or follow consciously
                        #2 is more attacking, 3 is more following,
                        #4 is a balance movement
        
    def addAffection(self, targetSpirit, affectionValue):
        self.affectionList[targetSpirit.identity] = affectionValue

        
    def _findTarget(self):
        maxHate = 0
        #print("%d finding targets"%(self.identity))
        for i in range(-self.getSightValue() + 1, self.getSightValue()):
            for j in range(-self.getSightValue() + 1, self.getSightValue()):
                if((not CCalculate.outRangeCheck(i, j, 0, 0, pow(self.getSightValue(), 2)))\
                   and CCalculate.checkInMapFile(self.x + i, self.y + j, self.mapFile)\
                   and self.mapFile[self.x + i][self.y + j].rigidbody):
                    try:
                        target = self.mapFile[self.x + i][self.y + j].rigidbody.identity                         
                    except AttributeError:
                        continue
                    try:
                        if(self.affectionList[target] < maxHate):
                            self.attackTarget = self.spiritList[target]
                            maxHate = self.affectionList[target]
                    except KeyError:
                        if(self.spiritList[target].race != self.race):
                            self.addAffection(self.spiritList[target], -10)
                        continue
        return maxHate
                    
    def AI_update(self):
        if(self.dead):
            return
        if(self.health[0] < 0):
            self.dead = True
            self.mapFile[self.x][self.y].rigidbody = 0
            if(self.invisible):
                print(self.name + "死掉了……")
            #print(self.name + "die")
            self.destroyed()
            self.undraw()
            del self
            return
        if(self.attackTarget):
            if(self._outOfSight(self.attackTarget) or self.attackTarget.dead):
                self.attackTarget = 0
                self._findTarget()
            elif(self.attackTarget.paralysis):
                self._findTarget()
        if(self.aiFlag == 0):
            #print("in ai0")
            self.AI_0()
        elif(self.aiFlag == 1):
            #print("in ai1")
            self.AI_1()
        elif(self.aiFlag == 2):
            #print("in ai2")
            self.AI_2()
        elif(self.aiFlag == 3):
            #print("in ai3")
            self.AI_3()
        elif(self.aiFlag == 4):
            #print("in ai4")
            self.AI_4()
        self.recoverEffect()
            
    def AI_0(self):
        self.move(DIRECTION[5])

    def AI_1(self):
        self.move(DIRECTION[random.randint(1,9)])

    def AI_2(self):
        if(self.attackTarget):
            if(-2 < self.attackTarget.x - self.x < 2 and -2 < self.attackTarget.y - self.y < 2):
                self.attack(CDirection(self.attackTarget.x - self.x, self.attackTarget.y - self.y))
            else:
                self.move(CCalculate.findWay(self.mapFile, self.x, self.y, self.attackTarget.x, self.attackTarget.y, self.getFindwayValue()))
        else:
            if(self._findTarget() < 0):
                self.AI_2()
            else:
                self.AI_3()

    def AI_3(self):
        if(self.followTarget):
            if(self._outOfSight(self.followTarget)):
                self.AI_1()
            else:
                self.move(CCalculate.findWay(self.mapFile, self.x, self.x, self.followTarget.x, self.followTarget.y, self.getFindwayValue()))
        else:
            self.AI_1()
        
    def AI_4(self):
        i = random.randint(0,1)
        if(i == 0):
            self.AI_3()
        else:
            self.AI_2()
        
class CHero(CSpirit):
    cameraX = 0
    cameraY = 0
    def __init__(self, x, y, mapFile, sex, age, race):
        CSpirit.__init__(self, 0, heroName, x, y, mapFile, sex, age, race)
        cameraX = self.x
        cameraY = self.y
        self.name = "你"

    def mouseControl(self, mx, my, function, var1):
        t = False
        if(function == self.move):
            if(var1):
                if(var1 == "休息"):
                    function(CDirection(0, 0))
                    for i in range(2):
                        self.recoverEffect()
                    return True
                else:
                    mx = var1.x
                    my = var1.y
            result = CCalculate.findWay(self.mapFile, self.x, self.y, mx, my, self.getFindwayValue())
            t = function(result)
            if(self.x == mx and self.y == my):
                t = False
        elif(function == self.attack):
            if(var1):
                time.sleep(0.2)
            t = (function(CDirection(mx - self.x, my - self.y).surround()) and var1)
        elif(function == self.useItem):
            return (function(mx, my) and var1)
        elif(function == self.catchItem):
            function(mx, my)
        self.recoverEffect()
        gameTime = self.nextMoveTime
        cameraX = self.x
        cameraY = self.y
        return t
        
    def checkMouse(self):
        q = win.checkMouse()
        if(not q):
            return False
        mx, my = self.x + CCalculate.mouseTMap(q).dx,  self.y + CCalculate.mouseTMap(q).dy
        var1 = 0
        enable = []
        if(CCalculate.checkInMapFile(mx, my, self.mapFile)):
            if(self.mapFile[mx][my].item !=[] and abs(mx - self.x) < 2 and abs(my - self.y) < 2):
                enable = [2, 8]
            try:
                if(self.mapFile[mx][my].rigidbody.identity == 0):
                    enable += [6, 7]
                elif(abs(mx - self.x) < 2 and abs(my - self.y) < 2):
                    enable = [0, 1, 3, 4]
                else:
                    enable = [0, 2, 3, 5]
            except AttributeError:
                pass
            if(enable != []):
                checkButton = CTargetButtonGroup(win, q, enable)
                theType = checkButton.clicked(win.getMouse())
                if(theType == "攻击"):
                    function = self.attack
                    var1 = False #Single attack
                elif(theType == "移动"):
                    function = self.move
                elif(theType == "调查"):
                    consider = CRaceConsider(self.mapFile[mx][my].rigidbody.race)
                    del checkButton
                    win.update()
                    return False
                elif(theType == "debug"):
                    print("starting debug")
                    Tdebug = CConditionDisplay(self.mapFile[mx][my].rigidbody)
                    Tdebug.win.getMouse()
                    Tdebug.win.close()
                    del Tdebug
                    del checkButton
                    win.update()
                    return False
                elif(theType == "连续攻击"):
                    function = self.attack
                    var1 = True
                elif(theType == "跟踪"):
                    function = self.move
                    var1 = self.mapFile[mx][my].rigidbody
                elif(theType == "停止"):
                    function = self.move
                elif(theType == "休息"):
                    function = self.move
                    var1 = "休息"
                elif(theType == "拾取"):
                    itemDisplay = CItemDisplay(self.mapFile[mx][my].item, "地上", [0], self)
                    result = itemDisplay.getMouse()
                    itemDisplay.quit()
                    return result
                else:
                    del checkButton
                    win.update()
                    return False
            else:
                function = self.move
        else:
            function = self.move
        return mx, my, function, var1

    def moveTo(self, x, y):
        t = CSpirit.moveTo(self, x, y)
        CHero.cameraX = self.x
        CHero.cameraY = self.y
        return t

    def move(self, direction):
        t = CSpirit.move(self, direction)
        CHero.cameraX = self.x
        CHero.cameraY = self.y
        return t

    @staticmethod
    def load():
        try:
            heroFile = open("sav//hero.sav", 'rb')
            t = pickle.load(heroFile)
            heroFile.close()
            return t
        except FileNotFoundError:
            return False      
