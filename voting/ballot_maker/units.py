
class Unit(object):
  pass

class Points(Unit):
  def __init__(self, number):
    self._number = number

  def ToPoints(self):
    return self._number

class Inches(Unit):
  def __init__(self, number):
    self._number = number

  def ToPoints(self):
    return float(self._number) / 72
