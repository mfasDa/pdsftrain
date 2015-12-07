#! /usr/bin/env python

import os, sys, shutil, getopt

class Worker():

        def __init__(self, workerid, base):
                self.__workerid = int(workerid)
                self.__inputdir=os.path.join(base, "dtn%dinput" %self.__workerid)
                self.__workdir=os.path.join(base, "dtn%dwork" %self.__workerid)
                self.__nfiles = self.ReadNfiles()

        def GetNfiles(self):
                return self.__nfiles

        def ReadNfiles(self):
                return len(os.listdir(self.__inputdir)) + len(os.listdir(self.__workdir))

        def AcceptJob(self, job):
                shutil.move(job, self.__inputdir)
                self.__nfiles += 1

def main():
        base=os.path.dirname(os.path.abspath(sys.argv[0]))
        inputdir=base

        workers = []
        nmax = 5
        for i in range(1, 4):
                workers.append(Worker(i, base))

        opt, arg = getopt.getopt(sys.argv[1:], "i:n:", ["input=", "nmax="])
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
                if workers[currentworker-1].GetNfiles() <= nmax:
                        workers[currentworker-1].AcceptJob(os.path.join(inputdir, myq))
                else:
                        navailable -= 1
                currentworker += 1
                if currentworker > 3:
                        currentworker = 1


if __name__ == "__main__":
        main()
