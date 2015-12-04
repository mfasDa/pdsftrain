#! /bin/bash

inputpath=$1
outputpath=$2
run=$3
pass=$4

echo "Input path:  $inputpath"
echo "Output path: $outputpath"
echo "Run:         $run"
echo "Pass:        $pass"

testcmd=$(printf "alien_ls %s/%09d" "$inputpath" $run)
hasfound=0
passes=($(eval $testcmd))
for mypass in ${passes[@]}; do
        if [ "$mypass" == "$pass" ]; then
                hasfound=1
                break
        fi
done
if [ $hasfound -eq 0 ]; then 
        echo Pass $pass not found for run $run
        exit 1
fi
findcmd=$(printf "alien_ls %s/%09d/%s | grep %d" "$inputpath" $run "$pass" $run)
echo $findcmd
myc=($(eval $findcmd))

filelistname=files_$run\_$pass.txt
for c in ${myc[@]}; do
  inputfile=$(printf "%s/%09d/%s/%s/root_archive.zip" $inputpath $run $pass $c)
  outputfile=$(printf "%s/%09d/%s/%s/root_archive.zip" $outputpath $run $pass $c)
  echo "$inputfile $outputfile" >> $filelistname
done
