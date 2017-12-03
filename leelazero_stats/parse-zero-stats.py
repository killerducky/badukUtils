#!/usr/bin/python

# zero-stats-2017-11-17_01:38:03.740811.html
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br>A total of 33272 games have been submitted.<br>645 clients have submitted games.<br>
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br>968 clients have submitted games.<br>51172 total submitted games.<br><br>The 19K game network beats the 9k game network 63% of the time. A 38K network is training now.<br>
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br>979 total clients seen. (652 in past 24 hours, 186 in past hour.)<br>51990 total submitted games. (21256 in past 24 hours, 818 in past hour.)<br><br>The 19K game network beats the 9k game network 63% of the time. A 38K network is training now.<br>


import datetime
import os
import sys
import time
import glob
import re

def logsys(cmd):
    print cmd
    os.system(cmd)

files = glob.glob("zero-stats/*.html")
for filename in sorted(files):
    with open(filename) as fh:
        date = time = clients = clients_24h = clients_1h = games = games_24h = games_1h = None
        line = fh.readline()
        #print line
        m = re.search("A total of (\d+) games.*?(\d+) clients", line)
        if m: (games, clients) = m.groups()
        else:
            m = re.search("(\d+) clients.*?(\d+) total submitted games", line)
            if m: (clients, games) = m.groups()
            else:
                m = re.search("(\d+) total clients seen. \((\d+) in past 24 hours, (\d+) in past hour.\).*?(\d+) total submitted games. \((\d+) in past 24 hours, (\d+) in past hour.", line)
                (clients, clients_24h, clients_1h, games, games_24h, games_1h) = m.groups()
        m = re.search("zero-stats-(.*)\.html", filename)
        (datetime,) = m.groups()
        datetime = datetime.replace("_", " ")
        print ", ".join(map(str, (datetime, clients, clients_24h, clients_1h, games, games_24h, games_1h)))

