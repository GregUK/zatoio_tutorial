zatoio_tutorial
===============

Zato tutorial using postgres, redis, rabbitmq deployed via Vagrant

Following the tutorial at https://zato.io/docs/tutorial/01.html and https://zato.io/docs/tutorial/02.html

Setup
=====

After cloning use the vagrant cloud image for ubuntu/trusty

```bash
 vagrant box add ubuntu\trusty https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box
```

Create the VM's and initialise using

```bash
 vagrant up
```

This will create four VM's: postgresdb, rabbitmq, zatoweb, djangoweb

The tutorial currently only requires zatoweb and postgresdb

to access the servers using vagrant e.g.
```bash
 vagrant ssh postgresdb
 vagrant ssh rabbitmq
 vagrant ssh zatoweb
 vagrant ssh djangoweb
```

After initialisation logon to the zatoweb, the vagrant file creates the base cluster however it isnt started by default
```bash
 vagrant ssh zatoweb
 sudo su - zato

 #Create the cluster
 #quickstart create takes zato quickstart create $path \
 #    postgresql $odb_host $odb_port $odb_user $odb_db_name \
 #    $kvdb_host $kvdb_port --verbose
 zato quickstart create /usr/share/zato postgresql 10.0.0.4 5432 zato1 zato1 localhost 6379 --verbose

 #When prompeted enter 'zato1' as the DB user and password
 #Dont enter a password or user of kvdb as these use the defaults
 #note the generated password. e.g. ikik-oreb-oteh-amel"

 #Start zato
 /usr/share/zato/zato-qs-start.sh

 #zato cluster is installed in /usr/share/zato
```

After starting you can access the admin interface from your host machine at http://localhost:8183 as the port has been forwarded

For convenience the files used in the tutorial are available within vagrant from 
```
/vagrant/services/
```

these can be used for hot deployment throughout the tutorials

