import itertools

import layout_concepts
from layout_concepts import Box, ORIGIN, Sides
import measurements
from measurements import pts, Measurement

"""
ContestLayout
------------------------
| Header
----------------------------
|  Description
|---------------------------
|     C|C|C|C|
|     o|o|o|o|
      l|l|l|l|
|____---------
|Name|x|x|x|x|
|------------------
|Name|x|x|x|x|
|------------------
|Name|x|x|x|x|
----------------


contest_box 
column_header_box =  Col bits
column_box = 
choice_grid_box contains only choices.
election_box contains names + choice_grid_box
row_box = name + choices

"""

class ContestLayoutOptions(object):
  def __init__(self):
    self.header_box_height = 30*pts
    self.max_name_height = 30*pts
    self.choice_box_width = 30*pts
    self.oval_height = 12*pts
    self.oval_width = 20*pts
    self.name_box_buffer = 20*pts
    self.name_font_size = 9*pts
    self.default_font_size = 12*pts
    self.default_font = "Helvetica"
    self.choice_description_box_height = 70*pts
    self.text_padding = 5*pts

class ContestLayout(object):
  def __init__(self, contest, pdf_printer):
    self._contest = contest
    self.options = ContestLayoutOptions()
    self._pdf_printer = pdf_printer
    self._generate_boxes()

  def _determine_name_box_width(self) -> Measurement:
     name_strings = (x.name() for x in self._contest.candidates())
     desc_strings = (x.description() for x in self._contest.candidates())
     width = self._pdf_printer.MaxStringWidth(self.options.name_font_size, itertools.chain(name_strings, desc_strings))
     return width + self.options.name_box_buffer

  def _determine_choice_grid_width(self) -> Measurement:
    return self._contest.num_choices() * self.options.choice_box_width

  def _generate_boxes(self):
    # Set height for boxes first.
    self._header_box = layout_concepts.HorizontalSlice(ORIGIN, self.options.header_box_height)
    self._choice_description_box = self._header_box.BoxBelow(self.options.choice_description_box_height)
    self._election_box = self._choice_description_box.BoxBelow(
        len(self._contest.candidates()) * self.options.max_name_height)

    # Now create width for the key part - the choices
    self._name_box = self._election_box.BoxInside(Sides.LEFT, self._determine_name_box_width())
    self._choice_grid_box = self._name_box.BoxToRight(self._determine_choice_grid_width())
    
    # Now fill in missing xs and widths from above.
    self._contest_box = Box(0, 0, self._choice_grid_box.right_x(), self.choice_grid_box().bottom_y())
    self._header_box.set_width(self._contest_box.width)
    self._choice_description_box.set_width(self._contest_box.width)
  
  def contest_box(self) -> Box:
    """  The entire space taken up by this contest. 
    Width determined by candidates + choice grid.
    Height determined by header, choice description, + candidates grid
    """
    return self._contest_box

  def header_box(self) -> Box:
    return self._header_box

  def choice_description_box(self) -> Box:
    return self._choice_description_box

  def name_box(self) -> Box:
    return self._name_box

  def election_box(self) -> Box:
    return self._election_box

  def choice_grid_box(self) -> Box:
    return self._choice_grid_box

  def column_box(self, column_num : int) -> Box:
    width = self.options.choice_box_width
    x = self.name_box().width + width * column_num
    y = self.choice_description_box().y
    height = self.choice_description_box().height + self._contest.num_candidates() * self.options.max_name_height
    return Box(x, y, width, height)

  def choice_box(self, row_num : int, column_num : int) -> Box:
    column_box = self.column_box(column_num)
    row_box = self.row_box(row_num)
    return column_box.Intersection(row_box)

  def row_box(self, row_num : int) -> Box:
    x = 0 * pts
    y = self.election_box().y + row_num * self.options.max_name_height
    width = self.name_box().width + self.options.choice_box_width * self._contest.num_choices()
    height = self.options.max_name_height
    return Box(x, y, width, height)

  def name_box_for_row(self, row_num : int) -> Box:
    height = self.options.max_name_height
    return self.name_box().HorizontalSlice(row_num * height, height)

