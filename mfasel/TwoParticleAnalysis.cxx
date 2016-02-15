#include <algorithm>
#include <vector>

#include <TMath.h>
#include <TList.h>
#include <TVector3.h>

#include "AliESDtrackCuts.h"
#include "AliESDtrack.h"
#include "AliMCEvent.h"
#include "TTreeSRedirector.h"

#include "TwoParticleAnalysis.h"

ClassDef(TwoParticleAnalysis)

TwoParticleAnalysis::TwoParticleAnalysis():
		AliAnalysisTaskSE(name),
		fTrackCuts(NULL),
		fHistos(NULL),
		hEventCount(0);
		fTreeStreem(NULL)
{
}

TwoParticleAnalysis::TwoParticleAnalysis(const char *name):
		AliAnalysisTaskSE(name),
		fTrackCuts(NULL),
		fHistos(NULL)
{
	DefineOutput(1, TList::Class());
}

TwoParticleAnalysis::~TwoParticleAnalysis(){
	if(fTreeStream) delete fTreeStream;
}

void TwoParticleAnaly  fTrackCuts = AliESDtrackCuts::GetStandardITSTPCTrackCuts2011(true, 1);
	fTrackCuts->DefineHistograms(kRed);
	fTrackCuts->SetName("Standard Track cuts");
	fTrackCuts->SetMinNCrossedRowsTPC(120);
	fTrackCuts->SetMaxDCAToVertexXYPtDep("0.0182+0.0350/pt^1.01");
	fTrackCuts->DefineHistograms(kRed);

	fHistos = new TList;
	fHistos->Add((hEventCount = new TH1F("hEventCount", "This histogram is so stupid", 1, 0.5, 1.5)));
	fHistos->Add(fTrackCuts);

	PostData(1, fHistos);

	fTreeStream = new TTreeSRedirector("trackingDebug.root");
}

void TwoParticleAnalysis::UserExec(Option_t *opt){
	hEventCount->Fill();
	PostData(1, fHistos);

	AliVParticle *part = NULL;
	std::vector<ParticleStruct> particles;
	for(int ipart = 0; ipart < MCEvent()->GetNumberOfTracks(); ++ipart){
		part = MCEvent()->GetTrack(ipart);
		if(!part->IsPhysicalPrimary()) continue;
		if(!part->Charge()) continue;
		particles.push_back(Particle(part->Pt(), part->Eta(), part->Phi(), part->GetLabel()));
	}

	std::sort(particles.begin(), particles.end());
	ParticleStruct &leadingpart = particles[particles.size()-1], &subleadingpart = particles[particles.size()-1];

	AliESDtrack *track = NULL;
	for(int itrk = 0; itrk < InputEvent()->GetNumberOfTracks(); itrk++){
		track = static_cast<AliESDtrack *>(InputEvent->GetTrack(itrk));
		unsigned int tracklabel = TMath::Abs(track->GetLabel());
		if(tracklabel != TMath::Abs(leadingpart.Label()) || tracklabel != TMath::Abs(subleadingpart.Label())) continue;
		if(!fTrackCuts->IsTrackAccepted()) continue;
		if(tracklabel == TMath::Abs(leadingpart.Label())) leadingpart.SetReconstructed();
		else subleadingpart.SetReconstructed();
	}

	// fill tree
	TVector3 lv, sv;
	lv.SetPtEtaPhi(leadingpart.Pt(), leadingpart.Eta(), leadingpart.Phi());
	sv.SetPtEtaPhi(subleadingpart.Pt(), subleadingpart.Eta(), subleadingpart.Phi());
	(*fTreeStream) << "TwoParticleRes"
			<< "ptleading=" << leadingpart.Pt()
			<< "etaleading=" << leadingpart.Eta()
			<< "phileading=" << leadingpart.Phi()
			<< "ptsubleading=" << subleadingpart.Pt()
			<< "etasubleading=" << subleadingpart.Eta()
			<< "phisubleading=" << subleadingpart.Phi()
			<< "leadingrec=" << (leadingpart.Reconstructed() ? 1 : 0)
			<< "subleadingrec=" << (subleadingpart.Reconstructed() ? 1 : 0)
			<< "deta=" << (subleading.Eta() - leading.Eta())
			<< "dphi=" << (subleading.Phi() - leading.Phi())
			<< "dr=" << (lv.DeltaR(sv));
			<< "\n";
}
