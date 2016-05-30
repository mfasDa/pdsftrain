void ConfigTriggerMakerPP2016(){
	gROOT->LoadMacro("$ALICE_PHYSICS/PWG/EMCAL/macros/AddTaskEmcalTriggerMakerNew.C");
	AliEmcalTriggerMakerTask *triggermaker = AddTaskEmcalTriggerMakerNew("EmcalTriggers", "", "", kTRUE);
	triggermaker->SetUseL0Amplitudes(kFALSE);
	triggermaker->SelectCollisionCandidates(AliVEvent::kAny);
	//triggermaker->SelectCollisionCandidates(AliVEvent::kAnyINT | AliVEvent::kEMCEGA | AliVEvent::kEMCEJE);
	triggermaker->GetTriggerMaker()->ConfigureForPP2015();
}
