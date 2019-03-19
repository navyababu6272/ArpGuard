#!/usr/bin/env python3

# import the serious stuff
import subprocess


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
            print("Manufacturer\t:", row[2])
        else:
            break


# call the main function
main()
