

class RoundRecord(object):
  WINNER = 0
  NO_WINNER = 1
  TIE_RESULT = 2

  def __init__(self, round_num, vote_snapshot, outcome, candidates, vote_count):
    self._round_num = round_num
    self._vote_snapshot = vote_snapshot
    self._contest = vote_snapshot.contest()
    self._outcome = outcome
    self._candidates = candidates
    self._vote_count = vote_count
    self._updated_votes = None

  def vote_snapshot(self):
    return self._vote_snapshot

  def candidate_name(self, index):
    return self._contest.candidate(index)

  def update_votes(self, updated_votes):
    self._updated_votes = updated_votes

  def round(self):
    return self._round

  def candidates(self):
    return self._candidates

  def outcome(self):
    return self._outcome

  def vote_count(self):
    return self._vote_count

  def is_final_round(self):
    return self._outcome != self.NO_WINNER

  def is_tie(self):
    return self._outcome != self.TIE_RESULT

  def _candidates_as_string(self, candidates):
    return "(" + ", ".join([str(self._contest.candidate(x)) for x in candidates]) + ")"

  def candidates_as_string(self):
    return self._candidates_as_string(self._candidates)

  def round_string(self):
    return "\n************ ROUND %d ***************\n\n" % self._round_num

  def __str__(self):
    string = ("%s\n"
           "Votes before round: \n"
           "%s\n"
           "\n"
           "%s\n\n" % (self.round_string(), self.vote_snapshot(), self.results_as_string()))
    if self._updated_votes:
      string += "Votes after round: \n%s\n"  % self._updated_votes
    return string

class NoWinner(RoundRecord):
  def __init__(self, round_num, votes_per_choice, lowest_ranked, vote_count):
    RoundRecord.__init__(self, round_num, votes_per_choice, self.NO_WINNER, lowest_ranked, vote_count)
    self._transferred_votes = []

  def transfer_votes(self, from_candidate, backups, to_candidate, vote_count):
    self._transferred_votes.append((from_candidate, backups, to_candidate, vote_count))

  def transfers_as_string(self):
    lines = []
    for from_candidate, backups, to_candidate, vote_count in self._transferred_votes:
      if to_candidate is not None:
        lines.append("%d votes from %s with backup choices %s were transferred to %s" % (vote_count, self.candidate_name(from_candidate), self._candidates_as_string(backups), self.candidate_name(to_candidate)))
      elif backups:
        lines.append("%d votes were discarded from %s because all their backups %s were eliminated" % (vote_count, self.candidate_name(from_candidate), self._candidates_as_string(backups)))
      else:
        lines.append("%d votes were discarded from %s because they had no backup candidate" % (vote_count, self.candidate_name(from_candidate)))
    return '\n'.join(lines) + '\n'

  def results_as_string(self):
    return "No winner yet.  Candidate(s) %s are eliminated with the lowest vote count of %d.\n%s" % (self.candidates_as_string(), self.vote_count(), self.transfers_as_string())


class FoundWinner(RoundRecord):
  def __init__(self, round_num, vote_snapshot, winner, vote_count):
    RoundRecord.__init__(self, round_num, vote_snapshot, self.WINNER, [winner], vote_count)

  def winner(self):
    return self._candidates[0]

  def results_as_string(self):
    return "Winner determined! %s is winner with %d votes.\n" % (self.candidate_name(self.winner()), self.vote_count())


class TieResult(RoundRecord):
  def __init__(self, round_num, votes_per_choice, tied_candidates, vote_count):
    RoundRecord.__init__(self, round_num, votes_per_choice, self.TIE_RESULT, tied_candidates, vote_count)

  def results_as_string(self):
    return ("It's a tie! %s are tied with %d votes each after all other candidates are"
            " eliminated." % (self.candidates_as_string(), self.vote_count()))
