#!/usr/bin/python

import datetime
import os
import sys
import subprocess
import time
import re

class Eval:
    def __init__(self, label, leelaz_path, weights):
        self.label = label
        self.leelaz_path = leelaz_path
        self.weights  = weights
        self.playouts = 1000
        self.leelaz_cmd = "%s -d -w /home/aolsen/networks/%s.txt -p %d --noponder -r 0" % (self.leelaz_path, self.weights, self.playouts)
        #self.leelaz_cmd += " -n -m 30"   # noise, more random first 30 moves
        self.leelaz_cmd += " -t 1"   # single thread
        self.leela = subprocess.Popen(self.leelaz_cmd.split(), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        while 1:
            self.leela.stdout.flush()
            line = self.leela.stdout.readline()
            print line,
            if re.search("^White time", line): break

    def colortomove(self, movenum):
        if movenum%2: return "b"
        return "w"

    def sendcmd(self, cmd):
        self.leela.stdin.write(cmd+"\n")
        self.log("cmd: %s\n" % (cmd))
        self.cmds.append(cmd)

    def log(self, line):
        self.fh.write(line)
        print line,

    def evalposition(self, sgffile, movenum):
        self.cmds = []
        self.fh = open("logs/evallog_%s_%d_%s_%s_%d.txt" % (sgffile, movenum, self.label, self.weights, self.playouts), "w")
        self.log("leelaz_cmd=%s\n" % (self.leelaz_cmd))
        self.log("evalposition %s %d\n" % (sgffile, movenum))
        self.sendcmd("loadsgf sgfs/%s %d" % (sgffile, movenum))
        self.sendcmd("heatmap")
        self.sendcmd("genmove %s" % (self.colortomove(movenum)))
        self.sendcmd("heatmap")
        self.sendcmd("dump_training w test_training")
        for cmd in self.cmds:
            self.log("\n\ncmd=%s\n" % (cmd))
            while 1:
                self.leela.stdout.flush()
                line = self.leela.stdout.readline()
                if re.search("^Leela: ", line):
                    line = re.sub("^Leela: ", "Leela:\n", line)
                self.log(line)
                if re.search("^White time", line): break
        self.fh.close()
        self.leela.kill()
    

def main():
    leelaz_paths = {}
    leelaz_paths["default"] = "/home/aolsen/projects/leela-zero-utils/leela-zero/src/leelaz"
    leelaz_paths["cpuct"]   = "/home/aolsen/projects/test_first_move_and_puct/leela-zero/src/leelaz"
    positions = []
    positions.append(("cap2.sgf", 1))
    #positions.append(("cap2.sgf", 612)
    #positions.append(("not_suicide.sgf", 430))   # White T1, black kills
    #positions.append(("kill.sgf", 351))   # White T1, black kills
    #positions.append(("fill_2nd_eye.sgf", 412))
    #positions.append(("cap_to_connect_tail.sgf", 422))

    #for weights in ("0k", "9k", "19k", "62k"):
    #for weights in ("137k", "human_best_v1"):
    for label in ("default", "cpuct"):
        for weights in ("292k",):
            #for playouts in (625, 1000, 1600):
            for playouts in (1000,):
                for position in (positions):
                    eval = Eval(label, leelaz_paths[label], weights)
                    eval.playouts = playouts
                    eval.evalposition(position[0], position[1])

if __name__ == "__main__": main()
