'''
Created on 01.12.2015

@author: markusfasel
'''

import os, time
from train.steer.config import ConfigHandler
from train.steer.submit import Submitter

def GetTag():
    config = ConfigHandler.GetConfig()
    return "%s.%s/%s" %(config.GetVersion(), config.GetName(), time.strftime("%y%m%d_%H%M%S", time.localtime()));

def FindList(listname):
    currentdir = ConfigHandler.GetTrainRoot()
    files = FindFiles(os.path.join(currentdir, "train", "filelists"))
    hasfound = False
    for f in files:
        if listname in f:
            hasfound = True
            break
    return hasfound

def FindFiles(inputdir):
    result = []
    for mypath, mydirs, myfiles in os.walk(inputdir):
        for f in myfiles:
            result.append(os.path.join(os.path.abspath(mypath), f))
    return result

def GetLists(mode):
    filelists = []
    trainroot = ConfigHandler.GetTrainRoot()
    currentdir = os.path.join(trainroot, mode)
    found = FindFiles(currentdir)
    # strip away train root
    for f in found:
        test = f.replace(trainroot, "")
        test = test.rstrip().lstrip()
        if test[0] == "/":
            filelists.append(test)
    return filelists
    
def SubmitBatch(outputdir, jobtrainroot, filelist, splitlevel, chunks, user):
    submitter = Submitter(filelist, jobtrainroot, outputdir, splitlevel)
    if chunks >= 0:
        submitter.SetNchunk(chunks)
    submitter.SetUser(user)
    submitter.Submit()
    return submitter.GetJobID()
    
def SubmitMergeJob(jobtrainroot, inputdir, jobid):
    jobbase = jobtrainroot
    jobbase.replace("TRAIN", "")
    jobbase.rstrip("/")
    tmpdir = inputdir.replace(jobbase)
    tmpdir.lstrip("/")
    outputdir = "%s/merge/%s" %(jobbase, tmpdir)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir, 0755)
    cmd = "qsub -l \"projectio=1,h_vmem=4G\" -hold_jid %d -j y -o %s/merge.log %s/train/steer/mergescript.sh %s %s %s %s" %(jobid, outputdir, jobtrainroot, jobtrainroot, inputdir, outputdir, "AnalysisResults.root") 
    os.system(cmd)
        
def GetWorkdir(doGlobal):
    return os.path.join(ConfigHandler.GetConfig().GetTrainOutputPath(doGlobal), GetTag())
