  
class Contest(object):
  """ A contest selects between multiple candidates using a particular ranking method.
      
      The candidates passed in will be shown in the order that they are listed here.
  """
  def __init__(self, contest_name, ranking_method, ordered_candidates):
    self._contest_name = contest_name
    self._ranking_method = ranking_method
    self._ordered_candidates = ordered_candidates

  def name(self):
    return self._contest_name

  def ranking_method(self):
    return self._ranking_method

  def num_candidates(self):
    return len(self._ordered_candidates)

  def num_choices(self):
    return self._ranking_method.num_choices(self)

  def candidates(self):
    return self._ordered_candidates

  def candidate(self, index):
    return self._ordered_candidates[index]
