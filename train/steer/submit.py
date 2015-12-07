import os
from train.steer.config import ConfigHandler
    
class Submitter():
    
    def __init__(self, inputlist, jobtrainroot, outputdir, splitlevel):
        self.__inputlist = inputlist
        self.__jobtrainroot = jobtrainroot
        self.__outputdir = outputdir
        self.__nchunk = -1
        self.__splitlevel = splitlevel
        self.__user = "all"
        
    def SetUser(self, user):
        self.__user = user
        
    def SetNchunk(self, nchunk):
        self.__nchunk = nchunk
    
    def Submit(self):
        jobs = self.__nchunk
        if jobs < 0:
            jobs = int(self.GetNfiles()) / self.__splitlevel + 1
        for j in range(1, jobs+1):
            os.makedirs(os.path.join(self.__outputdir, "job%d" %j))
        qsub = "qsub -l \"projectio=1,h_vmem=4G\" -t 1:%d" %jobs
        qsub += " " + self.__GetLogging()
        qsub += " " + self.__GetExecutable()
        #print "Here I would do %s" %qsub
        os.system(qsub)
        
    def __GetExecutable(self):
        return "%s %s %s %s %s %s %s" %(os.path.join(self.__jobtrainroot, "train", "steer", "jobscript.sh"), self.__jobtrainroot, ConfigHandler.GetConfig().GetName(), self.__outputdir, self.__user, self.__inputlist, self.__splitlevel)
    
    def __GetLogging(self):
        return "-j y -o %s/job\$TASK_ID/joboutput.log" %self.__outputdir
       
    def GetNfiles(self): 
        nfiles = 0
        reader = open(os.path.join(self.__jobtrainroot, "train", "filelists", self.__inputlist), 'r')
        for line in reader:
            newline = line.replace("\n", "").lstrip().rstrip()
            if not len(newline):
                continue
            nfiles += 1
        reader.close()
        return nfiles
