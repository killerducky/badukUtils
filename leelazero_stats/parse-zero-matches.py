#!/usr/bin/python

import datetime
import os
import sys
import time
import glob
import re
import urllib
from bs4 import BeautifulSoup

best_networks = {}

fh = urllib.urlopen("http://zero-test.sjeng.org")
#fh = open("index.html")
soup = BeautifulSoup(fh.read(), "html.parser")
for table in soup.find_all(lambda tag: tag.name == "table" and "networks-table" in tag["class"]):
    for row in table.find_all("tr"):
        data = row.find_all("td")
        if not data: continue
        date, network, games, prior_games = data
        games = int(games.string)
        prior_games = int(prior_games.string)
        best_networks[network.string] = {}
        best_networks[network.string]["prior_games"] = prior_games
        best_networks[network.string]["date"] = date.string

for table in soup.find_all(lambda tag: tag.name == "table" and "matches-table" in tag["class"]):
    for row in table.find_all("tr"):
        data = row.find_all("td")
        if not data: continue
        date, networks, record, games, sprt = data
        next_net, prev_net = networks.find_all()
        wins, losses = re.search("(\d+) : (\d+)", record.contents[0]).groups()
        wins = int(wins)
        losses = int(losses)
        if next_net.string in best_networks:
            best_networks[next_net.string]["prev_net"] = prev_net.string
            best_networks[next_net.string]["wins"] = wins
            best_networks[next_net.string]["losses"] = losses

for k in sorted(best_networks.keys(), key=lambda x: best_networks[x]["prior_games"]):
    v = best_networks[k]
    if "wins" in v:
        print ", ".join(map(str, [k, v["prev_net"], v["date"], v["prior_games"], v["wins"], v["losses"]]))
            


