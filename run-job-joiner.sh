#!/bin/bash
#SBATCH --mem=102400M
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=24:00:00
#SBATCH --mail-user=A00744368@tec.mx
#SBATCH --mail-type=ALL
cd ~/projects/def-pbranco/josecm08/datasets/dataset_splitter
module purge
module load python/3.10 scipy-stack
source ~/py10efc/bin/activate
python joiner.py
