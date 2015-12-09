void LoadLibs(){
	/*
	 * Loading fastjet libraries - Required for jet libraries
	 */

	TString libs[] = {"CGAL","fastjet","siscone","siscone_spherical","fastjetplugins","fastjettools","fastjetcontribfragile"};
	for(TString *libiter = libs; libiter < libs + sizeof(libs)/sizeof(TString); libiter++){
		gSystem->Load(Form("lib%s", libiter->Data()));
	}
}
