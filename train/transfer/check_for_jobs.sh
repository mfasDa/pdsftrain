#! /bin/bash

SCRIPTNAME=`readlink -f $0`
BASE=`dirname $SCRIPTNAME`

INPUTDIR=$1
WORKDIR=$2
COMPLETEDIR=$3
LOGDIR=$4

jobs=($(ls -1 $INPUTDIR))
for j in ${jobs[@]}; do
        mv $INPUTDIR/$j $WORKDIR/
        nohup $BASE/launchTransfer.sh $WORKDIR/$j $COMPLETEDIR $LOGDIR/log_$j &
done
