from gpiozero import MotionSensor
from jproperties import Properties
import smtplib
import traceback
import time
import os
import sys
import logging

configs = Properties()
config_filename = "configs.properties"
output_log = "output.log"
user = None
server = None
log = None

""" Setup logging """
def setup_logging():
  global log
  log = logging.getLogger()
  log.setLevel(logging.DEBUG)

  # Output to stdout console
  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
  handler.setFormatter(formatter)
  log.addHandler(handler)

  # Output to log file
  filehandler = logging.FileHandler("../logs/" + output_log)
  filehandler.setLevel(logging.DEBUG)
  filehandler.setFormatter(formatter)
  log.addHandler(filehandler)

""" Connects to email server via SMTP """
def connect_email():
  retries = int(configs.get("login_retries").data)
  for i in range(retries):
    try:
      global server
      log.info("connecting to email server...")
      passw = configs.get("from_password").data
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.ehlo()
      server.starttls()
      server.login(user, passw)
      log.info("logged in...")
      return server
    except Exception as ex:
      traceback.print_exc()
    log.warn("could not connect to email, retrying after 5s...")
    time.sleep(5)
  log.error('Could not connect to FROM email server!  SMTP is labeled as a "Less Secure" app, so check the FROM email settings to make sure those apps are allowed access.')

""" Action when motion is detected """
def act(device):
  log.info("motion detected...")
  global server
  message = configs.get("message").data
  to_list = configs.get("to_emails").data.split(",")
  try:
    [server.sendmail(user, to_entry, message) for to_entry in to_list]
  except smtplib.SMTPSenderRefused:
    log.info("attempting to reconnect smtp...")
    server = connect_email()
    [server.sendmail(user, to_entry, message) for to_entry in to_list]
  log.info("sent notification [" + message + "] to " + str(to_list))

def logdone():
  log.info("done")

if __name__ == "__main__":
  setup_logging()
  # Load settings file
  log.info("loading config file...")
  with open("../" + config_filename, 'rb') as config_file:
    configs.load(config_file)
  user = configs.get("from_username").data
  assert user is not None
  logdone()

  # Connect to Motion Sensor
  log.info("connecting to motion sensor...")
  pir = MotionSensor(23)
  logdone()
  
  pir.wait_for_no_motion()

  # Connect email
  log.info("connecting to FROM email...")
  server = connect_email()
  logdone()

  # Act on motion detection
  interval = int(configs.get("motion_detect_interval").data)
  try:
    pir.when_motion = act
    while(1):
      log.info("idle...")
      pir.wait_for_motion()
      time.sleep(1)
      log.info("waiting for motion to stop...")
      pir.wait_for_no_motion()
      time.sleep(interval)
    log.info("exited out of program")
  except:
    traceback.print_exc()
    log.error("Killed\n\n")
  finally:
    server.close()
