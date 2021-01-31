from voting.data import candidate
from voting.data import contest
from voting.data import ranking_method

def generate_votes(vote_table):
  votes = []
  for vote_count, vote in vote_table:
    for x in range(vote_count):
      votes.append(vote)
  return votes


ICECREAM_VOTES = [
  (125, (0, 1, 2, 3)),
  (125, (0, 2, 3, 1)),
  (255, (1, 0, 2, 3)),
  (250, (3, 1, 2, 0)),
  (120, (3, 0, 2, 1)),
  (130, (2,)),
]


def icecream_contest():
  method = ranking_method.RankedChoice(max_choices=6)
  ordered_candidates = []
  for candidate_name, info in (("chocolate", "Democratic Party"),
                               ("strawberry", "Republican Party"),
                               ("Vanilla", "Green Party"),
                               ("Rocky Road", "Independent"),
                               ("Bubblegum", "Chew")):
    ordered_candidates.append(candidate.Candidate(candidate_name, info))
  return contest.Contest("Best Ice Cream", method, ordered_candidates)

def icecream_votes():
  return generate_votes(ICECREAM_VOTES)

