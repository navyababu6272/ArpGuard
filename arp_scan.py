#!/usr/bin/env python3

# import the serious stuff
import subprocess
import urllib.request as urllib2
import json
import codecs

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
            print("\n")
            print("IP Address\t:", row[0])
            print("MAC ID\t\t:", row[1])
            
            
        else:
            break
    for row in arp_list:
        if len(row) != 0:
            lst=row[1]
            
            
            request = urllib2.Request(url+lst, headers={'User-Agent' : "API Browser"}) 
            response = urllib2.urlopen( request )
            reader = codecs.getreader("utf-8")
            obj = json.load(reader(response))
            print ("\n")
            print (obj['result']['company']);
   
    #print company address
            print (obj['result']['address']);

# call the main function
main()
