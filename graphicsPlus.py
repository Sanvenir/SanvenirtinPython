#Touhoulalala
#graphicPlus
try:
   from tkinter import *
except:
   from Tkinter import *
import graphics
from graphics import Point
from graphics import GraphWin
from graphics import Line
from graphics import Text
from graphics import color_rgb

class Image(graphics.Image):
   def __init__(self, p, *pixmap):
      graphics.Image.__init__(self, p, *pixmap)
      self.drawed = False

   def draw(self, graphwin):
      if self.drawed: return
      self.drawed = True
      graphics.Image.draw(self, graphwin)

   def undraw(self):
      if not self.drawed: return
      self.drawed = False
      graphics.Image.undraw(self)

class Rectangle(graphics.Rectangle):
   def __init__(self, p1, p2):
      graphics.Rectangle.__init__(self, p1, p2)
      self.drawed = False

   def draw(self, graphwin):
      if self.drawed: return
      self.drawed = True
      graphics.Rectangle.draw(self, graphwin)

   def undraw(self):
      if not self.drawed: return
      self.drawed = False
      graphics.Rectangle.undraw(self)


class Circle(graphics.Circle):
   def __init__(self, p1, p2):
      graphics.Circle.__init__(self, p1, p2)
      self.drawed = False

   def draw(self, graphwin):
      if self.drawed: return
      self.drawed = True
      graphics.Circle.draw(self, graphwin)

   def undraw(self):
      if not self.drawed: return
      self.drawed = False
      graphics.Circle.undraw(self)

