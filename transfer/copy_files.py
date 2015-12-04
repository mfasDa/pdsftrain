#! /usr/bin/env python
#
#Usage: Run this script with the trainname as argument.
#For example: ./copy_trainrun.py EMCALTrain_20140912_43554_lhc13e_pass2 [OPTIONS]
#
#This script assumes that in this PATH_IN_ALIEN there are any number of folders (All 3 digit numbers e.g. "000","001",...)
#Every of these folders again cointains any number of folders (any format, e.g. "001" or "1471" or whatever)
#Every one of these folders then holds one instance of your rootfile of interest.
#The script creates the same folder structure on you machine and downloads every outputfile
#In the end it merges all of them into one file.
#
#@author: Markus Fasel (mfasel@lbl.gov)
#

from commands import getstatusoutput
from threading import Thread
from getopt import getopt
import os, sys, getpass

class TransferStream(Thread):

    def __init__(self, threadID):
        Thread.__init__(self)
        self.__threadID = threadID
        self.__filestotransfer = []

    def AddFile(self, alienfile, localfile):
        self.__filestotransfer.append([alienfile, localfile])

    def run(self):
        # Copy all files of my thread
        for myfile in self.__filestotransfer:
            outputdir = os.path.dirname(myfile[1])
            #print "Outputdir: %s" %(outputdir)
            if not os.path.exists(outputdir):
                os.makedirs(outputdir, 0755)
            self.__alien_copy_file("alien://%s" %(myfile[0]), myfile[1])

    def __alien_copy_file(self, source, target):
        os.system("alien_cp %s %s &> /dev/null" %( source, target))

def PrintInfo(rootfilename, path_in_alien):
    print " "
    print "------------------------------------------------------------------------"
    print "  remember to create an alien token first"
    print "  To run this in the background for example on pdsf or pcikf2:"
    print "  run the command 'screen' then run this script"
    print "  then do STG + a + d to detach from the session"
    print "  you can now log of ('exit') and the skript will keep running"
    print "  later come back by logging in and running the command 'screen -r'"
    print "------------------------------------------------------------------------"

def Usage():
    print "Usage:"
    print " "
    print " ./copy_files.py FILELIST [OPTIONS]"
    print " "
    print "Parameters: "
    print "  FILELIST: List of files to be copied"
    print "Options:"
    print "  -n: Number of parallel streams  [default: 5]"

def main():
    username = alien_whoami()

    if len(sys.argv > 1) and sys.argv[1] == "-h":
        Usage()
        sys.exit(1)

    nstream = 5
    filelist = sys.argv[1]

    try:
        opts, args = getopt(sys.argv[2:], "n:h")
    except GetoptError as e:
        print e
        Usage()
        sys.exit(2)

    for o,a in opts:
        if o = "-n":
            nstream = int(a)
        elif o == "-h":
            Usage()
            sys.exit(1)
        else:
            Usage()
            sys.exit(2)

    PrintInfo()

    # Start worker threads
    workers = []
    for i in range(0,nstream):
        mystream = TransferStream(i)
        workers.append(mystream)

    # distriubte files to the workers
    currentworker = 0
    for myfile in filelist:
        inputfile = myfile.split(" ")[0].lstrip().rstrip()
        outputfile = myfile.split(" ")[1].lstrip().rstrip()
        print "Adding file %s to be copied to %s" %(inputfile, outputfile)
        workers[currentworker].AddFile(inputfile, outputfile)
        # find next worker
        if currentworker == nstream-1:
            currentworker = 0
        else:
            currentworker += 1

    # start workers
    for myworker in workers:
        myworker.start()

    # stop all workers when finished
    for myworker in workers:
        myworker.join()

    # we are done
    print "%s %s" %(trainname, "copied from the grid and merged" if mergemode else "copied from the grid")

if __name__ == "__main__":
    main()
