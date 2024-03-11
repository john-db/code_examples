#!/bin/bash

MYMODL=$1
INDIR=$2
OUTDIR=$3
GTRE_FILE=$4
STRE_TRUE=$5
GROUPDIR=$6
PROJDIR=$7

ASTER="$GROUPDIR/group/software-compiled-on-EPYC-7313/ASTER/bin/astral"
COMPARE="$PROJDIR/tools/compare_two_trees.py"


MYMTHD="aster"
MYSTRE="$OUTDIR/${MYMTHD}"

MYTIME="$(time ($ASTER -i $GTRE_FILE -o $MYSTRE.newick))"

MYTIME="$(echo $MYTIME | awk '{print $2","$4","$6}')"
echo "$MYMODL,$MYMTHD,$SEED,$MYNODE,$MYTIME" > ${MYSTRE}_runtime.csv

MYERR=$(python3 $COMPARE -t1 $STRE_TRUE -t2 $MYSTRE.newick)

echo "$MYMTHD,$MYMODL,$MYERR" > ${MYSTRE}_species_tree_error.csv
