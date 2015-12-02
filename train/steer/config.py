'''
Created on 01.12.2015

@author: markusfasel
'''

import os, getpass, json

gConfig = None
gMode = ""
gTrainRoot = ""

class ConfigHandler(object):
    
    @staticmethod
    def LoadConfiguration(mode):
        if not gConfig and mode != gMode:
            gConfig = Config(os.path.join(gTrainRoot, "steer", "config", "config_%s.json" %mode))
    
    @staticmethod
    def GetConfig():
        if not gConfig:
            raise Exception("Config not set")
        return gConfig 
    
    @staticmethod
    def GetTrainRoot():
        return gTrainRoot
    
    
    @staticmethod
    def SetTrainRoot(trainroot):
        gTrainRoot = trainroot
    
class Config(object):
    
    def __init__(self, filename = None):
        self.__name                     = ""
        self.__version                  = "V1"
        self.__outputdir                = "/project/projectdirs/alice/"
        self.__splitlevel               = -1
        if filename:
            self.Initialize(filename)
        
    def Initialize(self, jsonfile):
        jsontree = json.loads(self.__ReadConfigFile(jsonfile))
        for k, v in jsontree.iteritems():
            if str(k).upper() == "NAME":
                self.__name = v
            elif str(k).upper() == "VERSION":
                self.__version = v
            elif str(k).upper() == "OUTPUT":
                self.__outputdir = v
            elif str(k).upper() == "SPLITLEVEL":
                self.__splitlevel = v
    
    def __ReadConfigFile(self, configfile):
        jsonstring = ""
        reader = open(configfile, 'r')
        for line in reader:
            jsonstring += line.replace("\n","")
        reader.close()
        return jsonstring

    def GetTrainOutputPath(self, doGlobal):
        userdir = os.path.join(getpass.getuser(), "train") if not doGlobal else "train"
        return os.path.join(self.__outputbase, userdir)
    
    def GetName(self):
        return self.__name
    
    def GetVersion(self):
        return self.__version
    
    def GetSplitLevel(self):
        return self.__splitlevel
    