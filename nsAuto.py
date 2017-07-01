#!/usr/bin/env python

import base64
import os
import requests
import json
import time
import threading
from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
from nssrc.com.citrix.netscaler.nitro.exception.nitro_exception import nitro_exception
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsip import nsip
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nshostname import nshostname
from nssrc.com.citrix.netscaler.nitro.resource.config.dns.dnsnameserver import dnsnameserver
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsconfig import nsconfig
from nssrc.com.citrix.netscaler.nitro.resource.config.system.systemfile import systemfile
from nssrc.com.citrix.netscaler.nitro.resource.config.basic.service import service
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver import lbvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding import lbvserver_service_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver import csvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.ha.hanode import hanode


class netScaler:
    """This class reperesents a connection to a NetScaler using NITRO. Class
    Methods below provide functionality to interact with the NetScaler."""

    def __init__(self, conf):
        #initlization
        self.cfg = conf
        self.ns_session = ""

    def initConnection(self):
        """Create the NetScaler session using HTTP, passing in the credentials
        to the NSIP"""
        try:
            self.ns_session = nitro_service(self.cfg['config']['nsip'],"HTTP")
            self.ns_session.set_credential(self.cfg['config']['username'],self.cfg['config']['password'])
            self.ns_session.timeout = 300
            self.ns_session.login()

        except nitro_exception as e:
            print("Exception::errorcode=" +
                  str(e.errorcode) + ",message=" + e.message)
        except Exception as e:
            print("Exception::message=" + str(e.args))

        return

    def savec(self):
        """Simple class used to save the config of the NS"""
        try:
            self.ns_session.save_config()

        except nitro_exception as e:
            print("Exception::errorcode=" +
                  str(e.errorcode) + ",message=" + e.message)
        except Exception as e:
            print("Exception::message=" + str(e.args))

        return

    def closeConnection(self, savec=False):
        """Close the session.  Can pass in if you wish to save the config or
        not.  Defaults to not saving the config"""
        try:
            if savec:
                self.savec()

            self.ns_session.logout()

        except nitro_exception as e:
            print("Exception::errorcode=" +
                  str(e.errorcode) + ",message=" + e.message)
        except Exception as e:
            print("Exception::message=" + str(e.args))

        return

    def hostNameDnsTz(self):
        """Configure the HostName, DNS, and Time Zone for the NetScaler."""
        # Begin by setting the hostname
        try:
            newNsHostname = nshostname()
            newNsHostname.hostname = self.cfg['config']['hostname']
            nshostname.update(self.ns_session, newNsHostname)

        except nitro_exception as e:
            print("Exception::errorcode=" +
                  str(e.errorcode) + ",message=" + e.message)
        except Exception as e:
            print("Exception::message=" + str(e.args))

        # Add DNS Entries, traverse the dns class variable and add the
        # nameservers
        for dns in self.cfg['config']['dns']:
            try:
                newDNS = dnsnameserver()
                newDNS.ip = dns['nameserver']
                dnsnameserver.add(self.ns_session, newDNS)

            except nitro_exception as e:
                print("Exception::errorcode=" +
                      str(e.errorcode) + ",message=" + e.message)
            except Exception as e:
                print("Exception::message=" + str(e.args))

        # Configure the NetScaler TimeZone
        try:
            nsconf = nsconfig()
            nsconf.timezone = self.cfg['config']['tz']
            nsconfig.update(self.ns_session, nsconf)

        except nitro_exception as e:
            print("Exception::errorcode=" +
                  str(e.errorcode) + ",message=" + e.message)
        except Exception as e:
            print("Exception::message=" + str(e.args))

        return

    def confFeatures(self):
        """Configure the features for the NetScaler"""
        en = []
        dis = []

        for feature in self.cfg['config']['features']:
            if feature['enable']:
                #If we hit a feature to enable, add it to the en list
                en.append(feature['feature'])
            else:
                #Add it to the dis list if we need to disable the feature
                dis.append(feature['feature'])
        try:
            if en:
                #Send all enable features at once
                self.ns_session.enable_features(en)
            if dis:
                #Send all disable features at once
                self.ns_session.disable_features(dis)

        except nitro_exception as e:
            print("Exception::errorcode=" +
                  str(e.errorcode) + ",message=" + e.message)
        except Exception as e:
            print("Exception::message=" + str(e.args))

        return

    def confModes(self):
        """Configure the modes for the NetScaler"""
        en = []
        dis = []

        for mode in self.cfg['config']['modes']:
            if mode['enable']:
                #If we need to enable modes, add it to the en list
                en.append(mode['mode'])
            else:
                #add it to the dis list...
                dis.append(mode['mode'])
        try:
            if en:
                #Send all at once
                self.ns_session.enable_modes(en)
            if dis:
                self.ns_session.disable_modes(dis)

        except nitro_exception as e:
            print("Exception::errorcode=" +
                  str(e.errorcode) + ",message=" + e.message)
        except Exception as e:
            print("Exception::message=" + str(e.args))

        return

    def addServices(self):
        """Configure the services for the NetScaler"""
        if "services" in self.cfg.keys():
            #Lets loop through all the services
            for svc in self.cfg['services']:
                try:
                    #Setup the new service
                    newSVC = service()
                    newSVC.name = svc['name']
                    newSVC.ip = svc['ip']
                    newSVC.port = svc['port']
                    newSVC.servicetype = svc['type']

                    #Add the new service
                    service.add(self.ns_session, newSVC)

                except nitro_exception as e:
                    print("Exception::errorcode=" +
                          str(e.errorcode) + ",message=" + e.message)
                except Exception as e:
                    print("Exception::message=" + str(e.args))

        return

    def addLBVServers(self):
        """Configure the lbvservers for the NetScaler"""
        if "lbvs" in self.cfg.keys():
            #Lets loop through all lbvservers
            for lbvs in self.cfg['lbvs']:
                try:
                    #Setup a new lbvserver
                    newLBVS = lbvserver()
                    newLBVS.name = lbvs['name']
                    newLBVS.servicetype = lbvs['servicetype']
                    newLBVS.ipv46 = lbvs['ipv46']

                    #check these optional values
                    if "port" in lbvs.keys():
                        newLBVS.port = lbvs['port']
                    if "persistencetype" in lbvs.keys():
                        newLBVS.persistencetype = lbvs['persistencetype']
                    if "lbmethod" in lbvs.keys():
                        newLBVS.lbmethod = lbvs['lbmethod']

                    #Add the lbvs
                    response = lbvserver.add(self.ns_session, newLBVS)
                    if response.severity and response.severity == "WARNING":
                        print("\tWarning : " + response.message)

                except nitro_exception as e:
                    print("Exception::errorcode=" +
                          str(e.errorcode) + ",message=" + e.message)
                except Exception as e:
                    print("Exception::message=" + str(e.args))

                #If we have services to bind, lets do it.
                if "services" in lbvs.keys():
                    for svc in lbvs['services']:
                        #Create a new binding
                        newSVCBinding = lbvserver_service_binding()
                        newSVCBinding.name = lbvs['name']
                        newSVCBinding.servicename = svc['servicename']
                        newSVCBinding.weight = svc['weight']

                        #Add the binding!
                        try:
                            lbvserver_service_binding.add(self.ns_session,
                                                          newSVCBinding)
                        except nitro_exception as e:
                            print("Exception::errorcode=" +
                                  str(e.errorcode) + ",message=" + e.message)
                        except Exception as e:
                            print("Exception::message=" + str(e.args))
        return

def confNS(ns):
    """ This is used to preform the basic configuration of the NetScaler being
    passed in to the function"""
    # Lets get the initial config done and license the box
    ns.initConnection()
    ns.hostNameDnsTz()

    # Configure modes and features
    ns.confFeatures()
    ns.confModes()

    # Next lets add services and configure VServers
    ns.addServices()
    ns.addLBVServers()

    # Were done here, lets save and close the connection
    ns.savec()
    ns.closeConnection()

if __name__ == '__main__':
    """ This is our main thread of execution, it starts all the work!"""
    # read in cnfig http://www.objgen.com/json/models/mdui
    fin = open("nsAutoCfg.json", "r")
    json_raw = fin.read()
    fin.close()
    jsn = json.loads(json_raw)

    # Create some threads and netscalers
    threads = []

    for nscfg in jsn['ns']:
        print("Configuring NS " + nscfg['config']['hostname'])
        ns = netScaler(nscfg)

        # Create a thread object and add it to our list of threads
        t = threading.Thread(target=confNS, args=(ns,))
        t.daemon = True
        threads.append(t)

    print "Starting to configure..."

    # Lets start the threads -- If there are many NetScalers, we might want to
    # Slow this part down, rather than run them all at once...
    [x.start() for x in threads]

    # Lets wait for them to finish
    [x.join() for x in threads]

    print "All done preforming configuration"

"""
- create connection into NS
- creating first snip
- hostname
- dns
- TZ
- licensing
- reboot
- HA pair
- LB Vserver
* Content switching example
* SSL
* enabling basic AppFW?
"""
