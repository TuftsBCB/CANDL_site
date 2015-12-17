import sys
import os
import re
import datetime


if (len(sys.argv) < 6) :
     #  Must supply 6 arguments: GRAPH1 GRAPH2 LMs EMAIL DIRECTORY
    sys.exit(1)

def notValidEmail(email):
    if len(email) > 6:
        if re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) != None:
            return False
    return True

def main():

  # SCRIPT_TO_RUN = "CANDL/crossDSD_III.py"
  SCRIPT_TO_RUN = "CANDL/dummy_script.py"

  d = sys.argv[5]


  G1 = d +  sys.argv[1]
  G2 = d +  sys.argv[2]
  LMs = d +  sys.argv[3]
  email = sys.argv[4]
  opfile = d + 'output'

  # if notValidEmail(email):
  #   # If not well-formed email
  #   sys.exit(1)


  to_run = "python2.7 " + SCRIPT_TO_RUN + " " + G1 + " " + G2 + \
                          " -t cDSD_full_graph_v_full_graph -o " + \
                            opfile + " -reciprocals " + LMs + " &"

  os.system(to_run)

  # All set!
  exit(0)



if __name__ == '__main__':
    main()



