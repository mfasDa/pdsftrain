#! /bin/bash

while read line; do
        ./create_copy_filelist.sh /alice/data/2015/LHC15o /projecta/projectdirs/aliprod/data/LHC15o $line muon_calo_pass1
done < $1
