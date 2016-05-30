AliAnalysisTaskEmcalGammaPatchesRef *MakeTaskForTrigger(const char *name, ULong_t triggerbits, const char *triggerstring){
	AliAnalysisManager *mgr = AliAnalysisManager::GetAnalysisManager();

	AliAnalysisTaskEmcalGammaPatches *patchtask = new AliAnalysisTaskGammaPatches(name);
	mgr->AddTask(patchtask);
	patchtask->SetTriggerSelection(triggerbits, triggerstring);

	TString outputdir = mgr->GetCommonFileName();
	outputdir += TString::Format(":%s", name);

	mgr->ConnectInput(patchtask, 1, mgr->GetCommonInputContainer());
	mgr->ConnectOutput(patchtask, 1, mgr->CreateContainer(Form("histos_%s", name), TList::Class(), AliAnalysisManager::kOutputContainer, outputdir.Data()));
}

void AddTaskEmcalGammaPatches(){
	MakeTaskForTrigger("gammapatchMB", AliVEvent::kInt7, "");
	MakeTaskForTrigger("gammapatchEMC7", AliVEvent::kEMC7, "EMC7");
	MakeTaskForTrigger("gammapatchEG1", AliVEvent::kEGA, "EG1");
	MakeTaskForTrigger("gammapatchEG2", AliVEvent::kEGA, "EG2");
	MakeTaskForTrigger("gammapatchEJ1", AliVEvent::kEJE, "EJ1");
	MakeTaskForTrigger("gammapatchEJ2", AliVEvent::kEJE, "EJ2");
	MakeTaskForTrigger("gammapatchDG1", AliVEvnet::kEGA, "DG1");
	MakeTaskForTrigger("gammapatchDG2", AliVEvnet::kEGA, "DG2");
	MakeTaskForTrigger("gammapatchDJ1", AliVEvnet::kEGA, "DJ1");
	MakeTaskForTrigger("gammapatchDJ2", AliVEvnet::kEGA, "DJ2");
}
