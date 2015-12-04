#! /usr/bin/env python

import os, sys, shutil

SCRIPTBASE=None

class Worker():

        def __init__(self, id):
                self.__id = id
                self.__inputdir=os.path.join(SCRIPTBASE, "dtn%input" %id)
                self.__workdir=os.path.join(SCRIPTBASE, "dtn%input" %id)
                self.__nfiles = ReadNfiles()

        def GetNfiles(self):
                return self

        def ReadNfiles(self):
                return len(os.listdir(self.__inputdir)) + len(os.listdir(self.__workdir))

        def AcceptJob(self, job):
                shutil.copy(job, self.__inputdir)
                self.__nfiles. += 1

def main():
        SCRIPTBASE=os.path.abspath(sys.argv[0])
        inputdir=SCRIPTBASE

        workers = []
        nmax = 5
        for i in range (1, 3):
                workers.append(Worker(i))

        opt, arg = getopt.getopt(sys.argv[1:], "i:n", ["input=", "nmax="])
        for o, a, in opt:
                if o in ("-i", "--input"):
                        inputdir=str(a)
                elif o in ("-n", "--nmax"):
                        nmax = int(a)

        queued = os.listdir(inputdir)
        currentworker = 1
        navailable = 3
        for myq in queued:
                if navailable == 0:
                        # no resources available
                        break
                if workers[currentworker].GetNfiles() <= nmax:
                        workers[currentworker].AcceptJob()
                else:
                        navailable -= 1
                currentworker += 1
                if currentworker > 3:
                        currentworker = 1


if __name__ == "__main__":
        main()
