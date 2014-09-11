# -*- mode: ruby -*-
# vi: set ft=ruby :

$POSTGRES_SETUP_SCRIPT = <<SCRIPT
    #Creates user zato1 with password zato1 and db zato1, assumes using postgres 9.3`
    sudo apt-get -y install postgresql

    echo "Creating zato1 DB and zato1 user"
    sudo -H -u postgres bash -c "createuser --no-superuser --no-createdb --no-createrole zato1"
    echo "Creating zato DB"
    sudo -H -u postgres bash -c 'createdb --owner=zato1 zato1'
    echo "Creating password for zato1 user to zato1"
    sudo -H -u postgres bash -c "psql --dbname zato1 --command=\"ALTER ROLE zato1 WITH PASSWORD 'zato1'\""

    echo "Updating pg_hba.conf to allow access for zato using postgres version 9.3"
    sudo -H -u postgres bash -c 'echo "hostssl    zato1      zato1             10.0.0.2/32          password" >> "/etc/postgresql/9.3/main/pg_hba.conf"'
    sudo sed -i "s/\#listen_addresses \=.*/listen_addresses ='10.0.0.4'/" /etc/postgresql/9.3/main/postgresql.conf

    echo "restarting postgres"
    sudo service postgresql restart
SCRIPT

$RABBIT_SETUP_SCRIPT = <<SCRIPT
    sudo apt-get -y install rabbitmq-server
    sudo rabbitmq-plugins enable rabbitmq_management_visualiser
    sudo service rabbitmq-server restart
SCRIPT

$ZATO_SETUP_SCRIPT = <<SCRIPT
    sudo apt-get -y install apt-transport-https python-software-properties software-properties-common curl redis-server
    echo "adding zato apt repo"
    curl -s https://zato.io/repo/zato-0CBD7F72.pgp.asc | sudo apt-key add -
    sudo apt-add-repository https://zato.io/repo/stable/ubuntu
    sudo apt-get update > /dev/null
    echo "installing zato"
    sudo apt-get -y install zato

    echo "creating quickstart zato cluster for redis and postgres, assuming vagrant setup completed for postgres node"
    sudo mkdir -p /usr/share/zato
    sudo chown zato:zato /usr/share/zato
SCRIPT

$DJANGO_SETUP_SCRIPT = <<SCRIPT
    echo "Django setup script TBD"
SCRIPT

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  config.vm.define :rabbitmq do |rabbitmq|
    rabbitmq.vm.box = "ubuntu/trusty64"
    rabbitmq.vm.hostname = "rabbitmq"
    rabbitmq.vm.network "private_network", ip: "10.0.0.3"
    # Run the shell script inline provisioner
    rabbitmq.vm.provision "shell", inline: $RABBIT_SETUP_SCRIPT
  end

  config.vm.define :postgresdb do |postgresdb|
    postgresdb.vm.box = "ubuntu/trusty64"
    postgresdb.vm.hostname = "postgresdb"
    postgresdb.vm.network "private_network", ip: "10.0.0.4"
    # Run the shell script inline provisioner
    postgresdb.vm.provision "shell", inline: $POSTGRES_SETUP_SCRIPT
  end
 
  config.vm.define :djangoweb do |djangoweb|
    djangoweb.vm.box = "ubuntu/trusty64"
    djangoweb.vm.hostname = "djangoweb"
    djangoweb.vm.network "private_network", ip: "10.0.0.5"
    # Run the shell script inline provisioner
    djangoweb.vm.provision "shell", inline: $DJANGO_SETUP_SCRIPT
  end

  config.vm.define :zatoweb do |zatoweb|
    zatoweb.vm.box = "ubuntu/trusty64"
    zatoweb.vm.hostname = "zatoweb"
    zatoweb.vm.network :forwarded_port, guest: 8183, host: 8183
    zatoweb.vm.network :forwarded_port, guest: 11223, host: 11223
    zatoweb.vm.network "private_network", ip: "10.0.0.2"
    # Run the shell script inline provisioner
    zatoweb.vm.provision "shell", inline: $ZATO_SETUP_SCRIPT
  end

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  # config.vm.box_url = "http://domain.com/path/to/above.box"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network :forwarded_port, guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network :private_network, ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network :public_network

  # If true, then any SSH connections made will enable agent forwarding.
  # Default value: false
  # config.ssh.forward_agent = true

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider :virtualbox do |vb|
  #   # Don't boot with headless mode
  #   vb.gui = true
  #
  #   # Use VBoxManage to customize the VM. For example to change memory:
  #   vb.customize ["modifyvm", :id, "--memory", "1024"]
  # end
  #
  # View the documentation for the provider you're using for more
  # information on available options.

  # Enable provisioning with Puppet stand alone.  Puppet manifests
  # are contained in a directory path relative to this Vagrantfile.
  # You will need to create the manifests directory and a manifest in
  # the file ubuntu/trusty64.pp in the manifests_path directory.
  #
  # An example Puppet manifest to provision the message of the day:
  #
  # # group { "puppet":
  # #   ensure => "present",
  # # }
  # #
  # # File { owner => 0, group => 0, mode => 0644 }
  # #
  # # file { '/etc/motd':
  # #   content => "Welcome to your Vagrant-built virtual machine!
  # #               Managed by Puppet.\n"
  # # }
  #
  # config.vm.provision :puppet do |puppet|
  #   puppet.manifests_path = "manifests"
  #   puppet.manifest_file  = "site.pp"
  # end

  # Enable provisioning with chef solo, specifying a cookbooks path, roles
  # path, and data_bags path (all relative to this Vagrantfile), and adding
  # some recipes and/or roles.
  #
  # config.vm.provision :chef_solo do |chef|
  #   chef.cookbooks_path = "../my-recipes/cookbooks"
  #   chef.roles_path = "../my-recipes/roles"
  #   chef.data_bags_path = "../my-recipes/data_bags"
  #   chef.add_recipe "mysql"
  #   chef.add_role "web"
  #
  #   # You may also specify custom JSON attributes:
  #   chef.json = { :mysql_password => "foo" }
  # end

  # Enable provisioning with chef server, specifying the chef server URL,
  # and the path to the validation key (relative to this Vagrantfile).
  #
  # The Opscode Platform uses HTTPS. Substitute your organization for
  # ORGNAME in the URL and validation key.
  #
  # If you have your own Chef Server, use the appropriate URL, which may be
  # HTTP instead of HTTPS depending on your configuration. Also change the
  # validation key to validation.pem.
  #
  # config.vm.provision :chef_client do |chef|
  #   chef.chef_server_url = "https://api.opscode.com/organizations/ORGNAME"
  #   chef.validation_key_path = "ORGNAME-validator.pem"
  # end
  #
  # If you're using the Opscode platform, your validator client is
  # ORGNAME-validator, replacing ORGNAME with your organization name.
  #
  # If you have your own Chef Server, the default validation client name is
  # chef-validator, unless you changed the configuration.
  #
  #   chef.validation_client_name = "ORGNAME-validator"
end
