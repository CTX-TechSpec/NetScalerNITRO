#!/usr/bin/env python

#
# Copyright (c) 2008-2015 Citrix Systems, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License")
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http:#www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import sys

import base64
import os
import requests
import json
import time
import threading
### import pdb

from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
from nssrc.com.citrix.netscaler.nitro.exception.nitro_exception import nitro_exception
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsip import nsip
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsconfig import nsconfig
from nssrc.com.citrix.netscaler.nitro.resource.config.basic.service import service
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver import lbvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding import lbvserver_service_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver import csvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.policy.policypatset import policypatset
from nssrc.com.citrix.netscaler.nitro.util.filtervalue import filtervalue

# This program uses the Nitro API to delete a pattern set
class NitroApp : 
	def __init__(self):
		_ip=""
		_username=""
		_password=""

	@staticmethod
	def main(cls, args_):
		if(len(args_) < 4):
			print("Usage: run.bat <ip> <username> <password> <pattern-set-name>")
			return

		config = NitroApp()
		config.ip = args_[1]
		config.username = args_[2]
		config.password = args_[3]
		config.patset = args_[4]
		
		try :
			
			#Create an instance of the nitro_service class to connect to the appliance
			ns_session = nitro_service(config.ip,"HTTP")
			
			ns_session.set_credential(config.username,config.password) #to make arguments more generic
			ns_session.timeout = 500
			#Log on to the appliance using your credentials

			print("Logging into NetScaler at " + config.ip + " with userid " + config.username)

			
			ns_session.login()
			
                        print("Looking for a pattern named " + config.patset)


			patset_list = policypatset.get(ns_session)


                        for patset_obj in patset_list :
                           if patset_obj.name == config.patset :
			      print("Deleting patset named " + patset_obj.name)
                              policypatset.delete(ns_session, patset_obj)
			      
                              #Uncomment the lines below to save the configurations
			      # print("Saving the configuration.")
			      # ns_session.save_config()

                              # Comment the line below if you choose to save the configuration.
			      print("The running configuration was NOT saved.")

                              break
                        else: 
                           print("patset " + config.patset + " was not found in the configuration.")
                        print ("Logging out")
			
			
			
			#Logout from the NetScaler appliance
			ns_session.logout()
			
		except nitro_exception as  e:
			print("Exception::errorcode="+str(e.errorcode)+",message="+ e.message)
		except Exception as e:         
			print("Exception::message="+str(e.args))
		return

#
# Main thread of execution
#

if __name__ == '__main__':
	try:
		if len(sys.argv) != 5:
			sys.exit()
		else:
			ipaddress=sys.argv[1]
			username=sys.argv[2]
			password=sys.argv[3]
			patset=sys.argv[4]
			NitroApp().main(NitroApp(),sys.argv)
	except SystemExit:
		print("Exception::Usage: Sample.py <directory path of Nitro.py> <nsip> <username> <password> <pattern-set-name>")

