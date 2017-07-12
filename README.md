nsAuto
======
This script is used to interact with CPX in a sandbox environment and apply a simple Load Balancer configuration. Once you have deployed the CPX within a docker network, you can run the script via the [Nitro-IDE](https://github.com/Citrix-TechSpecialist/nitro-ide/) to configure the NetScaler CPX. See [Getting Started](https://github.com/Citrix-TechSpecialist/nitro-ide/#Getting-Started) section for instruction on how to execute the code. 

You use the `nsAutoCfg.json` file to specify the configuration. Check the [nsAutoCfg file](nsAutoCfg.json) out for what all you can do to configure the NetScaler with the [nsAuto.py](nsAuto.py) python script. 

## Requirements

The NetScaler Python SDK, can download from a NetScaler 10.5 or up

Python module requirements: 

* [requests](http://docs.python-requests.org/en/master/)
  * Install via `pip install requests` if needed

## Running

Run Script via: `python nsAuto.py` in the same directory as your [nsAutoCfg file](nsAutoCfg.json). 

You can setup a [sandbox environment](https://github.com/Citrix-TechSpecialist/nitro-ide/) via `docker-compose` and run the command in its terminal after cloning the repository.
