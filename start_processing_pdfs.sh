#!/bin/bash

figlet "processing pdfs"
cd /home/pi/development/sylloge_web/sylloge_of_codes/sylloge_of_codes
source ../bin/activate
process_pdfs development.ini
