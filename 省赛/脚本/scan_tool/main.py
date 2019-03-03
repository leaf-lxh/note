#!/usr/bin/python3.6
#coding:utf8

import os
import subprocess
import sys


import re
nojs = True

def GetCurrentDirStructure(directory):
    """
    By using system command 'ls', identify the files and directories. And save the result in a list.
    Be awared, this function doesn't prevent command injection. 
    parm:
        directory: the disired directory to identify
    return:
        a list, like such a structure [[directory1, directory2, ...], [file1, file2, ...]]
        if there is no file or directory, the list of it will be equal with [[], []], not []
    """

    #for linux:
    command = "ls -la %s" % directory

    #In python3.7, new option 'capture_output=True' has same effect of stdin,stdout=PIPE
    #result = subprocess.run(command, shell = True, capture_output = True, encoding='utf8').stdout
    result = subprocess.run(command, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, encoding='utf8').stdout
    
    struct = [[],[]]

    pathes = result.split("\n")

    for path in pathes:
        if path[0:1] == 'd':
            directoryName = path[path.rfind(" ") + 1:]
            if directoryName not in ('..', '.'):
                struct[0].append(directoryName)

        elif path[0:1] == '-':
            fileName = path[path.rfind(" ") + 1:]
            struct[1].append(fileName)

    return struct

def ScanVulnerabilities(webPath, keyword):
    """
    Scan files. Looking for the files that contents keyword. Print the file names with the keyword's line number.
    parm:
        webPath: The web folder to be scaned.
    retn:
        None
    """
    
    if webPath[-1] is not '/':
           webPath += '/'
 
    struct = GetCurrentDirStructure(webPath)
    print("Directory %s :" % webPath)
    for _file in struct[1]:
        try:
            if nojs == True:
                if _file[_file.rfind('.'):] == '.js':
                    continue

            with open(''.join([webPath, _file]), 'r') as f:
                lines = f.readlines();
                index = 0
                for line in lines:
                    index += 1
                    if None is not re.search(keyword,line):
                        print("    %s, line %d matched:\n       %s" % (_file, index, line))
        except:
            continue

    for directory in struct[0]:
       ScanVulnerabilities(''.join([webPath,directory]), keyword)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print("using default keyword")
        keyword = ''.join([r'\(|'.join(['eval','system','shell_exec','preg_replace','assert', 'exec', 'include','include_once','']), '|'.join(['_GET','_POST', '_REQUEST','mysql'])])
    elif len(sys.argv) == 3:
        keyword = sys.argv[2]
    else:
        print("usage: scan www_path [keyword]")
        exit(0)

    
    ScanVulnerabilities(sys.argv[1],keyword)



            










