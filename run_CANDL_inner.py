import sys
import os
import re
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():

  SCRIPT_TO_RUN = "CANDL/crossDSD_III.py"
  # SCRIPT_TO_RUN = "CANDL/dummy_script.py"

  G1 = sys.argv[1]
  G2 = sys.argv[2]
  LMs = sys.argv[3]
  email = sys.argv[4]
  opfile = sys.argv[5]


  today = str(datetime.date.today())


  to_run = "python2.7 " + SCRIPT_TO_RUN + " " + G1 + " " + G2 + \
                          " -t cDSD_full_graph_v_full_graph -o " + \
                            opfile + " -reciprocals " + LMs 

  os.system(to_run)
  # We wait for this to finish...



  # UNCOMMENT THE BELOW TO SEND AUTOMATIC EMAILS!
  
  # # # Now time to send the email!
  # msg = MIMEMultipart()
  # msg['Subject'] = 'CANDL node matching results, submission from ' + today

  # sender = # Add sender email
  # recipient = email

  # msg['From'] = sender
  # msg['To'] = recipient
  # msg.preamble = 'Your CANDL results: \n\n'

  # fp = open(opfile, 'rb')
  # txt = MIMEText(fp.read())
  # fp.close()
  # msg.attach(txt)

  # # Send the email via our own SMTP server.
  # s = smtplib.SMTP('localhost')
  # s.sendmail(sender, recipient, msg.as_string())


  # All set!
  exit(0)

if __name__ == '__main__':
    main()



