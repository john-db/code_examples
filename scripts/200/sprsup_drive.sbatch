#!/bin/bash
  
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=64gb
#SBATCH --partition=cbcb
#SBATCH --account=cbcb
#SBATCH --constraint=EPYC-7313
#SBATCH --qos=highmem
#SBATCH --time=24:00:00

# paths
GROUPDIR="/fs/cbcb-lab/ekmolloy"
PROJDIR="$GROUPDIR/johndb/Phylo2VecTests"

# inputs
MODL="200_50_2000000_0.000001_0.0000005"
INDIR="$PROJDIR/data/$MODL/$REPL"
GTRE_FILE="$INDIR/genes.newick"
STRE_TRUE="$INDIR/s_tree.trees"

# outputs
OUTDIR="$PROJDIR/results/$MODL/$REPL"

./run_sprsup.sh $MODL $INDIR $OUTDIR $GTRE_FILE $STRE_TRUE $GROUPDIR $PROJDIR
