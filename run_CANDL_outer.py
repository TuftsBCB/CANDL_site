import sys
import os
import re
import datetime


if (len(sys.argv) < 6) :
     #  Must supply 6 arguments: GRAPH1 GRAPH2 LMs EMAIL DIRECTORY
    sys.exit(1)


def main():

  d = sys.argv[5]

  G1 = d + sys.argv[1]
  G2 = d + sys.argv[2]
  LMs = d + sys.argv[3]
  email = sys.argv[4]
  opfile = d + 'output'

  logfile = d + "_logfile"


  # --------------------------------------------------------------
  # CAN DO MORE FILE CHECKING HERE:
  # if filesNotWellFormatted:
  #   sys.exit(1)     ## This will cause a visable error in client
  # --------------------------------------------------------------


  # Now run the script in the background, then exit 0 so client knows request got through.
  to_run = "python run_CANDL_inner.py " + G1 + " " + G2 + " " + LMs + " " + email + " " + opfile + " > " + logfile + " &"
  os.system(to_run)

  sys.exit(0) # tell the web app that all went well, the program is running.

if __name__ == '__main__':
    main()



