#Sanvenirtin
#roguelike game
#programming by Sanvenir
#ver 0.0.1
#main file
#executing this:)
#class imageimageNamed as CExampleClass
#function imageimageNamed as exampleFunction
#var imageimageNamed as exampleVar
#const imageimageNamed as EXAMPLE_CONST

from scene import *
from gui import *
def main():
    mainMap = CMainMap.load()
    if(mainMap):
        pass
    else:
        mainMap = CMainMap()
        mainMap.randomCreateMap(mainMapWidth, mainMapHeight, 20, 50, 100, 5, 20)
        mainMap.randomCreateTown(100)
        mainMap.save()
    print(mainMap.width)
    race = []
    try:
        raceFile = open("sav//character//race.sav", 'rb')
        race = pickle.load(raceFile)
    except FileNotFoundError:
        race.append(CRace(0, "人类"))
        startProperty = CProperty(30.0, 30.0, 30.0, 1.0, 30.0, 30.0, 30.0, 30.0, 30.0, 100.0, 30.0)
        increaseProperty = CProperty(1.0, 1.0, 1.0, 0.1, 1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 2.0)
        maleProperty = CProperty(1.5, 1.2, 1.2, 1.5, 0.8, 1.0, 0.8, 0.8, 1.0, 1.5, 1.5)
        femaleProperty = CProperty(0.8, 0.9, 0.9, 0.8, 1.5, 1.0, 1.5, 1.5, 1.0, 0.8, 0.8)
        race[0].setProperty(30, startProperty, increaseProperty, maleProperty, femaleProperty)
        for i in range(150):
            randomAddRace(race, random.randint(1, 20))
    hero = CHero.load()
    if(not hero):
        localMap = mainMap.loadLocalMap(0, 0)
        hero = CHero(10, 10, localMap.mapFile, 0, 100, race[0])
        hero += hero.race.randomCreateProperty(hero.age, hero.sex)
        hero.createHumanBody()
        hero.initialize()
        hero.mainX = 0
        hero.mainY = 0
    else:
        localMap = mainMap.loadLocalMap(hero.mainX, hero.mainY)
    conditionDisplay = CConditionDisplay(hero)
    inventoryDisplay = CEquipmentDisplay(hero)
    gameScene = CGameScene(hero.x, hero.y, localMap, race, hero, conditionDisplay)
    gameScene.draw()
    gameContinue = True
    gameMap = CMapShow(mainMap)
    print("地图绘制中......")
    gameMap.draw()
    print("绘制完毕")
    gameMap.update(hero.mainX, hero.mainY)
    mainWin = False
    win.update()
    try:
        while (gameContinue):
            passing = False
            mainWin = hero.checkMouse()
            equipWin = inventoryDisplay.checkMouse()
            if(mainWin):
                mx, my, function, var1 = mainWin
                passing = True
            if(equipWin):
                mx, my, function, var1 = equipWin
                passing = True
            while(passing):
                passing = hero.mouseControl(mx, my, function, var1)
                gameScene.update()
                gameScene.draw()
                win.update()
                if(win.checkMouse()):
                    passing = False
                if(gameScene.mapFile[hero.x][hero.y].checkTransform()):
                    nx, ny = gameScene.mapFile[hero.x][hero.y].transformMap
                    sx, sy = gameScene.mapFile[hero.x][hero.y].transform
                    passing = False
                    try:
                        gameMap.update(nx, ny)
                    except GraphicsError:
                        gameMap = CMapShow(mainMap)
                        gameMap.draw()
                        gameMap.update(nx, ny)
                    gameScene.undraw()
                    del gameScene
                    localMap.save()
                    localMap = mainMap.loadLocalMap(nx, ny)
                    gameScene = CGameScene(sx, sy, localMap, race, hero, conditionDisplay)
                    gameScene.update()
                    gameScene.draw()
                    win.update()
                if(gameScene.hero.health[0] < 0):
                    passing = False
                    gameContinue = False
                    print("你死了，游戏结束了")
                    try:
                        os.remove("sav//hero.sav")
                    except FileNotFoundError:
                        print("未存储角色信息")
        win.getMouse()
    except GraphicsError:
        print("角色数据存储中……")
        hero.reset()
        hero.mainX = localMap.x
        hero.mainY = localMap.y
        del hero.mapFile
        heroFile = open("sav//hero.sav", 'wb')
        pickle.dump(hero, heroFile)
        heroFile.close()
        print("存储完毕")
        pass
    finally:
        for i in windows:
            try:
                i.close()
            except:
                pass

def randomAddRace(race, level):
    identity = len(race)
    foreName = random.randrange(2)
    name = ""
    if(foreName == 0):
        for i in range(random.randint(2, 5)):
            name += randomMaleNameList[random.randrange(len(randomMaleNameList))]
    elif(foreName == 1):
        for i in range(random.randint(2, 5)):
            name += randomFemaleNameList[random.randrange(len(randomFemaleNameList))]
    name += randomMonsterNameList[random.randrange(len(randomMonsterNameList))]
    startProperty = CProperty().randomize()
    increaseProperty = CProperty().randomize()
    for i in range(level):
        for j in range(5):
            startProperty += CProperty().randomize()
        increaseProperty += CProperty().randomize()
    maleProperty = CProperty().randomize() + CProperty().randomize()
    femaleProperty = CProperty().randomize() + CProperty().randomize()
    race.append(CRace(identity, name))
    race[identity].setProperty(random.randint(1, 30), startProperty, increaseProperty, maleProperty, femaleProperty)
    raceFile = open("sav//character//race.sav", 'wb')
    pickle.dump(race, raceFile)
    raceFile.close()

main()

    
