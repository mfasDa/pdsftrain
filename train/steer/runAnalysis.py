#! /usr/bin/env python
'''
Created on 04.12.2015

@author: markusfasel
'''
import os, sys
import json
import ROOT

if __name__ == "__main__":
    sys.path.append(os.environ["TRAIN_ROOT"])

from train.steer.config import ConfigHandler
    
class UserConfig(object):
    
    def __init__(self):
        self.__name = ""
        self.__macro = ""
        self.__status = ""
        
    def Initialize(self, node):
        for k,v in node.iteritems():
            if k == "NAME":
                self.__name = v
            elif k == "MACRO":
                self.__macro = v 
            elif k == "STATUS":
                self.__status = v
    
    def SetName(self, name):
        self.__name = name
    
    def SetMacro(self, macro):
        self.__macro = macro
    
    def SetStatus(self, status):
        self.__status = status
        
    def GetName(self):
        return self.__name
    
    def GetMacro(self):
        return self.__macro
    
    def GetStatus(self):
        return self.__status
    
def ReadJSON(filename):
    result = ""
    reader = open(filename, "r")
    for line in reader:
        myline = line.replace("\n", "").lstrip().rstrip()
        result += myline
    reader.close()
    return result

def ProcessUser(username):
    userdir = os.path.join(ConfigHandler.GetTrainRoot(), username)
    userconfig = os.path.join(userdir, "config.json")
    configs = json.loads(ReadJSON(userconfig))
    for myconf, tasks in configs.iteritems():
        if myconf == ConfigHandler.GetConfig().GetName():
            for task in tasks:
                taskconfig = UserConfig()
                taskconfig.Initialize(task)
                if taskconfig.GetStatus().upper() == "ACTIVE":
                    if "$ALICE_ROOT" in taskconfig.GetMacro() or "$ALICE_PHYSICS" in taskconfig.GetMacro():
                        # Load macro from AliRoot or AliPhysics
                        ROOT.gROOT.Macro(taskconfig.GetMacro())
                    else:
                        # Load macro from user directory
                        ROOT.gROOT.Macro("%s/%s/%s" %(ConfigHandler.GetTrainRoot(), username, taskconfig.GetMacro()))

def CreateChain(filelist, treename):
    chain = ROOT.TChain(treename, "")
    for myfile in filelist:
        chain.AddFile(myfile)
    return chain

def CreateAnalysisManager():
    mgr = ROOT.AliAnalysisManager("MGR")
    mgr.SetCommonFileName("AnalysisResults.root")
    return mgr

def CreateHandlers():
    for handler in ConfigHandler.GetConfig().GetHandlers():
        ROOT.gROOT.Macro(handler)

def ReadFileList(inputfile, mymin, mymax):
    print "Reading file %s from %s to %s" %(inputfile, mymin, mymax)
    result = []
    reader = open(inputfile)
    counter = 0
    for line in reader:
        newline = line.replace("\n", "").lstrip().rstrip()
        if not len(newline):
            continue
        if mymin > -1 and counter < mymin:
            counter += 1
            continue
        if mymax > 0 and counter >= mymax:
            break
        print "Accepted %s" %(newline)
        result.append(newline)
        counter += 1
    reader.close()
    return result

def runAnalysis(user, config, filelist, filemin, filemax):
    # Load additional libraries
    ROOT.gROOT.Macro("%s/train/macros/LoadLibs.C" %ConfigHandler.GetTrainRoot())
    
    mgr = CreateAnalysisManager()
    CreateHandlers()
    
    ProcessUser("basics")
    if user != "all":
        print "Adding user %s" %user
        ProcessUser(user)
    else:
        userreader = open(os.path.join(ConfigHandler.GetTrainRoot(), "config", "user"), "R")
        for tmpuser in userreader:
            myuser = tmpuser.replace("\n", "").lstrip().rstrip()
            if(myuser[0] == "#"):
                continue
            print "Adding user %s" %myuser
            ProcessUser(myuser)
        userreader.close()
        
    files = ReadFileList(os.path.join(ConfigHandler.GetTrainRoot(), "train", "filelists", filelist), filemin, filemax)
    if not len(files):
        print "No files found to analyze"
        return
    if mgr.InitAnalysis():
        mgr.PrintStatus()
        mgr.StartAnalysis("local", CreateChain(files, ConfigHandler.GetConfig().GetTreename()))

if __name__ == "__main__":
    ConfigHandler.SetTrainRoot(os.environ["TRAIN_ROOT"])
    ConfigHandler.LoadConfiguration(sys.argv[2])
    runAnalysis(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
