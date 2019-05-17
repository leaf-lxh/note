import argparse #replacement for optparse after python3.2
import nmap

def DoScan(target):
    """
    Scan host
    retn:
    """
    pass

def GetOption():
    """
    Get the target host and port from the arguments
    retn: A dictionary contents the results.
          Like {"host1":[port1, port2], "host2":[port1,port2]}
    """
    pass

def main():
    target = GetOption()
    result = DoScan(target)
    


if __name__ == "__main__":
    main()

