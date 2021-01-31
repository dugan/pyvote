
class AbstractRankingMethod(object):
  def __init__(self):
    pass

  def num_choices(self):
    return 1

  def choices_exclusive(self):
    return True

  def minimum_votes_to_win(self, total_votes):
    # No minimum to win.
    return None

class FirstPastThePost(AbstractRankingMethod):
  """ Rank candidates using the First Past The Post method.

  This is the most familiar version of voting where each person picks one candidate.
  """
  def num_choices(self):
    return 1

  def choices_exclusive(self):
    return True

class RankedChoice(AbstractRankingMethod):
  """ Rank candidates using the Ranked Choice Method.
    
      If max_choices is set to something other than None, voters can pick at
      most max_choice candidates.  max_choice defaults to 6.  Unlimited
      max_choice may make ballot printing harder.

      TODO(dbc): get into the details of various RCV algorithms.
  """

  def __init__(self, max_choices=6):
    self._max_choices = max_choices

  def num_choices(self, contest):
    if self._max_choices is None:
      return contest.num_candidates()
    return min(self._max_choices, contest.num_candidates())

  def choices_exclusive(self):
    return True

  def minimum_votes_to_win(self, total_votes):
    return total_votes / 2 + 1
