# PiMotionDetectorNotifier
Some python scripts for email or text notification with a simple PIR sensor attached to Raspberry Pi on motion detection.  

Quick instructions on how to connect PIR sensors to a Raspberry Pi: https://projects.raspberrypi.org/en/projects/physical-computing/11.

This script currently assumes the OUT pin is connected to GPIO 23 (see https://www.raspberrypi.org/documentation/usage/gpio/).

<br />

## Instructions

### Prerequisites
Depends on [gpiozero](https://pypi.org/project/jproperties/) and [jproperties](https://pypi.org/project/jproperties/).  Both can be installed via `pip install gpiozero` and `pip install jproperties`

### Installation
Clone repository: `git clone https://github.com/spoorn/PiMotionDetectorNotifier.git`\
Or\
Download and extract zip under Releases: https://github.com/spoorn/PiMotionDetectorNotifier/releases

### Configuration
This script uses an email to send messages/text other emails/phone numbers.  You will need to provide an email for the FROM user (Gmail has been tested and works).  Recommend to use a non-important email as credentials will be stored in a configuration file.  The FROM email is logged in via SMTP, so depending on the email server, you may need to allow access from "Less Secure Apps" (see https://support.google.com/accounts/answer/6010255 if you are using Gmail).

There is a configuration file in the project root `configs.properties`.  Here you can set the FROM email credentials, TO recipients, the message for notification, and others.

### Running the script
`python src/motion.py`

> ⚠️ Ctrl+C to terminate python scripts seems to have issues on some Raspberry Pis for python 2.x.  You can workaround this by using python3 (and installing the prerequisites via pip3).  If you ran the script with python 2.x, you can terminate the motion.py script with Ctrl+Z -> `ps aux | grep motion.py` -> `sudo kill -9 <PID>`


### Output
Logs related to the script's execution will be printed to stdout console, and `logs/output.log`

This script does not print many logs, but if motion detection is frequent, the log file can grow large over a long period of time.  TODO to compress log files or delete based on size.
