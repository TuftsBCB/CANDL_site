import sys
import os
import re
import time
import datetime


if (len(sys.argv) != 9) :
     #  Must supply 6 arguments: GRAPH1 GRAPH2 LMs EMAIL DIRECTORY
    sys.exit(1)


def main():

  output_file = sys.argv[6]

  f = open(output_file, 'w+')

  for i in range(100):
    for a in sys.argv:
      f.write(a)
      f.write('\n')
    f.write('\n\n\n\n')

  f.write(str(datetime.datetime.now().time()))
  f.close()




if __name__ == '__main__':
    main()


