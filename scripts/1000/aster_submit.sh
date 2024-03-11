#!/bin/bash

REPLS=( $(seq  -f "%02g" 1 10) )           

for REPL in ${REPLS[@]}; do
	sbatch \
		--job-name="aster" \
		--output="aster.%j.out" \
		--error="aster.%j.err" \
		--export=REPL="$REPL" \
		aster_drive.sbatch
done
