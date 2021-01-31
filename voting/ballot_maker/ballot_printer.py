
class BallotPrinterOptions(object):
  # If true, will try to keep contests to < 1/2 the size of the paper.
  num_columns = 2

class BallotPrinter(object):
  def __init__(self, ballot, paper, options):
    self._ballot = ballot
    self._paper = paper
    self._options = options

  def 
