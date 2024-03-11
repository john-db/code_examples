#!/bin/bash

MYMODL=$1
INDIR=$2
OUTDIR=$3
GTRE_FILE=$4
STRE_TRUE=$5
GROUPDIR=$6
PROJDIR=$7

SPRSUP="$PROJDIR/software/spr_supertrees_1_2_1/spr_supertree"
COMPARE="$PROJDIR/tools/compare_two_trees.py"


MYMTHD="r_sprsup_split"
MYSTRE="$OUTDIR/${MYMTHD}"
OPTIONS="-split_approx"
MYTIME="$(time ($SPRSUP $OPTIONS < $GTRE_FILE &> $MYSTRE.log))"

cat $MYSTRE.log | grep "Final Supertree:" | awk '{print $3";"}' > $MYSTRE.newick

MYTIME="$(echo $MYTIME | awk '{print $2","$4","$6}')"
echo "$MYMODL,$MYMTHD,$SEED,$MYNODE,$MYTIME" > ${MYSTRE}_runtime.csv

MYERR=$(python3 $COMPARE -t1 $STRE_TRUE -t2 $MYSTRE.newick)

echo "$MYMTHD,$MYMODL,$MYERR" > ${MYSTRE}_species_tree_error.csv
