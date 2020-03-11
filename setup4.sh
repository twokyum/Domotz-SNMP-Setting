#!/bin/bash
#Step 4 - Make Directory for temp values  serial open 

sudo raspi-config
#7 Advanced Options A1 Expand Filesystem
#5 Interfacing Options P6 Serial
sudo apt-get update
sudo nano /boot/config.txt
#dtoverlay=pi3-disable-bt
sudo systemctl disable hciuart
sudo apt-get install -y python-serial
wget lechacal.com/RPICT/tools/lcl-rpict-config.py.zip
unzip lcl-rpict-config.py.zip
sudo cp lcl-rpict-config.py /usr/local/bin


sudo mkdir /usr/local/bin/Logging_Data
sudo chmod 777 /usr/local/bin/Logging_Data
cd /usr/local/bin/Logging_Data
sudo touch temperature.log
sudo chmod 777 /usr/local/bin/Logging_Data/temperature.log

sudo reboot&exit