import colors
from colors import Color
import contest_layout
from measurements import pts
from layout_concepts import Box, Sides
import text_util

class ContestPrintOptions(object):
  def __init__(self):
    self.gray_color = colors.Gray(.8)
    self.alternating_fill_colors = [self.gray_color, colors.White]
    self.line_color = colors.Black
 
  def get_color_for_option(self, option : int) -> Color:
    index = option % len(self.alternating_fill_colors)
    return self.alternating_fill_colors[index]


class ContestPrinter(object):
  def __init__(self, contest, pdf_printer):
    self._pdf_printer = pdf_printer
    self._contest = contest
    self._layout = contest_layout.ContestLayout(contest, pdf_printer)
    self.options = ContestPrintOptions()

  def DrawRankedChoiceColumnHeader(self, x, y, width, choice_num):
    bottom_buffer = 10
    top_buffer = 10
    font_height = 6
    choice_str = text_util.get_choice_string(choice_num)
    choice_as_word = text_util.get_choice_num_as_word(choice_num)
    self._pdf_printer.MakeBlack()
    self._pdf_printer.c.drawCentredString(x+width/2, y - 10, choice_str)
    self._pdf_printer.c.saveState()
    self._pdf_printer.c.translate(x + width / 2, y - 30)
    self._pdf_printer.c.rotate(270)
    text = self._pdf_printer.c.beginText(0, 0) 
    text.setFont("Helvetica", 9)
    text.textLine(choice_as_word.capitalize())
    text.textLine("Choice")
    self._pdf_printer.c.drawText(text)
    self._pdf_printer.c.restoreState()

  def WriteCandidate(self, name_box : Box, candidate):
    x, y, width, height = name_box.tuple()
    self._pdf_printer.MakeBlack()
    text = self._pdf_printer.c.beginText(x + self._pdf_printer._text_padding, y + height / 2 - 2) 
    text.setFont("Helvetica-Bold", 9)
    text.textLine(candidate.name().capitalize())
    text.setFont("Helvetica", 9)
    text.textLine(candidate.description().capitalize())
    self._pdf_printer.c.drawText(text)

  #def AddSelectionOption(self):
  #  self.alignment_points(x+width/2, y+height/2)

  def PrintContest(self):
    self._PrintDescription()
    self._PrintElectionBox()
    self._pdf_printer.DrawBoxSides(self._layout.contest_box(), [Sides.LEFT, Sides.RIGHT])

  def RankWinners(self, ranks):
    for order, candidate_id in enumerate(ranks):
      candidate = self._contest.candidates()[candidate_id]
      x, y, width, height = self._layout.choice_box(candidate_id, order).tuple()
      x += (width - self._layout.options.oval_width) / 2
      y += (height - self._layout.options.oval_height) / 2
      self._pdf_printer.FillOval(x, y, self._layout.options.oval_width, self._layout.options.oval_height)

  def _PrintChoice(self, candidate_num, choice_num):
    x, y, width, height = self._layout.choice_box(candidate_num, choice_num).tuple()
    # TODO: should this box be in layout?
    x += (width - self._layout.options.oval_width) / 2
    y += (height - self._layout.options.oval_height) / 2
    self._pdf_printer.DrawOval(x, y, self._layout.options.oval_width, self._layout.options.oval_height)

  def _PrintElectionBox(self):
    self._PrintElectionBoxLayout()
    for candidate_num, candidate in enumerate(self._contest.candidates()):
      self.WriteCandidate(self._layout.name_box_for_row(candidate_num), candidate)
      for choice_num in range(self._contest.num_choices()):
        self._PrintChoice(candidate_num, choice_num)

  def _PrintElectionBoxLayout(self):
    pdf_printer = self._pdf_printer
    contest = self._contest

    num_choices = contest.num_choices()
    for choice_num in range(num_choices):
      (x, y, width, height) = self._layout.column_box(choice_num).tuple()
      y = self._layout.election_box().y
      self.DrawRankedChoiceColumnHeader(x, y, width, choice_num+1)

    for candidate_num, candidate in enumerate(contest.candidates()):
      color = self.options.get_color_for_option(choice_num)
      pdf_printer.DrawBox(color, self._layout.row_box(candidate_num))

    for choice_num in range(num_choices):
      column_box = self._layout.column_box(choice_num)
      pdf_printer.DrawBoxSides(column_box, [Sides.LEFT, Sides.RIGHT])

    for candidate_num, candidate in enumerate(contest.candidates()):
      row_box = self._layout.row_box(candidate_num)
      pdf_printer.DrawBoxSides(row_box, [Sides.TOP, Sides.BOTTOM])

  def _PrintDescription(self):
    description_box = self._layout.header_box()
    self._pdf_printer.DrawBox(self.options.gray_color, description_box)
    self._pdf_printer.WriteName(description_box, self._layout.options.default_font_size, 
                                self._contest.name(),
                                self._layout.options.text_padding)
    self._pdf_printer.DrawBoxSides(description_box, [Sides.TOP])
