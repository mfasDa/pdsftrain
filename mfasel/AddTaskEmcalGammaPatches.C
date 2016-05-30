void MakeTaskForTrigger(TString name, ULong_t triggerbits, const char *triggerstring){
	AliAnalysisManager *mgr = AliAnalysisManager::GetAnalysisManager();

	AliAnalysisTaskEmcalGammaPatches *patchtask = new AliAnalysisTaskEmcalGammaPatches(name.Data());
	mgr->AddTask(patchtask);
	patchtask->SetTriggerSelection(triggerbits, triggerstring);

	TString outputdir = mgr->GetCommonFileName();
	outputdir += TString::Format(":%s", name.Data());

	mgr->ConnectInput(patchtask, 0, mgr->GetCommonInputContainer());
	mgr->ConnectOutput(patchtask, 1, mgr->CreateContainer(Form("histos_%s", name.Data()), TList::Class(), AliAnalysisManager::kOutputContainer, outputdir.Data()));
}

void AddTaskEmcalGammaPatches(){
  ULong_t triggerbits[4] = {(ULong_t)AliVEvent::kINT7, (ULong_t)AliVEvent::kEMC7, (ULong_t)AliVEvent::kEMCEGA, (ULong_t)AliVEvent::kEMCEJE};
  ULong_t triggerbitsAny = (ULong_t)AliVEvent::kAny;
	MakeTaskForTrigger("gammapatchMB", triggerbits[0], "");
	MakeTaskForTrigger("gammapatchEMC7", triggerbits[1], "EMC7");
	MakeTaskForTrigger("gammapatchDMC7", triggerbits[1], "DMC7");
	MakeTaskForTrigger("gammapatchEG1", triggerbitsAny, "EG1");
	MakeTaskForTrigger("gammapatchEG2", triggerbitsAny, "EG2");
	MakeTaskForTrigger("gammapatchEJ1", triggerbitsAny, "EJ1");
	MakeTaskForTrigger("gammapatchEJ2", triggerbitsAny, "EJ2");
	MakeTaskForTrigger("gammapatchDG1", triggerbitsAny, "DG1");
	MakeTaskForTrigger("gammapatchDG2", triggerbitsAny, "DG2");
	MakeTaskForTrigger("gammapatchDJ1", triggerbitsAny, "DJ1");
	MakeTaskForTrigger("gammapatchDJ2", triggerbitsAny, "DJ2");
}
