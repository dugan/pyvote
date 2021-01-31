from typing import Union

"""
Describes a distance in a single dimension.
"""
class Measurement(int):
  def __mul__(self, other : int) -> int:
    return self.__class__(int(self) * int(other))


  def __add__(self, other : int) -> int:
    return self.__class__(int(other) + int(self))

  def __repr__(self) -> str:
    return "%s(%d)" % (self.__class__.__name__, int(self))

  __rmul__ = __mul__
  __radd__ = __add__
 

"""
Point scale
"""
class Pts(Measurement):
  pass

# use to mark an integer as being in points (pts) - 10 * pts, e.g.
pts = Pts(1)
