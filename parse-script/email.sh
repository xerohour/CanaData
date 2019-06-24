#!/bin/bash

# file: email.sh

#----
# Simple script to run CanaData.py, run CanaParse.py, and send and email with filtered results triggered by a crontask.
#----

#---- 
# To Use:
# Setup/configure an smtp relay server using postfix: https://www.linode.com/docs/email/postfix/configure-postfix-to-send-mail-using-gmail-and-google-apps-on-debian-or-ubuntu/ 
# Update the variable 'dirpath' below to match your full path to CanaData (like I have it)
# Update the variable 'state' below to your US state (like I have it)
# Update the variable 'email_reciever' below to your email address where you'd like to recieve the emails
# Update the variable 'virtualenvpath' below to the location of your virtualenv dir (or set this to an empty string if not using virtualenv)
# Setup crontab (this example runs everyday at 10:00 am):
#
# % sudo crontab -e
# 0 10 * * * bash /var/www/projects/CanaData/parse-scripts/email.sh > /var/log/flower-filter-email.log 2>&1
#
# Setup custom email filters based on the email subject "daily flowers" so you can organize your inbox when the emails start coming in. 
# 
# INFO: Spend time adjusting filters, etc. before trying to setup emails. Once your filters are ready, then come here. 
#----

#----BEGIN EDITABLE VARS----
dirpath=/var/www/projects/CanaData
state=nevada
email_reciever=reciever@gmail.com
email_sender=sender@gmail.com
#----END EDITABLE VARS-------

cd "$dirpath"
find . -type d -name "CanaData_*" -exec rm -r "{}" \; #remove any existing CVS downloads
python3 "$dirpath"/CanaData.py -go "$state"
cd "$dirpath"/parse-script/
python3 "$dirpath"/parse-script/CanaParse.py
mailx -a 'Content-Type: text/html' -s "daily flowers" "$email_reciever" -- -f "$email_sender" <"$dirpath"/parse-script/output/flower-filter-email.html