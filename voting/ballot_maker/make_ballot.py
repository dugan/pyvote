#!/usr/bin/python
import sys
sys.path.append("/home/David/pyvote")
from voting.tests import example_contest
from voting.data import ballot 
from voting.ballot_maker import contest_printer
from voting.ballot_maker import pdf_printer



if __name__ == '__main__':
  contest = example_contest.icecream_contest()
  contest2 = example_contest.icecream_contest()
  full_ballot = ballot.Ballot([contest, contest2])
  pdf_printer = pdf_printer.PdfPrinter("../output/ex.pdf")
  contest_printer = contest_printer.ContestPrinter(contest, pdf_printer)
  pdf_printer.StartPrintingAt(50,200)
  contest_printer.PrintContest()
  pdf_printer.StopPrinting()
  #pdf_printer.DrawAlignmentSquares(6, 20, 50)
  #pdf_printer.DrawAlignmentLines()
  pdf_printer.Save()
