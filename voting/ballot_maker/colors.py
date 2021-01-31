
class Color(object): 
  def __init__(self, r : float, g : float, b : float):
    self.r = r
    self.g = g
    self.b = b

  def tuple(self):
    return (self.r, self.g, self.b)


class Gray(Color):
 # intensity bet
 def __init__(self, intensity : float):
   self.r = self.g = self.b = intensity
   self.intensity = intensity

 def __repr__(self):
   return "colors.Gray(%s)" % (self.intensity,)

Black = Gray(0)
White = Gray(1)
