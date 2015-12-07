#! /usr/bin/env python
'''
Created on 01.12.2015

@author: markusfasel
'''

import getopt, os, sys
import shutil

if __name__ == "__main__":
    sys.path.append(os.path.dirname(sys.argv[0]))

from train.steer.tools import GetWorkdir, SubmitBatch, FindList, GetLists
from train.steer.config import ConfigHandler
from train.steer.runAnalysis import runAnalysis

def Usage():
    print "Usage: ./run.py [MODE] [OPITONS]"
    print ""
    print "  Modes:"
    print "    train: Run the full train"
    print "    local: Run local tests"
    print "    merge: Merge output from a given train run"
    print " "
    print "  Options:"
    print "    -u|--user: Run for a special user"
    print "    -c|--config: Configuration"
    print "    -l|--list: Run on a special file list"
    print "    -s|--splitlevel: Number of files per job"
    print "    -n|--nchunk: Number of chunks"
    print "    -m|--minchunk: Minimum chunk (local running mode)"
    print "    -i|--inputdir: Inputdir (for merging)"
    print "    -f|--filename: Filename: (for merging)"
    print "    -d|--debug: Debug mode (printing debug messages)" 
    print "    -h|--help: Print help"
    

def main(argc, argv):
    
    modes = ["train", "batch", "local", "merge"]
    mode = argv[1]
    if not mode in modes:
        Usage()
        sys.exit(1)

    if mode == "local" and not "ALICE_PHYSICS" in os.environ.keys():
        print "For running in local mode please source [TRAIN_ROOT]/train/config/env before running"
        sys.exit(1)

    opt,arg = getopt.getopt(argv[2:], "u:c:l:s:n:m:i:f:hd", ["user=", "config=", "list=", "splitlevel=" , "nchunk=", "minchunk=", "inputdir=", "filename=", "help", "debug"]) 
    
    userdir = "all"
    filelist=""
    inputdir=""
    splitlevel=-1
    config = ""
    filename = ""
    nchunk = -1
    filemin = 0
    debug = False
    for o,a in opt:
        if o in ("-u", "--user"):
            userdir = str(a)
        elif o in ("-c", "--config"):
            config = str(a)
        elif o in ("-l", "--list"):
            filelist = str(a)
        elif o in ("-i", "--input"):
            inputdir = str(a)
        elif o in ("-f", "--filename"):
            filename = str(a)
        elif o in ("-s", "--splitlevel"):
            splitlevel = int(a)
        elif o in ("-n", "--nchunck"):
            nchunk = int(a)
        elif o in ("-m", "--minchunk"):
            filemin = int(a)
        elif o in ("-d", "--debug"):
            debug = True
        elif o in ("-h", "--help"):
            Usage()
            sys.exit(1)
    
    if not config:
        print "Config not specified. Please specify either PbPb, pPb, pp or the corresponding MC"
        sys.exit(1)
        
    ConfigHandler.LoadConfiguration(config)
    
    if splitlevel < 0:
        splitlevel = ConfigHandler.GetConfig().GetSplitLevel()

    if mode == "batch":
        # prepare job submission
        workdir = GetWorkdir(True if mode == "train" else False)
        if len(filelist): # run over one file
            if FindList(filelist):
                # create outputdir and copy train_root to that localtion
                os.makedirs(workdir, 0755)
                jobtrainroot = os.path.join(workdir, "TRAIN")
                shutil.copytree(ConfigHandler.GetTrainRoot(), jobtrainroot)
                tags = filelist.split("/")
                outputdir = workdir
                for tag in tags:
                    if tag == config:
                        continue
                    if ".txt" in tag:
                        outputdir = os.path.join(outputdir, tag.replace(".txt",""))
                        break
                    outputdir = os.path.join(outputdir, tag)
                os.makedirs(outputdir, 0755)
                # for debugging
                if debug:
                    print "Submitting batch job:"
                    print "============================="
                    print "Output location:             %s" %outputdir
                    print "Configuration:               %s" %ConfigHandler.GetConfig().GetName()
                    print "Users:                       %s" %userdir
                    print "Number of chunks:            %s" %nchunk
                    print "Split level:                 %s" %splitlevel
                    print "Using custom train root location %s" %jobtrainroot
                else:
                    SubmitBatch(outputdir, jobtrainroot, filelist, splitlevel, nchunk, userdir)
            else:
                print "List %s not found in your TRAIN_ROOT installation" %filelist
        else:
            "Batch mode - please specify an input list"
    elif mode == "train":
        os.makedirs(workdir, 0755)
        jobtrainroot = os.path.join(workdir, "TRAIN")
        shutil.copy(ConfigHandler.GetTrainRoot(), jobtrainroot)
            
        # run over all files
        filelists = GetLists(config)
        for myfilelist in filelists:
            tags = myfilelist.split("/")
            outputdir = workdir
            for tag in tags:
                if ".txt" in tag:
                    outputdir = os.path.join(outputdir, tag.replace(".txt",""))
                    break
                outputdir = os.path.join(outputdir, tag)
            os.makedirs(outputdir, 0755)
            SubmitBatch(outputdir, jobtrainroot, myfilelist, splitlevel, nchunk, userdir)
    elif mode == "merge":
        pass
    elif mode == "local":
        runAnalysis(userdir, config, filelist, filemin, filemin+nchunk)    
                

if __name__ == '__main__':
    ConfigHandler.SetTrainRoot(os.path.dirname(os.path.abspath(sys.argv[0])))
    main(len(sys.argv), sys.argv)
