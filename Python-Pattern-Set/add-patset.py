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
import pdb

from pprint import pprint

from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
from nssrc.com.citrix.netscaler.nitro.exception.nitro_exception import nitro_exception
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsip import nsip
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsconfig import nsconfig
from nssrc.com.citrix.netscaler.nitro.resource.config.basic.service import service
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver import lbvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding import lbvserver_service_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver import csvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.policy.policypatset import policypatset
from nssrc.com.citrix.netscaler.nitro.resource.config.policy.policypatset_binding import policypatset_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.policy.policypatset_pattern_binding import policypatset_pattern_binding
from nssrc.com.citrix.netscaler.nitro.util.filtervalue import filtervalue

# This program uses the Nitro API to add pattern sets in a data file in JSON format
class NitroApp : 
	def __init__(self):
		_ip=""
		_username=""
		_password=""

	@staticmethod
	def main(cls, args_):
		if(len(args_) < 4):
			print("Usage: run.bat <ip> <username> <password> <pattern-set-datafilename>")
			return

		config = NitroApp()
		config.ip = args_[1]
		config.username = args_[2]
		config.password = args_[3]
		config.pfile = args_[4]
		
		try :
			
			#Create an instance of the nitro_service class to connect to the appliance
			ns_session = nitro_service(config.ip,"HTTP")
			
			ns_session.set_credential(config.username,config.password) #to make arguments more generic
			ns_session.timeout = 500
			#Log on to the appliance using your credentials

			print("Logging into NetScaler at " + config.ip + " with userid " + config.username)

			
			ns_session.login()



			print("Reading input file " + config.pfile)


                        with open(config.pfile,'r') as jfile:
                            jdata = json.load(jfile)
                        jfile.closed

#
#                      Strip the leading tag - we don't need it any more
#

                        pattern_sets = jdata['patsets']

                        for psname,bindings in pattern_sets.iteritems():
                            patset_obj = policypatset()
                            patset_obj.name = psname
                            print("Attempting to add patset " + patset_obj.name)
                            try:
                               policypatset.add(ns_session,patset_obj);
		            except nitro_exception as  e:
                               if e.errorcode == 273 :
                                  print ("Pattern set " + patset_obj.name + " is already defined.   Will attempt to add bindings anyway.")
                               else : 
			          print("Exception::errorcode="+str(e.errorcode)+",message="+ e.message)
			          print("Running configuration was NOT saved.  Logging out.")
                                  ns_session.logout()
                                  return

                            for b in bindings:
                              ppbinding_obj = policypatset_pattern_binding()
                              ppbinding_obj.name = patset_obj.name
                              ppbinding_obj.String = b['String']
                              ppbinding_obj.index = b['index']
                              ppbinding_obj.charset = b['charset']
                              try:
                                 print("Attempting to add  " + ppbinding_obj.name + "/" + ppbinding_obj.String)
                                 policypatset_pattern_binding.add(ns_session, ppbinding_obj)
                                 print(ppbinding_obj.name + "/" + ppbinding_obj.String + " added.")
                              except nitro_exception as e:
                                 if e.errorcode in [2830, 2883] :
                                    print ("This pattern or index is already defined.   Overwriting current definition with new values.")
                                    ppbinding_delete_obj = policypatset_pattern_binding()
                                    ppbinding_delete_obj.name = ppbinding_obj.name
                                    ppbinding_delete_obj.String = ppbinding_obj.String
                                    policypatset_pattern_binding.delete(ns_session, ppbinding_delete_obj)
				    policypatset_pattern_binding.add(ns_session, ppbinding_obj)
                                 else :
			            print("Exception::errorcode="+str(e.errorcode)+",message="+ e.message)
			            print("Running configuration was NOT saved.  Logging out.")
                                    ns_session.logout()
                                    return
                                 


			# Uncomment the line below and indent properly to save the configurations
			# ns_session.save_config()
			



                        print ("Running configuration was NOT saved.  Logging out")
			
			
			
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
			patsetfile =sys.argv[4]
			NitroApp().main(NitroApp(),sys.argv)
	except SystemExit:
		print("Exception::Usage: Sample.py <directory path of Nitro.py> <nsip> <username> <password> <pattern-set-datafile-name>")

