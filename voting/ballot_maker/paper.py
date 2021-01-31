
class Paper(object):
  def __init__(self, paper_size):
    self._width, self._height = paper_size
    self._top_and_bottom_margins = Inches(.5).ToPoints()
    self._side_margins = Inches(.5).ToPoints()

  def inner_box_size(self):
    return (self._height - 2*self._top_and_bottom_margins,
            self._width - 2*self._side_margins)

  def inner_box_origin(self):
    return (self._top_and_bottom_margins, self._side_margins)

  def outer_box_size(self):
    return self._height, self._width
