# General Information
#gateway 

## Getting Started
#todo: add links for each getting started related to gateway 
[[Getting Started with Gateway]], [[Setting up Database Service]], [[Setting up MQTT broker]]


## Security Details
#security
- Password: wow2020
- Details for generating certificates: https://www.ibm.com/support/knowledgecenter/SSB23S_1.1.0.2020/gtps7/cfgcert.html

## Other commands
 - Creating system user without password
```
sudo adduser \
   --system \
   --shell /bin/bash \
   --gecos ‘User for running the Python3 DB service’ \
   --ingroup sqluser \
   --disabled-login \
   --home /home/pyservice \
   pyservice
```