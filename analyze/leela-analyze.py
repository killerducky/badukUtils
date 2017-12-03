#!/usr/bin/python

import datetime
import os
import sys
import subprocess
import time
import re


class Eval:
    def __init__(self, weights):
        self.weights  = weights
        self.playouts = 1000
        #leelaz_cmd = "leelaz -d -w ../networks/%s.txt -p %d --noponder -r 0" % (self.weights, self.playouts)
        leelaz_cmd = "/home/aolsen/projects/leela-zero-utils/leela-zero/src/leelaz -d -w ../networks/%s.txt -p %d --noponder -r 0" % (self.weights, self.playouts)
        #leelaz_cmd += " -n -m 30"   # noise, more random first 30 moves
        self.leela = subprocess.Popen(leelaz_cmd.split(), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
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
        self.fh = open("logs/evallog-%s-%d-%s-%d.txt" % (sgffile, movenum, self.weights, self.playouts), "w")
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
    

def main():
    #for weights in ("0k", "9k", "19k", "62k"):
    #for weights in ("137k", "human_best_v1"):
    for weights in ("292k",):
        eval = Eval(weights)
        #eval.evalposition("cap2.sgf", 612)
        #eval.evalposition("cap2.sgf", 1)
        #eval.evalposition("kill.sgf", 351)   # White T1, black kills
        #eval.evalposition("fill_2nd_eye.sgf", 412)
        #eval.evalposition("cap_to_connect_tail.sgf", 422)
        eval.playouts = 1000
        eval.evalposition("not_suicide.sgf", 430)   # White T1, black kills
        eval.playouts = 1600
        eval.evalposition("not_suicide.sgf", 430)   # White T1, black kills
        eval.playouts = 5000
        eval.evalposition("not_suicide.sgf", 430)   # White T1, black kills

if __name__ == "__main__": main()