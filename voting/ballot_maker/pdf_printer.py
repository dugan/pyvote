import math
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.units import inch
from reportlab.lib import pagesizes

from measurements import  Measurement, pts
import layout_concepts
from layout_concepts import Box, Sides
from colors import Color

class PrintOptions(object):
  page_size = pagesizes.LETTER
  font_size = 12
  font = "Helvetica"

class PdfPrinter:
  def __init__(self, filename):
    self._alignment_points = []
    # Note: bottom up will be dropped in the future!
    self.c = canvas.Canvas(filename,  pagesize=pagesizes.letter, bottomup=False)
    self.c.setStrokeColorRGB(0,0,0)
    self.c.setFillColorRGB(0,0,0)
    self.c.setFont("Helvetica", 12)
    self.SetFontSize(12)
    self._text_padding = 5*pts
    self._width, self._height  = pagesizes.letter
    print(pagesizes.letter)

  def height(self) -> Measurement:
    return self._height * pts

  def width(self) -> Measurement:
    return self._width * pts

  def DrawBox(self, color : Color, box : Box):
    self.c.setStrokeColorRGB(*color.tuple())
    self.c.setFillColorRGB(*color.tuple())
    x, y, width, height = box.tuple()
    self.c.rect(x, y, width, height, fill=1)
 
  def StringWidth(self, font_size, text : str) -> Measurement:
    self.SaveState()
    self.SetFontSize(font_size)
    width = self.c.stringWidth(text) * pts
    self.RestoreState()

  def MaxStringWidth(self, font_size, text_array) -> Measurement:
    self.SaveState()
    self.SetFontSize(font_size)
    max_width = 0
    for text in text_array:
      max_width = max(max_width, self.c.stringWidth(text))
    self.RestoreState()
    return max_width * pts

  def MakeBlack(self):
    self.c.setStrokeColorRGB(0,0,0)
    self.c.setFillColorRGB(0,0,0)

  def WriteName(self, name_box : Box, font_size : int, name : str, horiz_padding : int):
    # TODO: we only need x,y, height here - text is left-justified.  Could provide centering option...
    x, y, width, height = name_box.tuple()
    self.MakeBlack()
    self.SetFontSize(font_size)
    self.c.drawString(x + horiz_padding, y+(height / 2)+font_size/2, name)

  def SetFontSize(self, font_size):
    self._font_size = font_size
    self.c.setFontSize(font_size)

  def DrawHorizontalLine(self, x : Measurement, y : Measurement, width : Measurement):
    self.c.setStrokeColorRGB(0,0,0)
    self.c.line(x, y, x + width, y)

  def DrawBoxSides(self, box : Box, box_sides):
    self.c.setStrokeColorRGB(0,0,0)
    top_left = layout_concepts.Point(box.x, box.y)
    top_right = layout_concepts.Point(box.right_x(), box.y)
    bottom_left = layout_concepts.Point(box.x, box.bottom_y())
    bottom_right = layout_concepts.Point(box.x+box.width, box.y+box.height)
    if (Sides.LEFT in box_sides):
      self.c.line(box.x, box.y, box.x, box.bottom_y())
    if (Sides.RIGHT in box_sides):
      self.c.line(box.right_x(), box.y, box.right_x(), box.bottom_y())
    if (Sides.TOP in box_sides):
      self.c.line(box.x, box.y, box.right_x(), box.y)
    if (Sides.BOTTOM in box_sides):
      self.c.line(box.x, box.bottom_y(), box.right_x(), box.bottom_y())

  def DrawVerticalLine(self, x : Measurement, y : Measurement, height : Measurement):
    self.c.setStrokeColorRGB(0,0,0)
    self.c.line(x, y, x, y + height)

  def DrawOval(self, x : Measurement, y : Measurement, width : Measurement, height : Measurement):
    self.c.setStrokeColorRGB(0,0,0)
    self.c.setFillColorRGB(1,1,1)
    self.c.ellipse(x, y, x + width, y + height)

  def FillOval(self, x : Measurement, y : Measurement, width : Measurement, height : Measurement):
    self.c.setStrokeColorRGB(0,0,0)
    self.c.setFillColorRGB(0,0,0)
    self.c.ellipse(x, y, x + width, y + height, fill=1)

  def SaveState(self):
    self.c.saveState()

  def RestoreState(self):
    self.c.restoreState()

  def StartPrintingAt(self, x : Measurement, y : Measurement):
    self.c.saveState()
    self.c.translate(x,y)
    self.origin = (x,y)
  
  def StopPrinting(self):
    self.origin = (0,0)
    self.c.restoreState()

  def Save(self):
    self.c.showPage()
    self.c.save()
