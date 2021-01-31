from reportlab.platypus import Paragraph
from reportlab.lib import enums

class HeaderLayout(layouts.Layout):
  def __init__(self, container, paper, pdf_printer):
    self._container = container
    self._header_text = header_text
    self._paper = paper
    self._pdf_printer = pdf_printer
    self._paragraph = Paragraph(self._header_text, alignment=enums.TA_CENTER)
    w, h = self._container.inner_box_size()
    self._height, self._width = self._paragraph.wrap(w, h)

  def box(self):
    return self._height, self._width

  def draw(self, canvas, x, y):
    self._paragraph.drawOn(canvas, x, y)
    
  
class BallotLayout(object):
  def __init__(self, ballot, paper, options, pdf_printer):
    self._ballot = ballot
    self._paper = paper
    self._options = options
    self._pdf_printer = pdf_printer
    self._pages = [page_layout.PageLayout(1, paper, pdf_printer)]
    self._current_page = self._pages[0]
    self._header = HeaderLayout(
    self._contest_layouts = [ contest_printer.ContestLayout(c, pdf_printer) for c in self._ballot.contests() ]

  def lay_out_contests(self):
    self._current_page.add_layout(
    start_x,start_y,page_w,page_h = self.usable_page_space()[:2]

    remaining_page_height = h
    remaining_page_width = w
    current_x, current_y = start_x, start_y
    page_num = 1

    for layout in self._contest_layouts:
      page_num, current_x, current_y = self.LayoutContest(page_num, current_x, current_y)
      contest_w, contest_h = layout.contest_box()[2:]
      if contest_h > remaining_page_height or contest_w > remaining_page_width:
        if contest_height > page_height or contest_w > page_w:
          # TODO: better exceptions.
          raise RuntimeError("Contest is too large")
        page_num += 1
        remaining_page_height = page_height
        remaining_page_width = page_width

        self.PlaceContest(page_num, 
        self._contest_locations.append((page, contest_x, contest_y, contest_w, contest_h))

        


        
      else:
        
    

  def header_box(


