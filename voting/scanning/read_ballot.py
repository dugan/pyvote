#!/usr/bin/python
import sys
sys.path.append("/Users/dbc/pyvote")

# import the necessary packages
import argparse
import cv2
import json

from voting.scanning import scanner

def run():
  # construct the argument parse and parse the arguments
  ap = argparse.ArgumentParser()
  ap.add_argument("-i", "--image", required=True,
    help="path to the input image")
  ap.add_argument("-o", "--output", required=True,
    help="output to write results to")
  args = vars(ap.parse_args())

  image = cv2.imread(args["image"])
  ballot_scanner = scanner.BallotScanner()
  all_votes = []
  vote = ballot_scanner.ScanBallot(image)
  all_votes.append(vote)
  open(args["output"], "w").write(json.dumps(all_votes))


if __name__ == "__main__":
  run()
