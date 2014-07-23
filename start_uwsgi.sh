#!/bin/bash
figlet "starting uwsgi"
cd /home/pi/development/sylloge_web/sylloge_of_codes/sylloge_of_codes
source ../bin/activate
uwsgi --ini-paste production.ini
echo "Sleeping for 30s"
sleep 30
echo "Done"
