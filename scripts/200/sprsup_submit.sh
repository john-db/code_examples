#!/bin/bash

REPLS=( $(seq  -f "%02g" 1 10) )           

for REPL in ${REPLS[@]}; do
	sbatch \
		--job-name="r_sprsup_split" \
		--output="sprsup.%j.out" \
		--error="sprsup.%j.err" \
		--export=REPL="$REPL" \
		sprsup_drive.sbatch
done
