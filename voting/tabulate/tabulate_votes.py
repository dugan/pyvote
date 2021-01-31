#!/usr/bin/python
import sys
sys.path.append("/Users/dbc/pyvote")

# import the necessary packages
import argparse
import json

from voting.tests import example_contest
from voting.tabulate import tabulator


def run():
  # construct the argument parse and parse the arguments
  #ap = argparse.ArgumentParser()
  #ap.add_argument("-v", "--votes", required=True,
  #  help="path to the input votes")
  #args = vars(ap.parse_args())

  #votes = json.loads(open(args["votes"], "r").read())

  contest = example_contest.icecream_contest()
  votes = example_contest.icecream_votes()
  runner = tabulator.GetContestRunner(contest)
  final_result, records = runner.Run(votes)
  print "\n".join(str(x) for x in records)

if __name__ == "__main__":
  run()
