#!/usr/bin/python3
#coding: utf8
import argparse #replacement for optparse after python3.2
from scapy.all import *
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

usage = """
        lxh port scanner.
        usage:
        scan one host: scan_tool.py --host 127.0.0.1 --port 22 33 44 55
        scan multiple hosts: scan_tool.py --host 192.168.247.1-254 --port 22-50
        """
def DoScan(target, SYN=False, FIN=False):
    """
    Scan host
    retn: {"uphost1": [(open_port1, state)], "uphost2": [(open_port1,state)]}
    """
    result = {}
    for host in target:
        result[host]=[]
        for port in target[host]:
            ret = None
            if SYN == True:
                ret = sr1(IP(dst=host)/TCP(dport=int(port), flags="S"), timeout=5, verbose=0)
            elif FIN == True:
                ret = sr1(IP(dst=host)/TCP(dport=int(port), flags="F"), timeout=5, verbose=0)
            else:
                ret = sr1(IP(dst=host)/TCP(dport=int(port)), timeout=5, verbose=0)
            
            if ret != None:
                if ret.getlayer(TCP).__str__() !=  'RA':
                    result[host].append((port, "open"))
                    continue
            result[host].append((port, "closed"))
    
    return result

def GetOption():
    """
    Get the target host and port from the arguments
    retn: A dictionary contents the results.
          Like {"host":[port1, port2, ...]"}
    """
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("--host", nargs=1, dest="host", type=str, help="The host to be scaned. "
                        "If you want to scan multi-hosts, the format should like xx.xx.xx.1-254"
                       )
    parser.add_argument("--ports", nargs="+", dest="ports", type=str, help="The port to be scaned."
                        "Each port should be splited by a space ( )."
                       )
    args = parser.parse_args()
    if None in [args.host, args.ports]:
        print(parser.description)
        exit(0)
    return {args.host[0]:args.ports}

def main():
    target = GetOption()
    result = DoScan(target)
    for host in result:
        print("up host: {}".format(host))
        for port_info in result[host]:
            print("\t{} tcp/{}\n".format(port_info[1], port_info[0]))


if __name__ == "__main__":
    main()

