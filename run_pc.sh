#!/bin/bash
#SBATCH --job-name lattice-percolation
#SBATCH --time 4:00:00
#SBATCH --mem-per-cpu=50M
#SBATCH --output /dev/null
#SBATCH --error /dev/null
#SBATCH --cpus-per-task 1


dims=2
multi=$((48*$SLURM_CPUS_PER_TASK))

mkdir -p out/$dims

parallel -j 1 --header : \
  python lattice.py \
  --pc $1 \
  --dimensions $dims \
  --nodes {nodes} \
  --seed {i} \
  --time 1024 \
  ::: i $(seq $((SLURM_ARRAY_TASK_ID*multi)) $(((SLURM_ARRAY_TASK_ID+1)*multi-1))) \
  ::: nodes 4 8 16 32 64 128 \
  > out/$dims/s-$SLURM_ARRAY_TASK_ID-pc-$1.csv
