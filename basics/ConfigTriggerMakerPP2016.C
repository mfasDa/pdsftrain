void ConfigTriggerMakerPP2016(){
	gROOT->LoadMacro("$ALICE_PHYSICS/PWG/EMCAL/macros/AddTaskEmcalTriggerMakerNew.C");
	AliEmcalTriggerMakerTask *triggermaker = AddTaskTriggerEmcalMakerNew("EmcalTriggers", "", "", kTRUE);
	triggermaker->SetUseL0Amplitudes(kFALSE);
	triggermaker->SelectCollisionCandidates(AliVEvent::kAnyINT || AliVEvent::kEGA || AliVEvent::kEJE);
	triggermaker->GetTriggerMaker()->ConfigureForPP2016();
}
