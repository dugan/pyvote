
class Candidate(object):
  def __init__(self, name, description=""):
    self._name = name
    self._description = description

  def __str__(self):
    return self._name

  def name(self):
    return self._name 

  def description(self):
    return self._description 
