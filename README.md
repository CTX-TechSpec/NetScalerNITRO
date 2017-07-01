nsAuto
======
This script is used to interact with CPX in a sandbox environment and apply a simple Load Balancer configuration.  Once you have deployed the CPX within a docker network, you can run the script via the [Nitro-IDE](TBD) to configure the NetScaler CPX.

You use the `nsAutoCfg.json` file to specify the configuration. Check the [file](nsAutoCfg.json) out for what all you can do to configure the NetScaler.

## Requirements
NetScaler(s) 10.1 or up

The NetScaler Python SDK, can download from a NetScaler 10.5 or up

Python module requirments: paramiko, requests (Install both via "pip install MODULENAME")

## Running

Run Script via: `python nsAuto.py` using the `docker-compose` deployment of the [Nitro-IDE](TBD) project.

# Example Tutorial

PLACE HOLDER --- TBD ---