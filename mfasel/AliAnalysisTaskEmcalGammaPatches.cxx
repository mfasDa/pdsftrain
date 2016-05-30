#include <bitset>
#include <iostream>

#include <TArrayD.h>
#include <TClonesArray.h>
#include <THashList.h>
#include <THistManager.h>

#include "AliEMCALTriggerPatchInfo.h"
#include "AliInputEventHandler.h"
#include "AliVEvent.h"

#include "AliAnalysisTaskEmcalGammaPatches.h"

ClassImp(AliAnalysisTaskEmcalGammaPatches)

AliAnalysisTaskEmcalGammaPatches::AliAnalysisTaskEmcalGammaPatches():
	AliAnalysisTaskSE(),
	fTriggerBits(AliVEvent::kAny),
	fTriggerString(""),
	fHistManager(NULL)
{
}

AliAnalysisTaskEmcalGammaPatches::AliAnalysisTaskEmcalGammaPatches(const char *name):
	AliAnalysisTaskSE(name),
	fTriggerBits(AliVEvent::kAny),
	fTriggerString(""),
	fHistManager(NULL)
{
	DefineOutput(1, TList::Class());
}

AliAnalysisTaskEmcalGammaPatches::~AliAnalysisTaskEmcalGammaPatches() {
}

void AliAnalysisTaskEmcalGammaPatches::UserCreateOutputObjects(){
	fHistManager = new THistManager("histosGammaPatches");

	TArrayD energybinning, amplitudebinning;
	CreateEnergyBinning(energybinning);
	CreateAmplitudeBinning(amplitudebinning);

  fHistManager->CreateTH1("hEvents", "Number of events", 1., 0.5, 1.5);
	fHistManager->CreateTH1("patchL1AmplitudeEMCAL", "Patch Level1 amplitude for patches in EMCAL", amplitudebinning);
	fHistManager->CreateTH1("patchL1EnergyEMCAL", "Patch L1 energy estimate for patches in EMCAL", energybinning);
	fHistManager->CreateTH1("patchL1AmplitudeDCAL", "Patch Level1 amplitude for patches in DCAL", amplitudebinning);
	fHistManager->CreateTH1("patchL1EnergyDCAL", "Patch L1 energy estimate for patches in DCAL", energybinning);
  printf("Several histograms created\n");

	PostData(1, fHistManager->GetListOfHistograms());
}

void AliAnalysisTaskEmcalGammaPatches::UserExec(Option_t *opt){
  //std::cout << "Trigger bits " << std::bitset<64>(fTriggerBits) << std::endl;
  //std::cout << "Event bits " << std::bitset<64>(fInputHandler->IsEventSelected()) << std::endl;
	if(!(fInputHandler->IsEventSelected() & fTriggerBits)) return;
	if(fTriggerString.Length()){
    //printf("Checking for trigger string: %s\n", fTriggerString.Data());
    //printf("Triggers: %s\n", fInputEvent->GetFiredTriggerClasses().Data());
		if(!fInputEvent->GetFiredTriggerClasses().Contains(fTriggerString)) return;
    //printf("event selected\n");
	}

  fHistManager->FillTH1("hEvents", 1);

	TClonesArray *triggerpatches = static_cast<TClonesArray *>(fInputEvent->FindListObject("EmcalTriggers"));
  //if(!triggerpatches) printf("trigger patche not found in the list of objects\n");
	for(TIter patchiter = TIter(triggerpatches).Begin(); patchiter != TIter::End(); ++patchiter){
		AliEMCALTriggerPatchInfo *currentpatch = static_cast<AliEMCALTriggerPatchInfo *>(*patchiter);
		if(!(currentpatch->IsGammaHighRecalc() || currentpatch->IsGammaLowRecalc())) continue;
		TString detector = "EMCAL";
		if(!currentpatch->IsEMCal()) detector = "DCAL";
		fHistManager->FillTH1(Form("patchL1Amplitude%s", detector.Data()), currentpatch->GetADCAmp());
		fHistManager->FillTH1(Form("patchL1Energy%s", detector.Data()), currentpatch->GetADCAmpGeVRough());
	}
}

void AliAnalysisTaskEmcalGammaPatches::CreateEnergyBinning(TArrayD &binning){
	std::map<double, double> limits;
	limits.insert(std::pair<double, double>(15, 0.5));
	limits.insert(std::pair<double, double>(20, 1.));
	limits.insert(std::pair<double, double>(40, 2.));
	limits.insert(std::pair<double, double>(60, 5.));
	limits.insert(std::pair<double, double>(100, 10.));
	limits.insert(std::pair<double, double>(200, 20.));

	std::vector<double> binedges;
	binedges.push_back(0.);
	double current = 0.;
	for(std::map<double, double>::iterator limititer = limits.begin(); limititer != limits.end(); ++limititer){
		while(current < limititer->first){
			current += limititer->second;
			binedges.push_back(current);
		}
	}

	binning.Set(binedges.size());
	int mybin = 0;
	for(std::vector<double>::iterator edgeit = binedges.begin(); edgeit != binedges.end(); ++edgeit)
		binning[mybin++] = *edgeit;
}

void AliAnalysisTaskEmcalGammaPatches::CreateAmplitudeBinning(TArrayD &binning){
	std::map<double, double> limits;
	limits.insert(std::pair<double, double>(200, 1));
	limits.insert(std::pair<double, double>(500, 5.));
	limits.insert(std::pair<double, double>(3000, 10.));
	limits.insert(std::pair<double, double>(5000, 50.));
	limits.insert(std::pair<double, double>(1000, 100.));

	std::vector<double> binedges;
	binedges.push_back(0.);
	double current = 0.;
	for(std::map<double, double>::iterator limititer = limits.begin(); limititer != limits.end(); ++limititer){
		while(current < limititer->first){
			current += limititer->second;
			binedges.push_back(current);
		}
	}

	binning.Set(binedges.size());
	int mybin = 0;
	for(std::vector<double>::iterator edgeit = binedges.begin(); edgeit != binedges.end(); ++edgeit)
		binning[mybin++] = *edgeit;
}
