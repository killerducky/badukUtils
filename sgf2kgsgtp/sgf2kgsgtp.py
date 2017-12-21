#!/usr/bin/env python3

# cd /home/aolsen/projects/badukUtils/sgf2kgsgtp
# ./sgf2kgsgtp.py LeelaZeroA.cfg /home/aolsen/projects/leela-zero-utils/leela-zero/autogtp/save
# ./sgf2kgsgtp.py LeelaZeroB.cfg /home/aolsen/projects/leela-zero-utils/leela-zero/autogtp/save

import subprocess
import re
import sys
import glob
import os
import time

class KgsGtp:
    def __init__(self, cfgfile, auto_sgfs_dir):
        self.cfgfile = cfgfile
        self.auto_sgfs_dir = auto_sgfs_dir      # autogtp output dir
        self.queued_sgfs_dir = "queued_sgfs"
        self.relayed_sgfs_dir = "relayed_sgfs"
        self.move_sleep_early = 4.0
        self.move_sleep_late  = 1.0
        self.final_status_list_sleep = 20.0
        self.kgs_game_over_sleep = 20.0
        self.boardsize = 19  # Could get this from GTP but this is easier
        self.maxmoves  = self.boardsize*self.boardsize*2
        self.responses = {}
        self.responses["list_commands"] = [
            "protocol_version",
            "name",
            "version",
            "quit",
            "known_command",
            "list_commands",
            "boardsize",
            "clear_board",
            "komi",
            "play",
            "genmove",
            "showboard",
            "undo",
            "final_score",
            "final_status_list",
            "time_settings",
            "time_left",
            "fixed_handicap",
            "place_free_handicap",
            "set_free_handicap",
            "loadsgf",
            "printsgf",
            "kgs-genmove_cleanup",
            "kgs-time_settings",
            "kgs-game_over",
            #"kgs-chat",
            "heatmap"
        ]
        # computer-go mailing list said kgs-chat is broken.
        #if (self.cfgfile == "LeelaZeroA.cfg"):
        #    self.responses["list_commands"].append("kgs-chat")
        if (self.cfgfile == "LeelaZeroA.cfg"):
            self.responses["name"] = "LeelaZero -- This robot relays Leela Zero self play games to KGS. See my info or http://zero.sjeng.org"
        else:
            self.responses["name"] = ""
        self.responses["version"] = ""
        # Throw these away
        self.responses["kgs-time_settings"] = ""
        self.responses["clear_board"] = ""
        self.responses["komi"] = ""
        self.responses["play"] = ""
        self.responses["time_left"] = ""
        self.moves = []
        self.movenum = 0
        self.kgsGtpCmd = "java -jar ../../kgsGtp-3.5.22/kgsGtp.jar %s" % (self.cfgfile)
        self.winner = None
        self.score = None

    def openKgsGtpProc(self):
        self.kgsGtpProc = subprocess.Popen(self.kgsGtpCmd.split(), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines=True, bufsize=1)

    def send2kgsGtp(self, s):
        print(">%s" % (s), end="")
        self.kgsGtpProc.stdin.write(s)

    def readKgsGtp(self):
        s = self.kgsGtpProc.stdout.readline()
        print("<%s" % (s), end="")
        return s

    def getNextMove(self, mycolor):
        self.moveSleep()
        self.mycolor = mycolor
        print("getNextMove %s self.movenum=%d len(self.moves)=%d" % (self.mycolor, self.movenum, len(self.moves)))
        if self.movenum >= len(self.moves):
            print("out of moves, resign. self.winner=%s self.score=%s self.mycolor=%s\n" % (self.winner, self.score, self.mycolor))
            return "resign"
        (color, move) = self.moves[self.movenum]
        self.movenum += 1
        if color != self.mycolor:
            print("opponent should have played %s %s" % (color, move))
            if self.movenum >= len(self.moves):
                print("out of moves, resign. self.winner=%s self.score=%s self.mycolor=%s\n" % (self.winner, self.score, self.mycolor))
                return "resign"
            (color, move) = self.moves[self.movenum]
            self.movenum += 1
        return move

    def move_and_preserve_ts(self, olddir, newdir, filename):
        oldfullname = "%s/%s" % (olddir, filename)
        newfullname = "%s/%s" % (newdir, filename)
        stat = os.stat(oldfullname)
        print("move %s to %s" % (oldfullname, newfullname))
        os.rename(oldfullname, newfullname)
        os.utime(newfullname, (stat.st_atime, stat.st_mtime))

    def game_over(self):
        if self.mycolor == "B":
            self.move_and_preserve_ts(self.queued_sgfs_dir, self.relayed_sgfs_dir, self.filename)
            # Having a separate queue directory from autogtp prevents Black and White from picking a different game
            for filename in glob.iglob("%s/*.sgf" % (self.auto_sgfs_dir)):
                filename = re.sub(".*/", "", filename)  # strip path and use just base filename
                self.move_and_preserve_ts(self.auto_sgfs_dir, self.queued_sgfs_dir, filename)
        self.moves = []
        self.movenum = 0
        time.sleep(self.kgs_game_over_sleep)

    def moveSleep(self):
        # Start speeding up halfway through the max = 361 moves
        scale = 1.0 * (self.movenum - (self.maxmoves/2.0 - self.boardsize)) / self.boardsize
        scale = min(1.0, scale)
        scale = max(0.0, scale)
        t = (1.0-scale)*self.move_sleep_early + scale*self.move_sleep_late
        print("movenum=%d sleep=%0.1f" % (self.movenum, t))
        time.sleep(t)

    def kgsGtpLoop(self):
        while 1:
            cmd = self.readKgsGtp()
            cmdarray = cmd.split()
            if cmdarray[0] == "genmove":
                move = self.getNextMove(cmdarray[1].upper())
                self.send2kgsGtp("= %s\n" % (move))
            elif cmdarray[0] == "boardsize":
                if len(self.moves)==0:
                    self.parseNextSgf()
                    continue
                self.send2kgsGtp("=\n")
            elif cmdarray[0] == "final_status_list":
                time.sleep(self.final_status_list_sleep)
                self.send2kgsGtp("=\n")
            elif cmdarray[0] == "kgs-game_over":
                self.game_over()
                self.send2kgsGtp("=\n")
            elif cmdarray[0] == "kgs-chat":
                self.send2kgsGtp("= %s\n" % (self.responses["version"]))
            elif cmdarray[0] in self.responses.keys():
                response = self.responses[cmdarray[0]]
                self.send2kgsGtp("= ")
                if isinstance(response, tuple) or isinstance(response, list):
                    for line in response:
                        self.send2kgsGtp("%s\n" % line)
                else:
                    self.send2kgsGtp("%s\n" % response)
            self.send2kgsGtp("\n")

    # Convert from sgf letter+letter style to human/gtp letter+number style
    # Also looks like we need to swap the order
    def sgf2human(self, sgf):
        if sgf == "tt": return "pass"
        letter = sgf[0]
        if letter >= "i": letter = chr(ord(letter) + 1)   # skip "i"
        letter.upper()  # I think gtp usually uses uppercase?
        number = ord("s") - ord(sgf[1]) + 1
        return "%s%d" % (letter, number)

    def parseNextSgf(self):
        # Pick the most recent game from queue
        filename = max(glob.iglob("%s/*.sgf" % (self.queued_sgfs_dir)), key=os.path.getmtime)
        filename = re.sub(".*/", "", filename)  # strip path and use just base filename
        print("picked %s" % (filename))
        self.parseSgf(filename)
        self.kgsGtpProc.kill()
        self.kgsGtpProc = subprocess.Popen(self.kgsGtpCmd.split(), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines=True, bufsize=1)

    #
    # Example sgf:
    #(;GM[1]FF[4]RU[Chinese]DT[2017-11-22]SZ[19]KM[7.5]PB[Leela Zero 0.6 1ac2638d]PW[Human]RE[B+9.5]
    #
    #;B[po];W[nb];B[hs];W[jf];B[nq];W[af];B[nl];W[rn];B[ap];W[sr]
    # <snip>
    #;B[jn];W[df];B[jp];W[aq];B[ss];W[tt];B[tt])
    #
    # Example header with resign:
    #(;GM[1]FF[4]RU[Chinese]DT[2017-12-05]SZ[19]KM[7.5]PB[Leela Zero 0.6 /home/ao]PW[Human]RE[B+Resign]
    #
    def parseSgf(self, filename):
        self.moves = []
        self.filename = filename
        fh = open("%s/%s" % (self.queued_sgfs_dir, self.filename), "r")
        line = fh.readline()
        m = re.search("PB\[Leela Zero (.*?)\]PW\[Leela Zero (.*?)\].*RE\[(.)\+(\S+)?\]", line)
        (pw, pb, self.winner, self.score) = m.groups()
        if (self.cfgfile == "LeelaZeroA.cfg"):
            if pw == pb:
                self.responses["version"] = pw
            else:
                self.responses["version"] = "Test Match White: %s, Black %s" % (pw, pb)
        for line in fh:
            for move in line.split(";"):
                m = re.search("([BW])\[(..)\]", move)
                if not m: continue
                (color, move) = m.groups()
                move = self.sgf2human(move)
                self.moves.append((color, move))
                print("%s %s " % (color, move), end="")
        fh.close()

def main():
    cfgfile       = sys.argv[1]
    auto_sgfs_dir = sys.argv[2]
    kgsGtp = KgsGtp(cfgfile, auto_sgfs_dir)
    kgsGtp.openKgsGtpProc()
    kgsGtp.kgsGtpLoop()

if __name__ == "__main__": main()

