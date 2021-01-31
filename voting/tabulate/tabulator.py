from voting.tabulate import record
from voting.tabulate import votes
from voting.data import ranking_method

class ContestRunner(object):
  def __init__(self, contest):
    self._contest = contest

  def Run(self, individual_votes):
    vote_state = votes.VoteState(self._contest, individual_votes)
    all_records = []
    round_num = 1
    while True:
      round_record = self.RunRound(round_num, vote_state)
      all_records.append(round_record)
      if round_record.is_final_round():
        break
      round_num += 1
    return round_record, all_records


class FirstPastThePostContestRunner(ContestRunner):
  def RunRound(self, round_num, vote_state):
    vote_snapshot = vote_state.snapshot()
    top_votes, top_candidates = vote_snapshot.top_vote_and_candidates()
    if len(top_candidates) > 1:
      return record.TieResult(round_num, vote_snapshot, top_candidates, top_votes)
    else:
      return record.FoundWinner(round_num, vote_snapshot, top_candidates[0], top_votes)

class RankedChoiceVotingContestRunner(ContestRunner):
  def RunRound(self, round_num, vote_state):
    vote_snapshot = vote_state.snapshot()
    total_votes = vote_snapshot.total_votes()
    # Total number is the floor of number / 2 + 1, e.g. 1000 / 2 = 500, so you need 501.
    # 1001 / 2 = 500.5, so you still need 501.
    # 1002 / 2 = 501, so you need 502.
    winning_vote_total = int(total_votes / 2) + 1

    top_votes, top_candidates = vote_snapshot.top_vote_and_candidates()
    if top_votes >= winning_vote_total:
      # Standard case: someone has more than 50% of the vote - they win!
      return record.FoundWinner(round_num, vote_snapshot, top_candidates[0], top_votes)
    elif len(top_candidates) == vote_snapshot.num_candidates():
      # Corner case: if all remaining candidates have the same number of votes,
      # then it's a tie.
      return record.TieResult(round_num, vote_snapshot, top_candidates, top_votes)
    else:
      lowest_vote, bottom_candidates = vote_snapshot.lowest_vote_and_candidates()
      if len(bottom_candidates) == vote_snapshot.num_candidates() - 1:
        # Corner case: If all candidates except one would be eliminated, we don't
        # give all of those votes to the last candidate, we just call them the
        # winner without redistributing the remaining votes.
        return record.FoundWinner(round_num, vote_snapshot, top_candidates[0], top_votes)
      # Standard case: no one has 50% of the votes and there's some candidates to
      # safely eliminate.
      round_record = record.NoWinner(round_num, vote_snapshot, bottom_candidates, lowest_vote)
      vote_state.eliminate_candidates(bottom_candidates, round_record)
      round_record.update_votes(vote_state.snapshot())
      return round_record

_runners = { ranking_method.FirstPastThePost : FirstPastThePostContestRunner,
             ranking_method.RankedChoice :  RankedChoiceVotingContestRunner}

def GetContestRunner(contest):
  return _runners[contest.ranking_method().__class__](contest)
