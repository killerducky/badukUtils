#!/usr/bin/python

import datetime
import os
import sys
import subprocess
import time
import re


class Eval:
    def __init__(self, label, leelaz_path, weights, playouts_arg, playouts, sgffile, movenum, args = ""):
        weights_path = "/home/aolsen/networks"
        self.label = label
        self.leelaz_path = leelaz_path
        self.weights  = weights
        self.playouts_arg = playouts_arg
        self.playouts = playouts
        self.args = args
        self.sgffile = sgffile
        self.movenum = movenum

        self.logfile = "logs/%s-%s-%d-%s-%d.log" % (label, playouts_arg, playouts, sgffile, movenum)
        if os.path.isfile(self.logfile):
            os.remove(self.logfile)
        self.pcmd = "%s -g -d -t 1 -r 1 -w %s/%s -%s %d --noponder %s -l %s" % (
            self.leelaz_path, weights_path, self.weights, self.playouts_arg, self.playouts, self.args, self.logfile)

    def colortomove(self, movenum):
        if movenum%2: return "b"
        return "w"

    def evalposition(self, sgffile, movenum):
        print(self.pcmd.split())
        #self.leela = subprocess.Popen(self.pcmd.split(), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        self.leela = subprocess.Popen(self.pcmd.split(), stdin = subprocess.PIPE)
        self.leela.stdin.write("kgs-time_settings byoyomi 0 1 0\n")
        self.leela.stdin.write("loadsgf sgfs/%s %d\n" % (sgffile, movenum))
        self.leela.stdin.write("heatmap\n")
        self.leela.stdin.write("genmove %s\n" % (self.colortomove(movenum)))
        self.leela.stdin.write("heatmap\n")
        self.leela.stdin.write("dump_training w test_training\n")

    def quit(self):
        self.leela.stdin.write("quit\n")
        self.leela.wait()


def main():
    leelaz_paths = {}
    #leelaz_paths["default"] = "/home/aolsen/projects/lz-master/leela-zero/src/leelaz"
    leelaz_paths["next"]   = "/home/aolsen/projects/lz-next/leela-zero/build/leelaz"
    positions = []
    #positions.append(("opening.sgf", 1))
    #positions.append(("early_pass.sgf", 4))
    #positions.append(("cap2.sgf", 612))
    #positions.append(("not_suicide.sgf", 430))   # White T1, black kills
    positions.append(("kill.sgf", 351))   # White T1, black kills
    #positions.append(("fill_2nd_eye.sgf", 412))
    #positions.append(("cap_to_connect_tail.sgf", 422))
    #positions.append(("test_suicide.sgf", 282))  # black dead group many liberties
    #positions.append(("test_suicide.sgf", 304))  # black dead group 2 liberties
    #positions.append(("test_suicide.sgf", 306))  # black dead group 1 liberties
    #positions.append(("test_suicide.sgf", 326))  # no dame left
    #positions.append(("test_suicide.sgf", 342))  # white only 2 eyes
    #positions.append(("test_suicide.sgf", 343))  # white only 1 eye, black to kill
    #positions.append(("test_suicide2.sgf", 256))  # black dead group many liberties
    #positions.append(("test_suicide2.sgf", 274))  # black dead group 2 liberties
    #positions.append(("test_suicide2.sgf", 276))  # black dead group 1 liberties
    #positions.append(("test_suicide2.sgf", 316))  # white only 2 eyes
    #positions.append(("test_suicide2.sgf", 317))  # white only 1 eye, black to kill
    positions.append(("test_suicide2.sgf", 317))  # white only 1 eye, black to kill
    for lz in ["next"]:
        #for weights in ("0k", "9k", "19k", "62k", "292k"):
        #for weights in ("137k", "human_best_v1"):
        for weights in ["890k.txt"]:
            #for playouts in [50, 100, 360, 500, 625, 1000, 1600, 5000, 10000]:
            for visits in [1600]:
                for (position, movenum) in (positions):
                    eval = Eval(lz, leelaz_paths[lz], weights, "v", visits, position, movenum)
                    eval.evalposition(position, movenum)
                    eval.quit()

if __name__ == "__main__": main()
