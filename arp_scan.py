#!/usr/bin/env python3

# import the serious stuff
import subprocess
import urllib.request as urllib2
import json
import codecs
import re
url = "http://macvendors.co/api/"

# the main function
def main():
  

    # run the command
    arp_scan = subprocess.run(
        ["arp-scan", "-l"],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    # get the output
    arp_out = arp_scan.stdout.decode()

    # split the output into a recursive list
    arp_list = [x.split() for x in arp_out.split("\n")]

    # the scanned MACs starts from third row
    arp_list = arp_list[2:]

    # print the stuff
    for row in arp_list:
        if len(row) != 0:
           
            print("IP Address\t:", row[0])
            print("MAC ID\t\t:", row[1])
            print("\n")
        else:
            break
    #mac Vendor lookup
    for row in arp_list:

        if len(row) != 0:
            phone=[]
            lst=row[1]
            request = urllib2.Request(url+lst, headers={'User-Agent' : "API Browser"}) 
            response = urllib2.urlopen( request )
            reader = codecs.getreader("utf-8")
            obj = json.load(reader(response))
            mac=(obj['result']['mac_prefix']);
            vendor=(obj['result']['company']);
            phone=[mac]
            #printing mac prefix and vendor name
            print("--------------------------------------------")
            print("MAC Prefix:",mac)
            print("Vendor:",vendor)
            print("--------------------------------------------")

            #opening mobile_mac file  
            # define empty list
            mob = []
           

            # open file and read the content in a list
            with open('phone.txt', 'r') as filehandle:  
                filecontents = filehandle.readlines()

                for line in filecontents:
            # remove linebreak which is the last character of the string
                    current_phone = line[:-1]

            # add item to the list
                    mob.append(current_phone)
            
                    
                
            #identifying mobiles connected in wifi
                
                for item in mob:                     #mac contains list of mac_prefix of device connected to network
                    for item1 in phone:                #phone contains mac_prefixof all mobile phones
                       if item == item1:
                           print ("This is a mobile and he mac prefix is",item)
                      
                 
        else:
            break

# call the main function
main()
