#! /bin/bash

TRAINROOT=$1
INPUTDIR=$2
OUTPUTDIR=$3
FILENAME=$4

cd $OUTPUTDIR
export TRAIN_ROOT=$TRAINROOT
source $TRAIN_ROOT/train/config/env

python $TRAIN_ROOT/run.py merge -i $INPUTDIR -f $FILENAME