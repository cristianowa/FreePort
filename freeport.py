#!/usr/bin/python
from commands import getoutput as cmd
import re
import os
import sys
import tempfile
def getpidport(port):
    output = cmd("netstat -lnp | grep tcp |  grep 0.0.0.0:" + port)
    print output
    return re.findall("LISTEN *([0-9]*)/", output)[0]

def findfp(pid, port):
    output = cmd("lsof -P -np "+ pid + " | grep IP").split("\n")
    fps = []
    for line in output:
        fps.append(line.split(" ")[7])
    return fps

def closefp(fp):
    f = tempfile.mktemp() + ".gdb"
    x = open(f,"w")
    x.write("call close(" + fp + ")\nquit\n\n")
    x.close()
    print f
    print cmd("cat " + f)
    print cmd("gdb -p " + pid + " --command=" + f + " --batch")
    
if len(sys.argv) < 2:
    print "Usage:"
    print " frees a port from it's usurper"
    print sys.argv[0] + " <port>"
port = sys.argv[1]
pid = getpidport(sys.argv[1])
print pid
fps = findfp(pid, port)
print fps
for fp in fps:
        closefp(fp)

