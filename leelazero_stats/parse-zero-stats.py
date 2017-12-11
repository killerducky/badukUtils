#!/usr/bin/python

# Format has changed over time:
# zero-stats-2017-11-17_01:38:03.740811.html
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br>A total of 33272 games have been submitted.<br>645 clients have submitted games.<br>
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br>968 clients have submitted games.<br>51172 total submitted games.<br><br>The 19K game network beats the 9k game network 63% of the time. A 38K network is training now.<br>
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br>979 total clients seen. (652 in past 24 hours, 186 in past hour.)<br>51990 total submitted games. (21256 in past 24 hours, 818 in past hour.)<br><br>The 19K game network beats the 9k game network 63% of the time. A 38K network is training now.<br>
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br><br>2017-11-21 We are now on 5 blocks x 64 filters, so the speed of the games will drop.<br>2017-11-20 <a href="https://github.com/gcp/leela-zero/releases">Leela Zero 0.6 + AutoGTP v4</a>.<br><br>707 clients in past 24 hours, 216 in past hour.<br>216395 total submitted games. (34392 in past 24 hours, 1338 in past hour.)<br><br>Autogtp will automatically download better networks once found.<br>Not each trained network will be a strength improvement over the prior one. Patience please. :)<br><br><a href="http://zero.sjeng.org/networks">Archive of past networks</a>.<br><a href="https://sjeng.org/zero/">Raw training data and SGF files</a>.<br><a href="https://docs.google.com/spreadsheets/d/e/2PACX-1vTsHu7T9vbfLsYOIANnUX9rHAYu7lQ4AlpVIvCfn60G7BxNZ0JH4ulfbADEedPVgwHxaH5MczdH853l/pubchart?oid=286613333&format=interactive">Strength graph</a>.<br><br><iframe width="987" height="638" seamless frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTsHu7T9vbfLsYOIANnUX9rHAYu7lQ4AlpVIvCfn60G7BxNZ0JH4ulfbADEedPVgwHxaH5MczdH853l/pubchart?oid=286613333&format=interactive"></iframe>
# Leela Zero is available from: <a href="https://github.com/gcp/leela-zero">Github</a>.<br><br>Autogtp will automatically download better networks once found.<br>Not each trained network will be a strength improvement over the prior one. Patience please. :)<br><br>2017-12-08 <a href="https://github.com/gcp/leela-zero/releases">Leela Zero 0.9 + AutoGTP v8</a>. <b>Update required.</b><br>2017-12-07 <a href="https://github.com/gcp/leela-zero/releases">Leela Zero 0.8 + AutoGTP v7</a>.<br>2017-12-07 <a href="https://github.com/gcp/leela-zero/releases">Leela Zero 0.7 + AutoGTP v6</a>.<br>2017-11-21 We are now on 5 blocks x 64 filters, so the speed of the games will drop.<br>2017-11-20 <a href="https://github.com/gcp/leela-zero/releases">Leela Zero 0.6 + AutoGTP v4</a>.<br><br>621 clients in past 24 hours, 253 in past hour.<br>956011 total selfplay games. (27307 in past 24 hours, 1270 in past hour.)<br>1210 network test matches in past 24 hours, 127 in past hour.<br><br><a href="https://sjeng.org/zero/">Raw training data and SGF files</a>.<br><a href="https://docs.google.com/spreadsheets/d/e/2PACX-1vTsHu7T9vbfLsYOIANnUX9rHAYu7lQ4AlpVIvCfn60G7BxNZ0JH4ulfbADEedPVgwHxaH5MczdH853l/pubchart?oid=286613333&format=interactive">Strength graph</a>.<br><br><iframe width="987" height="638" seamless frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTsHu7T9vbfLsYOIANnUX9rHAYu7lQ4AlpVIvCfn60G7BxNZ0JH4ulfbADEedPVgwHxaH5MczdH853l/pubchart?oid=286613333&format=interactive"></iframe><br>


import datetime
import os
import sys
import time
import glob
import re
import operator

dayBins = {}

files = glob.glob("zero-stats/*.html")
for filename in sorted(files):
    with open(filename) as fh:
        date = time = clients = clients_24h = clients_1h = games = games_24h = games_1h = None
        for line in fh:
            m = re.search("(\d+) clients in past 24 hours, (\d+) in past hour.*?(\d+) total submitted games. \((\d+) in past 24 hours, (\d+) in past hour.", line)
            if m: break
            m = re.search("(\d+) clients in past 24 hours, (\d+) in past hour.*?(\d+) total selfplay games. \((\d+) in past 24 hours, (\d+) in past hour.", line)
            if m: break
        if not m: 
            print "No match: %s" % filename
            continue
        (clients_24h, clients_1h, games, games_24h, games_1h) = m.groups()
        m = re.search("zero-stats-([\d-]+)_([\d:\.]+)\.html", filename)
        (day, time) = m.groups()
        stats = map(int, (1, clients_24h, clients_1h, games, games_24h, games_1h))
        if day in dayBins.keys():
            dayBins[day] = map(operator.add, dayBins[day], stats)
        else:
            dayBins[day] = stats
        #print day, dayBins[day]

for day, stats in dayBins.iteritems():
    count = stats[0]
    stats = stats[1:]
    stats = map(lambda x: x/count, stats)
    print ", ".join(map(str, [day+" 23:59:59", "NA"]+stats))
