#!/bin/bash -l

#SBATCH --job-name=qh-plot
#SBATCH --time=00:30:00
#SBATCH --output=qh-plot-%j.out
#SBATCH --error=qh-plot-%j.err

conda activate project7_env

rm -f plot.data
mkdir -p charts

# strong scaling
for N in 100 1000 10000 100000
do
    for p in 1 2 4 8 16 32
    do
        mpiexec -n $p python mpi_main.py $N -$N $N
    done
    echo >> plot.data
    echo >> plot.data
done

gnuplot gp4strong.gp
