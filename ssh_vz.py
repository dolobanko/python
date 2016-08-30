#!/usr/bin/env python

import os
import argparse
import pexpect

global p
p = argparse.ArgumentParser()
p.add_argument ('host', type=str,  help="Host to connect")
arg = vars(p.parse_args())

def main ():
        connect = traceroute(arg['host'])
        root_host=connect[-2].split()[1]
        if len(connect) == 4:
                host=connect[-1].split()[1].split('.')[0]
                os.system ('ssh -t ' + root_host + ' sudo /usr/sbin/vzctl enter ' +host)
        else:
                os.system ('ssh-t ' + root_host + ' sudo -s')

def traceroute(host):
        tracert = pexpect.spawn('traceroute -4 ' + host)
        line = tracert.readlines()
        return line

if __name__ == "__main__":
        main()