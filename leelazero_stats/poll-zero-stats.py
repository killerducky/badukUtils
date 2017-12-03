#!/usr/bin/python

import datetime
import os
import sys
import time

DELAY = 3600
#DELAY = 10
URL   = "http://zero.sjeng.org"

def logsys(cmd):
    print cmd
    os.system(cmd)

while (1):
    ts = str(datetime.datetime.utcnow()).replace(" ", "_")
    logsys("wget -q %s" % (URL))
    logsys("mv index.html zero-stats/zero-stats-%s.html" % (ts))
    print "sleep %d seconds" % (DELAY)
    time.sleep(DELAY)

