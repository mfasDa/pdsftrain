#! /usr/bin/env python

import os, sys, shutil

if __name__ == "__main__":
        datain = os.listdir(sys.argv[2])
        filelists = os.listdir(sys.argv[1])
        data=[]
        for d in datain:
                data.append(int(d))

        for l in filelists:
                mytest = l
                test = int(mytest.replace("files_", "").replace("_muon_calo_pass1.txt", ""))
                if l in data:
                        continue
                shutil.copy(os.path.join(sys.argv[1], l), os.path.join(os.getcwd(), l))
