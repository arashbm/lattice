#!/bin/bash
set -ex

parallel --nice 20 --header : \
  sbatch --array 1-128 run_pc.sh {pc} \
  ::: pc 0.478018 $(seq 0 0.01 1.0)
