#ifndef AliAnalysisTaskEmcalGammaPatches_h
#define AliAnalysisTaskEmcalGammaPatches_h

#include <TString.h>
#include <AliAnalysisTaskSE.h>

class TArrayD;
class THistManager;

class AliAnalysisTaskEmcalGammaPatches : public AliAnalysisTaskSE {
	ULong_t						fTriggerBits;
	TString						fTriggerString;
	THistManager 				*fHistManager;

public:
	AliAnalysisTaskEmcalGammaPatches();
	AliAnalysisTaskEmcalGammaPatches(const char *name);
	virtual ~AliAnalysisTaskEmcalGammaPatches();

	void SetTriggerSelection(ULong_t triggerbits, TString triggerstring){
		fTriggerBits = triggerbits;
		fTriggerString = triggerstring;
	}

protected:
	virtual void UserCreateOutputObjects();
	virtual void UserExec(Option_t *);
	void CreateEnergyBinning(TArrayD &binning);
	void CreateAmplitudeBinning(TArrayD &binning);

	ClassDef(AliAnalysisTaskEmcalGammaPatches, 1);
};

#endif
