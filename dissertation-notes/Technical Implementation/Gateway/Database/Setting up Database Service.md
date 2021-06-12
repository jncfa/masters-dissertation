## Requirements for setting up the database service
#database #getting-started

```bash
# Create the file repository configuration:
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb\_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update the package lists:
sudo apt-get update 

# Install the latest version of PostgreSQL.
sudo apt install -y postgresql-12

# Downgrade libpq5 to install headers and dev packages (known bug, check if the version is the same!)
sudo apt install libpq5=12.6-0ubuntu0.20.04.1
sudo apt install postgresql-server-dev-12
```


### (Optional) Add GUI client for managing the database service

```bash
# Install the public key for the repository (if not done previously):
sudo curl https://www.pgadmin.org/static/packages\_pgadmin\_org.pub | sudo apt-key add

  
# Create the repository configuration file:
sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb\_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'

  
# Install both desktop and web modes
sudo apt install pgadmin4

  
# Configure the webserver
sudo /usr/pgadmin4/bin/setup-web.sh

```