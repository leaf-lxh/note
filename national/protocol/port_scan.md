## 端口扫描

2019-5-17

### easy way

[scan_nmap.py](./code/scan_nmap.py)

使用python调用nmap进行扫描

安装nmap以及python接口

```
$ sudo apt-get install nmap python3-nmap
```

python调用

```python
#!/usr/bin/python3
#coding: utf8
import argparse #replacement for optparse after python3.2
import nmap

usage = """
        lxh port scanner.
        usage:
        scan one host: scan_tool.py --host 127.0.0.1 --port 22 33 44 55
        scan multiple hosts: scan_tool.py --host 192.168.247.1-254 --port 22-50
        """
def DoScan(target):
    """
    Scan host
    retn: {"uphost1": [(open_port1, state)], "uphost2": [(open_port1,state)]}
    """
    scanner = nmap.PortScanner()
    report = scanner.scan(target.keys()[0], ",".join(target.values()[0]), arguments="")
    
    result = {}
    for host in report["scan"]:
        result[host] = [(port, report["scan"][host]["tcp"][port]["state"]) for port in report["scan"][host]["tcp"].keys()]

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


```



### normal way

[scan_scapy.py](./code/scan_scapy.py)

使用python调用scapy库进行端口扫描



### hard way

 直接用套接字API