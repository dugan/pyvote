
class VoteState(object):
  def __init__(self, contest, unsorted_votes):
    self._contest = contest

    grouped_votes = {}
    for vote in unsorted_votes:
      vote = tuple(vote)
      if vote not in grouped_votes:
        grouped_votes[vote] = 1
      else:
        grouped_votes[vote] += 1

    self._totals_per_candidate = {}
    self._total_active_votes = 0
    self._backup_candidates = {}
    for vote, count in grouped_votes.iteritems():
      first_candidate = vote[0]
      backup_candidates = vote[1:]
      if first_candidate not in self._backup_candidates:
        self._backup_candidates[first_candidate] = {}
      self._backup_candidates[first_candidate][backup_candidates] = count
      if first_candidate not in self._totals_per_candidate:
        self._totals_per_candidate[first_candidate] = count
      else:
        self._totals_per_candidate[first_candidate] += count
      self._total_active_votes += count

  def total_active_votes(self):
    return self._total_active_votes

  def snapshot(self):
    return VoteTotalsSnapshot(self._contest, self._totals_per_candidate)

  def is_candidate_active(self, candidate):
    return candidate in self._totals_per_candidate

  def eliminate_candidates(self, candidates, record):
    votes_to_reassign = []
    for candidate in candidates:
      votes_to_reassign.append((candidate, self._backup_candidates[candidate]))
      del self._backup_candidates[candidate]
      del self._totals_per_candidate[candidate]
      
    for first_candidate, backup_candidates_dict in votes_to_reassign:
      for backup_candidates, vote_count in backup_candidates_dict.iteritems():
        original_backup_candidates = backup_candidates
        new_candidate = None
        if backup_candidates:
          new_candidate = backup_candidates[0]
          backup_candidates = backup_candidates[1:]
          while not self.is_candidate_active(new_candidate):
            # Their backup candidate was also eliminated.  if they have more backup
            # candidates, give their votes to them.
            if backup_candidates:
              new_candidate = backup_candidates[0]
              backup_candidates = backup_candidates[1:]
            else:
              new_candidate = None
              break
        record.transfer_votes(first_candidate, original_backup_candidates, new_candidate, vote_count)

        if new_candidate is None:
          # they're all out of backup candidates, so their vote is discarded.
          self._total_active_votes -= vote_count
          continue
          
        if backup_candidates not in self._backup_candidates[new_candidate]:
          self._backup_candidates[new_candidate][backup_candidates] = vote_count
        else:
          self._backup_candidates[new_candidate][backup_candidates] += vote_count
        self._totals_per_candidate[new_candidate] += vote_count

class VoteTotalsSnapshot(object):
  def __init__(self, contest, candidate_vote_dict):
    self._contest = contest
    self._votes_per_candidate = sorted([(x[1], x[0]) for x in candidate_vote_dict.iteritems()], reverse=True)
    self._total_votes = sum(candidate_vote_dict.values())

  def num_candidates(self):
    return len(self._votes_per_candidate)

  def contest(self):
    return self._contest

  def total_votes(self):
    return self._total_votes

  def top_vote_and_candidates(self):
    top_vote =  self._votes_per_candidate[0][0]
    return top_vote, [ x[1] for x in self._votes_per_candidate if x[0] == top_vote ]

  def lowest_vote_and_candidates(self):
    lowest_votes =  self._votes_per_candidate[-1][0]
    return lowest_votes, [ x[1] for x in self._votes_per_candidate if x[0] == lowest_votes ]

  def __str__(self):
    total = self.total_votes()
    string = ("\n".join(["%s: %d" % (self._contest.candidate(x[1]), x[0]) for x in self._votes_per_candidate]) + "\n"
              + "%d total" % (total,))
    if self._contest.ranking_method().minimum_to_win(total):
      string += " (%s to win)" % self._contest.ranking_method().minimum_to_win(total)
    return string
