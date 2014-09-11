#!/bin/bash

sudo apt-get install apt-transport-https python-software-properties software-properties-common curl
curl -s https://zato.io/repo/zato-0CBD7F72.pgp.asc | sudo apt-key add -
sudo apt-add-repository https://zato.io/repo/stable/ubuntu
sudo apt-get install zato
