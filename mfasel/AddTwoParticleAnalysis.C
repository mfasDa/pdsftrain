TwoParticleAnalysis *AddTwoParticleAnalysis(){
	AliAnalysisManager *mgr = AliAnalysisManager::GetAnalysisManager();

	TwoParticleAnalysis *twoparticle = new TwoParticleAnalysis("twoparticleanalysis");
	mgr->AddTask(twoparticle);

	TString filename = mgr->GetCommonFileName() + ":twoparticlehists";

	twoparticle->ConnectInput(1, mgr->GetCommonInputContainer());
	twoparticle->ConnectOutput(1, task->CreateContainer("histocontainer", TList::Class(), AliAnalysisManager::kOutputContainer, filename.Data()));
	return twoparticle;
}
