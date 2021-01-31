ALIGNMENT_QR_CODE,
ALIGNMENT_LINES,
ALIGNMENT_SQUARES = range(3)

class AlignmentLayout(object):
  def __init__(self, pdf_printer, paper):
    self._alignment_points = []
  
  def add_alignment_point(self, page_num, x, y):
    self._alignment_points.append(page_num, x, y))


class AlignmentPrinter(object):
  def __init__(self):
    self._alignment_points = []
                        
  def DrawAlignmentLines(self):
    self.c.saveState()
    if self.origin != (0,0):
      self.c.translate(-self.origin[0], -self.origin[1])
    self.MakeBlack()
    thickness = 6
    length = 12
    # printers don't print to the edge of the page, so leave some space.
    padding = 15
    for (x,y) in self._alignment_points:
      self.c.rect(x-thickness/2, padding, thickness, length, fill=1)
      self.c.rect(x-thickness/2, self._height - (length+padding), thickness, length, fill=1)

      self.c.rect(padding, y-thickness/2, length, thickness, fill=1)
      self.c.rect(self._width - (length+padding), y-thickness/2, length, thickness, fill=1)
    self.c.restoreState()

  def DrawAlignmentSquare(self, center_x, center_y, inner_box_length, outer_box_length):
    inner_half = inner_box_length / 2
    outer_half = outer_box_length / 2
    self.c.rect(center_x - inner_half, center_y - inner_half, inner_box_length, inner_box_length, fill=0)
    self.c.rect(center_x - outer_half, center_y - outer_half, outer_box_length, outer_box_length, fill=0)

  def DrawAlignmentSquares(self, thickness, inner_box_length, outer_box_length):
    self.c.saveState()
    self.c.setLineWidth(thickness)
    self.MakeBlack()
    edge_padding = 10
    left_x = top_y  = edge_padding + outer_box_length / 2
    right_x = self.width() - edge_padding - outer_box_length / 2
    bottom_y = self.height() - edge_padding - outer_box_length / 2
    self.DrawAlignmentSquare(left_x, top_y, inner_box_length, outer_box_length)
    self.DrawAlignmentSquare(left_x, bottom_y, inner_box_length, outer_box_length)
    self.DrawAlignmentSquare(right_x, top_y, inner_box_length, outer_box_length)
    self.DrawAlignmentSquare(right_x, bottom_y, inner_box_length, outer_box_length)
    self.c.restoreState()

