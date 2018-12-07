#Sanvenirtin
#roguelike game
#programming by Sanvenir
#ver 0.0.2a
#gui file
#Including gui elements

from config import *

class CTextBlock:
    def __init__(self, text, width, rawDistance, anchorPoint):
        self.context = text
        self.width = width
        self.rawDistance = rawDistance
        self.anchorPoint = anchorPoint
        i = 0
        j = -1
        textGroup = []
        self.text = []
        for i in range(len(text)):
            if(not (i % width)):
                textGroup.append("")
                j += 1
            textGroup[j] += text[i]
        for i in textGroup:
            self.text.append(Text(anchorPoint, i))
        self.raw = len(self.text)
        for i in range(self.raw):
            dy = -(float(i) - float(self.raw) / 2.0) * rawDistance
            self.text[i].move(0.0, dy)

    def setText(self, text):
        self.__init__(self, text, self.width, self.rawDistance, self.anchorPoint)

    def getText(self):
        return self.context

    def getAnchor(self):
        return self.anchor

    def setSize(self, point):
        for i in self.text:
            i.setSize(point)

    def setTextColor(self, color):
        for i in self.text:
            i.setTextColor(color)

    def move(self, dx, dy):
        for i in self.text:
            i.move(dx, dy)
        self.anchorPoint.move(dx, dy)

    def draw(self, win):
        for i in self.text:
            i.draw(win)

    def undraw(self):
        for i in self.text:
            i.undraw()
            
class CImageButton:
    def __init__(self, win, anchorPoint, side, imagePath):
        self.win = win
        self.shell = Rectangle(Point(anchorPoint.getX() - side / 2.0, anchorPoint.getY() - side / 2.0), Point(anchorPoint.getX() + side / 2.0, anchorPoint.getY() + side / 2.0))
        self.shell.setFill("white")
        self.imagePath = imagePath
        self.image = Image(self.shell.getCenter(), imagePath)
        self.visible = False

    def move(self, dx, dy):
        self.shell.move(dx, dy)
        self.image.move(dx, dy)

    def draw(self):
        self.shell.draw(self.win)
        self.image.draw(self.win)
        self.visible = True

    def undraw(self):
        self.shell.undraw()
        self.image.undraw()
        self.visible = False

    def clicked(self, q):
        if(not self.visible):
            return False
        if(self.shell.getP1().getX() < q.getX() < self.shell.getP2().getX() and self.shell.getP1().getY() < q.getY() < self.shell.getP2().getY()):
            return True
        else:
            return False
        
class CRectangleButton:
    def __init__(self, win, p1, p2, text, color, textColor):
        self.win = win
        self.shell = Rectangle(p1, p2)
        self.shell.setFill(color)
        self.text = Text(self.shell.getCenter(), text)
        self.text.setTextColor(textColor)
        self.visible = False

    def move(self, dx, dy):
        self.shell.move(dx, dy)
        self.text.move(dx, dy)

    def draw(self):
        self.shell.draw(self.win)
        self.text.draw(self.win)
        self.visible = True

    def undraw(self):
        self.shell.undraw()
        self.text.undraw()
        self.visible = False

    def clicked(self, q):
        if(not self.visible):
            return False
        if(self.shell.getP1().getX() < q.getX() < self.shell.getP2().getX() and self.shell.getP1().getY() < q.getY() < self.shell.getP2().getY()):
            return True
        else:
            return False

class CTargetButtonGroup:
    def __init__(self, win, anchorPoint, enable = [0, 1, 2]):
        self.win = win
        color = color_rgb(30, 30, 200)
        textColor = color_rgb(200, 200, 30)
        self.button = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        p1 = Point(anchorPoint.getX() - actionButtonSize, anchorPoint.getY() - actionButtonSize)
        p2 = Point(anchorPoint.getX() + actionButtonSize, anchorPoint.getY() + actionButtonSize)
        self.button[0] = CRectangleButton(self.win, p1, p2, "调查", color, textColor)
        self.button[1] = CRectangleButton(self.win, p1, p2, "攻击", color, textColor)
        self.button[2] = CRectangleButton(self.win, p1, p2, "移动", color, textColor)
        self.button[3] = CRectangleButton(self.win, p1, p2, "debug", color, textColor)
        self.button[4] = CRectangleButton(self.win, p1, p2, "连续攻击", color, textColor)
        self.button[5] = CRectangleButton(self.win, p1, p2, "跟踪", color, textColor)
        self.button[6] = CRectangleButton(self.win, p1, p2, "停止", color, textColor)
        self.button[7] = CRectangleButton(self.win, p1, p2, "休息", color, textColor)
        self.button[8] = CRectangleButton(self.win, p1, p2, "拾取", color, textColor)
        self.button[0].move( actionButtonDistance, 0.0)
        self.button[1].move(-actionButtonDistance, 0.0)
        self.button[2].move(0.0, 0.0)
        self.button[3].move( 0.0, actionButtonDistance)
        self.button[4].move( 0.0,-actionButtonDistance)
        self.button[5].move( 0.0,-actionButtonDistance)
        self.button[6].move(0.0, 0.0)
        self.button[7].move( actionButtonDistance, 0.0)
        self.button[8].move(-actionButtonDistance, 0.0)
        for i in enable:
            self.button[i].draw()

    def __del__(self):
        for i in range(len(self.button)):
            self.button.pop().undraw()

    def clicked(self, q):
        TheType = False
        for i in self.button:
            if(i.clicked(q)):
                TheType = i.text.getText()
                break
        del self
        return TheType
        
class CEquipmentDisplay:
    def __init__(self, target):
        try:
            name = target.name
        except AttributeError:
            pass
        color = "white"
        textColor = "black"
        self.win = GraphWin(target.name + "的装备", 500, 50, False, 100, 50)
        self.win.setCoords(-1.0, 10.0, 11.0, 0.0)
        self.equipButton = []
        self.target = target
        self.total = len(target.bodyPart)
        self.itemDisplay = False
        self.open = False
        for i in range(self.total):
            self.equipButton.append(CRectangleButton(self.win, Point(float(i) - 0.5, 1.0), Point(float(i) + 0.5, 9.0), target.bodyPart[i].name, color, textColor))
            self.equipButton[i].draw()
            
    def checkMouse(self):
        q = self.win.checkMouse()
        if(q):
            for i in range(self.total):
                if(self.equipButton[i].clicked(q)):
                    self.itemDisplay = CItemDisplay(self.target.bodyPart[i].equipment, self.target.bodyPart[i].name + "装备", [1, 2, 3], self.target, 100, 100)
                    self.open = True
                    break
        if(self.open):
            result = self.itemDisplay.getMouse()
            if(result):
                return result
            else:
                self.open = False
                self.itemDisplay.quit()
                return False
        return False

class CItemDisplay:
    def __init__(self, item, name, enable, hero, positionX = 800, positionY = 400):
        self.total = len(item)
        self.item = item
        self.enable = enable
        self.width = int(math.sqrt(self.total)) + 2
        self.height = int(self.total / self.width) + 2
        self.win = GraphWin(name + "的物品", 100 * self.width, 100 * self.height, False, positionX, positionY)
        Text(Point(50 * self.width, 10), name + "的物品").draw(self.win)
        self.win.undrawTitle("yellow1")
        self.win.setCoords(-1, self.height, self.width, -1)
        self.hero = hero
        x = 0
        y = 0
        self.itemButton = []
        for i in range(self.total):
            self.itemButton.append(CImageButton(self.win, Point(x, y), 1.0, item[i].imageName))
            self.itemButton[i].draw()
            x += 1
            if(x > self.width):
                y += 1
                x = 0
        self.win.update()
        
    def update(self):
        for i in range(self.total):
            self.itemButton[0].undraw()
            del self.itemButton[0]
        self.total = len(self.item)
        x = 0
        y = 0
        self.itemButton = []
        for i in range(self.total):
            self.itemButton.append(CImageButton(self.win, Point(x, y), 1.0, self.item[i].imageName))
            self.itemButton[i].draw()
            x += 1
            if(x > self.width):
                y += 1
                x = 0
        self.win.update()
        

    def getMouse(self):
        self.update()
        q = self.win.getMouse()
        for i in range(self.total):
            result = self.itemButton[i].clicked(q)
            if(result):
                self.itemConsider = CItemConsider(self.item[i], self.enable)
                result2 = self.itemConsider.getMouse()
                if(not result2):
                    self.itemConsider.quit()
                    return False
                functionType, tItem =  result2
                if(functionType == "使用一次"):
                    self.itemConsider.quit()
                    return tItem, self.item, self.hero.useItem, False
                elif(functionType == "全部使用"):
                    self.itemConsider.quit()
                    return tItem, self.item, self.hero.useItem, True
                elif(functionType == "拿取"):
                    self.itemConsider.quit()
                    return tItem, self.item, self.hero.catchItem, True
                else:
                    return False
        return False

    def quit(self):
        self.win.close()
        
    

class CItemConsider:
    def __init__(self, item, enable, positionX = 500, positionY = 200):
        self.item = item
        self.win = GraphWin(item.name + "的基本情况", 300, 300, False, positionX, positionY)
        self.win.undrawTitle("green1")
        self.win.setCoords(0.0, 0.0, 20.0, 20.0)
        self.nameText = Text(Point(10.0, 18.0), item.name)
        self.informationText = Text(Point(10.0, 16.0), "重量 " + str(int(item.weight)))
        self.introductionText = CTextBlock(item.introduction, 15, 2.0, Point(10.0, 10.0))
        p1 = Point(8.0, 4.0)
        p2 = Point(12.0, 6.0)
        color = color_rgb(200, 200, 0)
        textColor = color_rgb(0, 0, 200)
        self.enable = enable
        self.button = [0, 1, 2, 3]
        self.button[0] = CRectangleButton(self.win, p1, p2, "拿取", color, textColor)
        self.button[1] = CRectangleButton(self.win, p1, p2, "使用一次", color, textColor)
        self.button[2] = CRectangleButton(self.win, p1, p2, "全部使用", color, textColor)
        self.button[3] = CRectangleButton(self.win, p1, p2, "投掷", color, textColor)
        self.button[0].move( 0.0, 0.0)
        self.button[1].move(-4.0, 0.0)
        self.button[2].move( 4.0, 0.0)
        self.button[3].move( 0.0, 2.0)
        for i in enable:
            self.button[i].draw()
        self.nameText.draw(self.win)
        self.informationText.draw(self.win)
        self.introductionText.draw(self.win)
        self.win.update()

    def update(self):
        self.informationText.setText("重量 " + str(int(self.item.weight)))
        self.win.update()
            
    def getMouse(self):
        q = self.win.getMouse()
        result1 = False
        for i in self.enable:
            result = self.button[i].clicked(q)
            if(result):
                return self.button[i].text.getText(), self.item
        self.update()

    def quit(self):
        for i in range(len(self.button)):
            del self.button[0]
        self.win.close()
        
            
        
class CDirectionButtonGroup:
    def __init__(self, win, anchorPoint):
        self.win = win
        p1 = Point(anchorPoint.getX() - actionButtonSize, anchorPoint.getY() - actionButtonSize)
        p2 = Point(anchorPoint.getX() + actionButtonSize, anchorPoint.getY() + actionButtonSize)
        color = color_rgb(100, 50, 50)
        textColor = color_rgb(0, 200, 200)
        self.button = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.button[8] = CRectangleButton(self.win, p1, p2, "上", color, textColor)
        self.button[8].move( 0.0, actionButtonDistance)
        self.button[9] = CRectangleButton(self.win, p1, p2, "右上", color, textColor)
        self.button[9].move( actionButtonDistance, actionButtonDistance)
        self.button[6] = CRectangleButton(self.win, p1, p2, "右", color, textColor)
        self.button[6].move( actionButtonDistance, 0.0)
        self.button[3] = CRectangleButton(self.win, p1, p2, "右下", color, textColor)
        self.button[3].move( actionButtonDistance,-actionButtonDistance)
        self.button[2] = CRectangleButton(self.win, p1, p2, "下", color, textColor)
        self.button[2].move( 0.0,-actionButtonDistance)
        self.button[1] = CRectangleButton(self.win, p1, p2, "左下", color, textColor)
        self.button[1].move(-actionButtonDistance,-actionButtonDistance)
        self.button[4] = CRectangleButton(self.win, p1, p2, "左", color, textColor)
        self.button[4].move(-actionButtonDistance, 0.0)
        self.button[7] = CRectangleButton(self.win, p1, p2, "左上", color, textColor)
        self.button[7].move(-actionButtonDistance, actionButtonDistance)
        self.button[5] = CRectangleButton(self.win, p1, p2, "中", color, textColor)
        for i in self.button[1:]:
            i.draw()
            
        
class CRaceConsider:
    def __init__(self, race):
        self.win = GraphWin(race.name + "种族的情报", 300, 200, 200, 200)
        self.win.undrawTitle("white")
        self.win.setCoords(0.0, 0.0, 15.0, 10.0)
        if(race.name == "人类"):
            text = "人族。你的同类，和你自己的属性差不多。"
        else:
            text = race.name + "族，寿命在" + str(race.longevity) + "年左右，"
            total = race.startProperty.totalLevel()
            if(total < 50.0):
                text += "不是一般的弱，"
            elif(total < 100.0):
                text += "几乎没有威胁，"
            elif(total < 200.0):
                text += "略弱于人类，"
            elif(total < 300.0):
                text += "与人类体质相近，"
            elif(total < 400.0):
                text += "非常危险，建议不要招惹，"
            elif(total < 500.0):
                text += "几乎能轻松虐杀人类的种族，"
            else:
                text += "这是个挂逼！一定是个挂逼种族！"
            mTotal = race.sexProperty[0].totalLevel()
            fTotal = race.sexProperty[1].totalLevel()
            eTotal = race.sexProperty[2].totalLevel()
            if(mTotal < fTotal):
                text += "雄性比较强一些"
            else:
                text += "似乎女性是其中的统治者"
            if(mTotal < eTotal and fTotal < eTotal):
                text += "， 不过天下还是秀吉的。"
            else:
                text += "。"
        self.context = CTextBlock(text, 10, 1.0, Point(7.5, 5.0))
        self.context.draw(self.win)
        self.win.getMouse()
        self.win.close()
        del self
        
class CConditionDisplay:
    def __init__(self, hero):
        self.win = GraphWin(hero.name + "的属性表", 300, 400, False, 200, 150)
        self.win.undrawTitle("white")
        self.win.setCoords(0.0, 0.0, 15.0, 24.0)
        self.timeText = Text(Point(7.5, 22.0), "下一动作时间:" + str(hero.nextMoveTime))
        self.timeText.draw(self.win)
        self.positionText = Text(Point(7.5, 10.0), "位置   " + str(hero.x) + "   " + str(hero.y) + "   ID   " + str(hero.identity))
        self.positionText.draw(self.win)
        self.healthText = Text(Point(7.5, 8.0), "生命力：" + str(int(hero.health[0])) + "/" + str(int(hero.health[1])))
        self.healthText.draw(self.win)
        self.endureText = Text(Point(7.5, 6.0), "耐力：" + str(int(hero.endure[0])) + "/" + str(int(hero.endure[1])) + "/" + str(int(hero.endure[2])))
        self.endureText.draw(self.win)
        self.hungerText = Text(Point(7.5, 4.0), "饥饿度：" + str(int(hero.hunger[0])) + "/" + str(int(hero.hunger[1])))
        self.hungerText.draw(self.win)
        self.injureText = Text(Point(7.5, 2.0), "伤残度：" + str(int(hero.injure[0])) + "/" + str(int(hero.injure[1])))
        self.injureText.draw(self.win)
        self.conValue = Text(Point(7.5, 20.0), "conValue" + str(hero.conValue))
        self.conValue.draw(self.win)
        self.armStrValue = Text(Point(7.5, 19.0), "armStrValue" + str(hero.armStrValue))
        self.armStrValue.draw(self.win)
        self.legStrValue = Text(Point(7.5, 18.0), "legStrValue" + str(hero.legStrValue))
        self.legStrValue.draw(self.win)
        self.touValue = Text(Point(7.5, 17.0), "touValue" + str(hero.touValue))
        self.touValue.draw(self.win)
        self.intValue = Text(Point(7.5, 16.0), "intValue" + str(hero.intValue))
        self.intValue.draw(self.win)
        self.wilValue = Text(Point(7.5, 15.0), "wilValue" + str(hero.wilValue))
        self.wilValue.draw(self.win)
        self.dexValue = Text(Point(7.5, 14.0), "dexValue" + str(hero.dexValue))
        self.dexValue.draw(self.win)
        self.senValue = Text(Point(7.5, 13.0), "senValue" + str(hero.senValue))
        self.senValue.draw(self.win)
        self.recValue = Text(Point(7.5, 12.0), "recValue" + str(hero.recValue))
        self.recValue.draw(self.win)

    def update(self, hero):
        self.timeText.setText("下一动作时间:" + str(hero.nextMoveTime))
        self.positionText.setText("位置   " + str(hero.x) + "    " + str(hero.y) + "   ID   " + str(hero.identity))
        self.healthText.setText("生命力：" + str(int(hero.health[0])) + "/" + str(int(hero.health[1])))
        self.endureText.setText("耐力：" + str(int(hero.endure[0])) + "/" + str(int(hero.endure[1])) + "/" + str(int(hero.endure[2])))
        self.hungerText.setText("饥饿度：" + str(int(hero.hunger[0])) + "/" + str(int(hero.hunger[1])))
        self.injureText.setText("伤残度：" + str(int(hero.injure[0])) + "/" + str(int(hero.injure[1])))
        self.conValue.setText("conValue" + str(hero.conValue))
        self.armStrValue.setText("armStrValue" + str(hero.armStrValue))
        self.legStrValue.setText("legStrValue" + str(hero.legStrValue))
        self.touValue.setText("touValue" + str(hero.touValue))
        self.intValue.setText("intValue" + str(hero.intValue))
        self.wilValue.setText("wilValue" + str(hero.wilValue))
        self.dexValue.setText("dexValue" + str(hero.dexValue))
        self.senValue.setText("senValue" + str(hero.senValue))
        self.recValue.setText("recValue" + str(hero.recValue))
        
class CMapShow:
    def __init__(self, mainMap):
        self.width = mainMap.width
        self.height = mainMap.height
        self.mainMap = mainMap
        self.win = GraphWin("大地图", 800, 800, False, 300, 100)
        self.win.master.iconify()
        self.win.setCoords(-5.0, -5.0, self.width + 5.0, self.height + 5.0)

    def draw(self):
        self.win.setBackground("grey")
        for x in range(self.width):
            for y in range(self.height):
                mapType = self.mainMap.mainMap[x][y].mapType
                self.win.plot(x, y, MAPCOLORSET[mapType])
        for i in self.mainMap.town:
            Text(Point(i.x, i.y + 0.5), i.name).draw(self.win)
        self.win.update()

    def update(self, hx, hy):
        try:
            self.nowPosition.undraw()
            del self.nowPosition
        except AttributeError:
            pass
        self.nowPosition = Circle(Point(hx, hy), 2)
        self.nowPosition.setFill("black")
        self.nowPosition.draw(self.win)
        
        
        
