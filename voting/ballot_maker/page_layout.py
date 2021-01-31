
class PageLayout(layouts.Layout):
  def __init__(self, pdf_printer, page_num, container):
    self._pdf_printer = pdf_printer
    self._container = container
    self._alignment = AlignmentLayout(pdf_printer, paper)

  def outer_box_size(self):
    return self._container.inner_box_size(),

  def inner_box_size(self):
    return (self._paper.height() - 2*self._alignment.top_and_bottom_height(), 
            self._paper.width() - 2*self._alignment.side_pixels())
