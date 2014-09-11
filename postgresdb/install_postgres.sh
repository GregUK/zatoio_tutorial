#!/bin/bash

#sudo apt-get update
#sudo apt-get install postgresql

sudo -H -u postgres bash -c 'createuser --no-superuser --no-createdb --no-createrole zato1; createdb --owner=zato1 zato1'
sudo -H -u postgres bash -c "psql --dbname zato1 --command=\"ALTER ROLE zato1 WITH PASSWORD 'zato1'\""
