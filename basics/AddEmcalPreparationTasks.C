void AddEmcalPreparationTasks()
{
  AliAnalysisManager *mgr = AliAnalysisManager::GetAnalysisManager();

  printf("Loading setup task\n");
  printf("ALICE_PHYSICS: %s\n", gSystem->Getenv("ALICE_PHYSICS"));
  gROOT->LoadMacro(Form("%s/PWG/EMCAL/macros/AddTaskEmcalSetup.C", gSystem->Getenv("ALICE_PHYSICS")));
  AliEmcalSetupTask *setupTask = AddTaskEmcalSetup();
  //setupTask->SetOcdbPath("local:///cvmfs/alice-ocdb.cern.ch/calibration/data/2015/OCDB");
  setupTask->SetOcdbPath("raw://");

  Bool_t  bDistBC          = kFALSE; //switch for recalculation cluster position from bad channel
  Bool_t  bRecalibClus     = kFALSE;
  Bool_t  bRecalcClusPos   = kFALSE;
  Bool_t  bNonLinearCorr   = kFALSE;
  Bool_t  bRemExoticCell   = kFALSE;
  Bool_t  bRemExoticClus   = kFALSE;
  Bool_t  bFidRegion       = kFALSE;
  Bool_t  bCalibEnergy     = kTRUE;
  Bool_t  bCalibTime       = kTRUE;
  Bool_t  bRemBC           = kTRUE;
  UInt_t  iNonLinFunct     = AliEMCALRecoUtils::kNoCorrection;
  Bool_t  bReclusterize    = kFALSE;
  Float_t fSeedThresh      = 0.1;      // 100 MeV
  Float_t fCellThresh      = 0.05;     // 50 MeV
  UInt_t  iClusterizer     = AliEMCALRecParam::kClusterizerv2;
  Bool_t  bTrackMatch      = kFALSE;
  Bool_t  bUpdateCellOnly  = kFALSE;
  Float_t fTimeMin         = -50e6;   // minimum time of physical signal in a cell/digit
  Float_t fTimeMax         =  50e6;   // maximum time of physical signal in a cell/digit
  Float_t fTimeCut         =  25e6;
  const char *cPass        = 0;

  gROOT->LoadMacro("$ALICE_PHYSICS/PWG/EMCAL/macros/AddTaskEMCALTender.C");
  AliAnalysisTaskSE *pTenderTask = AddTaskEMCALTender(bDistBC, bRecalibClus, bRecalcClusPos, bNonLinearCorr, bRemExoticCell, bRemExoticClus,
						      bFidRegion, bCalibEnergy, bCalibTime, bRemBC, iNonLinFunct, bReclusterize, fSeedThresh,
						      fCellThresh, iClusterizer, bTrackMatch, bUpdateCellOnly, fTimeMin, fTimeMax, fTimeCut, cPass);
  
  gROOT->LoadMacro("$ALICE_PHYSICS/PWG/EMCAL/macros/AddTaskClusterizerFast.C");
  AliAnalysisTaskEMCALClusterizeFast *pClusterizerTask = AddTaskClusterizerFast("ClusterizerFast", "", "", iClusterizer,
										fCellThresh, fSeedThresh, fTimeMin, fTimeMax, fTimeCut,
										kFALSE, kFALSE, AliAnalysisTaskEMCALClusterizeFast::kFEEData);

  gROOT->LoadMacro("$ALICE_PHYSICS/PWG/EMCAL/macros/AddTaskEmcalTriggerMakerNew.C");
  AliEmcalTriggerMakerTask *triggermaker = AddTaskEmcalTriggerMakerNew("EmcalTriggers",0,0,"AliEmcalTriggerMaker",8,0,0,0,0,0,0,0,0,0,0,0,0,0,1);
  triggermaker->SetUseTriggerBitConfig(AliEmcalTriggerMaker::kNewConfig);
  triggermaker->SetUseNewCentralityEstimation(kTRUE);
  triggermaker->SetNCentBins(5);

  bRemExoticClus = kTRUE;
  iNonLinFunct   = AliEMCALRecoUtils::kNoCorrection;
  
  gROOT->LoadMacro("$ALICE_PHYSICS/PWG/EMCAL/macros/AddTaskEmcalClusterMaker.C");
  AliEmcalClusterMaker *pClusterMakerTask = AddTaskEmcalClusterMaker(iNonLinFunct, bRemExoticClus, 0, "", 0, kTRUE);
  pClusterMakerTask->GetClusterContainer(0)->SetClusECut(0.);
  pClusterMakerTask->GetClusterContainer(0)->SetClusPtCut(0.);
  pClusterMakerTask->SetUseNewCentralityEstimation(kTRUE);
  pClusterMakerTask->SetNCentBins(5);
}
