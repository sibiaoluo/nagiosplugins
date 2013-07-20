#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys

OK=0
WARNING=1
CRICITCAL=2
UNKNOWN=3

def opt():
    parser = OptionParser(usage="usage: %prog -w WARNING -c CRITICAL")
    parser.add_option("-c", default='100M', action="store", type="string", dest="critical")
    parser.add_option("-w", default='200M', action="store", type="string", dest="warning")
    return parser.parse_args()


def convertUnit(s):
    unit = {'g':2**30,'m':2**20,'k':2**10,'t':2**40,'b':1}
    s = s.lower()
    lastchar = s[-1]
    num = int(s[:-1])
    if lastchar in unit:
        return num*unit[lastchar]
    else:
        return int(s)


def getFreeMemory():
    with open('/proc/meminfo', 'r') as fd:
        for line in fd.readlines():
            if line.startswith('MemFree'):
                 k, v, u = line.split()
                 return int(v)*1024
                       
def main():
    opts, args = opt()
    w = convertUnit(opts.warning)
    c = convertUnit(opts.critical)
    free_mem = getFreeMemory()
    if w >= free_mem > c:
        print "WARNING, free:%s MB" % free_mem
        sys.exit(WARNING)
    elif free_mem <= c:
        print "CRICITCAL, free:%s MB" % free_mem
        sys.exit(CRICITCAL)
    elif free_mem > w:
        print "OK, free:%s MB" % free_mem
        sys.exit(OK)
    else:
        print "UNKNOWN, free:%s MB" % free_mem
        sys.exit(UNKNOWN)

if __name__=="__main__":
    main()                      
