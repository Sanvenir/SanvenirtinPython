#Sanvenirtin
#roguelike game
#programming by Sanvenir
#ver 0.0.6
#Drawing file
#Including drawing classes and functions

from config import *

class CDrawingObject:
    def __init__(self, imageName, x, y):
        self.x = x
        self.y = y
        self.imageName = imageName
        self.imagePath = ""

    def draw(self, cameraX, cameraY, imagePath):
        self.imagePath = imagePath
        dx = self.x - cameraX
        dy = self.y - cameraY
        try:
            self.undraw()
            self.image = Image(Point(dx, dy),imagePath)
            self.image.draw(win)
        except tk.TclError:
            print("Not found CSpirit image")

    def reset(self):
        try:
            del self.image
        except AttributeError:
            pass
        try:
            del self.text
        except AttributeError:
            pass
        
    def undraw(self):
        try:
            self.image.undraw()
            del self.image
        except AttributeError:
            return

    def setText(self, cameraX, cameraY, text):
        try:
            self.text.undraw()
            del self.text
        except AttributeError:
            self.text = 0
        dx = self.x - cameraX
        dy = self.y - cameraY + 1.0
        self.text = Text(Point(dx, dy), text)
            
class CGround(CDrawingObject):
    def __init__(self, imageName, x, y, mapType):
        CDrawingObject.__init__(self, imageName, x, y)
        self.mapType = mapType

    def changeImage(self, imageName):
        self.imageName = imageName

    def draw(self, cameraX, cameraY):
        try:
            CDrawingObject.draw(self, cameraX, cameraY, ".//res//image//ground//" + MAPTYPESET[self.mapType] + "//" + self.imageName + ".gif")
        except KeyError:
            CDrawingObject.draw(self, cameraX, cameraY, ".//res//image//ground//" + self.imageName + ".gif")
