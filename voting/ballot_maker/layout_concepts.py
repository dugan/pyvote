from measurements import Measurement, pts
import enum

class Point(object):
  def __init__(self, x: Measurement, y : Measurement):
    self.x = x
    self.y = y

class Sides(enum.Enum):
  LEFT = enum.auto()
  RIGHT = enum.auto()
  TOP = enum.auto()
  BOTTOM = enum.auto()

class HorizontalAlignment(enum.Enum):
  CENTER = enum.auto()
  LEFT = enum.auto()
  RIGHT = enum.auto()

class VerticalAlignment(enum.Enum):
  CENTER = enum.auto()
  TOP = enum.auto()
  BOTTOM = enum.auto()

class Box(object):

  def __init__(self, width : Measurement,  height : Measurement):
    Box.__init__(self, 0*width, 0*height, width, height)
    
  def __init__(self, x : Measurement, y : Measurement, width : Measurement, height : Measurement):
    self.upper_left = Point(x, y)
    self.width = width
    self.height = height
    self.x = x 
    self.y = y

  def tuple(self):
    return (self.x, self.y, self.width, self.height)

  def set_width(self, width):
    self.width = width

  def bottom_y(self):
    return self.y + self.height

  def right_x(self):
    return self.x + self.width
 
  def Intersection(self, other):
    # could using points help here?
    # some sort of max across points
    x = max(self.x, other.x)
    y = max(self.y, other.y)
    right_x = min(self.right_x(), other.right_x())
    bottom_y = min(self.bottom_y(), other.bottom_y())
    width = max(0, right_x - x)
    height = max(0, bottom_y - y)
    return Box(x, y, width, height)

  def BoxInside(self, side, extension):
    x,y,width,height = self.tuple()
    if (side == Sides.TOP):
      height = extension
    if (side == Sides.BOTTOM):
      y = self.bottom_y() - extension
      height = extension
    if (side == Sides.LEFT):
      width = extension
    if (side == Sides.RIGHT):
      x = self.right_x() - extension
      width = extension
    return Box(x, y, width, height)

  def BoxOnOuterSide(self, side, extension):
    x,y,width,height = self.tuple()
    if (side == Sides.TOP):
      y = y - extension
      height = extension
    if (side == Sides.BOTTOM):
      y = self.bottom_y()
      height = extension
    if (side == Sides.LEFT):
      x = x - extension
      width = extension
    if (side == Sides.RIGHT):
      x = self.right_x() 
      width = extension
    return Box(x, y, width, height)
  
  def BoxBelow(self, height : Measurement):
    return self.BoxOnOuterSide(Sides.BOTTOM, height)

  def BoxToRight(self, width : Measurement):
    return self.BoxOnOuterSide(Sides.RIGHT, width)
    

  def HorizontalSlice(self, relative_y : Measurement, height : Measurement):
    return self.Intersection(HorizontalSlice(self.y + relative_y, height))

_INFINITY = 999999*pts
ORIGIN = 0*pts

# Slices, useful for creating intersections
def HorizontalSlice(y : Measurement, height : Measurement):
  return Box(0, y, _INFINITY, height)

def VerticalSlice(x : Measurement, width : Measurement):
  Box(x, 0, width, _INFINITY)
