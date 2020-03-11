#!/bin/bash
#VNC Remote Access Setup
sudo apt-get update && apt-get upgrade -y
sudo apt install -y realvnc-vnc-server realvnc-vnc-viewer
sudo raspi-config
