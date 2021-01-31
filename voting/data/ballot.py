  
class Ballot(object):
  """ A ballot is a set of separate contests that are voted on together."""

  def __init__(self, contests, header=""):
    self._header = header
    self._contests = contests

  def header(self):
    self._header = header

  def contests(self):
    return self._contests
