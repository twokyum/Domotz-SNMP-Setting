#!/bin/bash
#SNMP Service Setup & Cacti Download
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y snmp snmp-mibs-downloader
sudo apt-get update
sudo apt-get install -y snmpd
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y cacti