#!/bin/bash

#Creates user zato1 with password zato1 and db zato1, assumes using postgres 9.3`
sudo apt-get update
sudo apt-get install postgresql

echo "Creating zato1 DB and zato1 user" 
sudo -H -u postgres bash -c "createuser --no-superuser --no-createdb --no-createrole zato1"
echo 'createdb --owner=zato1 zato1'
echo "Creating password for zato1 user to zato1"
sudo -H -u postgres bash -c "psql --dbname zato1 --command=\"ALTER ROLE zato1 WITH PASSWORD 'zato1'\""

echo "Updating pg_hba.conf to allow access for zato using postgres version 9.3"
sudo -H -u postgres bash -c 'echo "hostssl    zato1      zato1             zato1          password" >> "/etc/postgresql/9.3/main/pg_hba.conf"'

echo "restarting postgres"
sudo service postgresql restart

