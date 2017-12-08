#!/usr/bin/python

# Format has changed over time:
# zero-stats-2017-11-17_01:38:03.740811.html
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br>A total of 33272 games have been submitted.<br>645 clients have submitted games.<br>
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br>968 clients have submitted games.<br>51172 total submitted games.<br><br>The 19K game network beats the 9k game network 63% of the time. A 38K network is training now.<br>
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br>979 total clients seen. (652 in past 24 hours, 186 in past hour.)<br>51990 total submitted games. (21256 in past 24 hours, 818 in past hour.)<br><br>The 19K game network beats the 9k game network 63% of the time. A 38K network is training now.<br>
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br><br>2017-11-21 We are now on 5 blocks x 64 filters, so the speed of the games will drop.<br>2017-11-20 <a href="https://github.com/gcp/leela-zero/releases">Leela Zero 0.6 + AutoGTP v4</a>.<br><br>707 clients in past 24 hours, 216 in past hour.<br>216395 total submitted games. (34392 in past 24 hours, 1338 in past hour.)<br><br>Autogtp will automatically download better networks once found.<br>Not each trained network will be a strength improvement over the prior one. Patience please. :)<br><br><a href="http://zero.sjeng.org/networks">Archive of past networks</a>.<br><a href="https://sjeng.org/zero/">Raw training data and SGF files</a>.<br><a href="https://docs.google.com/spreadsheets/d/e/2PACX-1vTsHu7T9vbfLsYOIANnUX9rHAYu7lQ4AlpVIvCfn60G7BxNZ0JH4ulfbADEedPVgwHxaH5MczdH853l/pubchart?oid=286613333&format=interactive">Strength graph</a>.<br><br><iframe width="987" height="638" seamless frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTsHu7T9vbfLsYOIANnUX9rHAYu7lQ4AlpVIvCfn60G7BxNZ0JH4ulfbADEedPVgwHxaH5MczdH853l/pubchart?oid=286613333&format=interactive"></iframe>


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
        #m = re.search("A total of (\d+) games.*?(\d+) clients", line)
        #m = re.search("(\d+) clients.*?(\d+) total submitted games", line)
        #m = re.search("(\d+) total clients seen. \((\d+) in past 24 hours, (\d+) in past hour.\).*?(\d+) total submitted games. \((\d+) in past 24 hours, (\d+) in past hour.", line)
        #m = re.search("(\d+) total clients seen. \((\d+) in past 24 hours, (\d+) in past hour.\).*?(\d+) total submitted games. \((\d+) in past 24 hours, (\d+) in past hour.", line)
        m = re.search("(\d+) clients in past 24 hours, (\d+) in past hour.*?(\d+) total submitted games. \((\d+) in past 24 hours, (\d+) in past hour.", line)
        if not m: 
            print "No match: %s" % filename
            continue
        (clients_24h, clients_1h, games, games_24h, games_1h) = m.groups()
        m = re.search("zero-stats-(.*)\.html", filename)
        (datetime,) = m.groups()
        datetime = datetime.replace("_", " ")
        print ", ".join(map(str, (datetime, "NA", clients_24h, clients_1h, games, games_24h, games_1h)))

