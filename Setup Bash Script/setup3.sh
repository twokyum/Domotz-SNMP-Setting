#!/bin/bash
#Step3 - Domotz Agent Install
sudo apt-get update && sudo apt-get -y upgrade
wget https://portal.domotz.com/download/agent_packages/domotz-raspberry-armhf-1.0-2.5.0-2.7.5-b004-0023.deb
sudo dpkg -i domotz-raspberry-armhf-1.0-2.5.0-2.7.5-b004-0023.deb