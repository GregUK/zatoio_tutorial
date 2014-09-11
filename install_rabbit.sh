#!/bin/bash

sudo apt-get update
sudo apt-get install rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management_visualiser
sudo service rabbitmq restart

