#!/bin/bash
#SBATCH -A ghobadk1
#SBATCH --partition=defq
#SBATCH --nodes=4
#SBATCH --time=48:00:00
#SBATCH --output="/data/ghobadk1/simulation_feature_test/Experiements/Experiment_3/25/runtime_log.out"
#SBATCH --mem=100GB
module load anaconda
conda info --envs
source activate shiyu
pwd
python main.py -p parameters/default.py