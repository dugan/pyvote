 
  def DrawColumnWithDiagonalHeader(self, header, color, x, y, width, height):
    bottom_buffer = 10
    top_buffer = 10
    font_height = 6
    c = self.c
    self.DrawBox(color, x, y, width, height)
    c.saveState()
    c.translate(x+width,y)
    c.rotate(45)
    # side of right triangle w/ hypotenuse of width.
    vert = math.sqrt((width*width)/2)
    # side of right triangle w/ hypotense of width/2
    # this is the vertical amount that the string is pushed out.
    # TODO: switch these to use rotation + translate instead
    vert2 = math.sqrt((width*width)/8)
    c.translate(-(c.stringWidth(header)+vert2+bottom_buffer+top_buffer), 0)

    self.DrawBox(color, 0, 0, vert2 + c.stringWidth(header)+bottom_buffer+top_buffer, vert)
    c.restoreState()
    c.saveState()
    c.stringWidth(header)
    c.translate(x+width/2,y-5)
    c.rotate(45)
    # TODO: make based on font height?
    c.translate(-(c.stringWidth(header)) - bottom_buffer, font_height)
    self.MakeBlack()
    c.drawString(0, 0, header)
    c.restoreState()

