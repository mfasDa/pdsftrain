#! /usr/bin/env python

import os, sys, shutil

if __name__ == "__main__":
        datain = os.listdir(sys.argv[2])
        filelists = os.listdir(sys.argv[1])
        data=[]
        for d in datain:
                mydat = int(d)
                print "Run %d in process or completed" %mydat
                data.append(mydat)

        for l in filelists:
                mytest = l
                test = int(mytest.replace("files_", "").replace("_muon_calo_pass1.txt", ""))
                if test in data:
                        continue
                print "Adding data %s" %l
                shutil.copy(os.path.join(sys.argv[1], l), os.path.join(os.getcwd(), l))
