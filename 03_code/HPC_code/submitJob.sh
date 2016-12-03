#PBS -l nodes=1:ppn=1
#PBS -l walltime=24:00:00
#PBS -l mem=100GB
#PBS -N OPT
#PBS -M mc3784@nyu.edu
#PBS -m b -m e -m a -m abe
#PBS -j oe

module purge

SRCDIR=$HOME/OPTIMIZATION/NER_Spectral/pipeline
RUNDIR=$SCRATCH/PIPELINE/run-${PBS_JOBID/.*}
mkdir -p $RUNDIR

cd $PBS_O_WORKDIR
cp -R $SRCDIR/05_entities_avg.py $RUNDIR
cp -R $SRCDIR/submitJob.sh $RUNDIR
cd $RUNDIR
echo "Starting up"
#module load scipy/intel/0.16.0
module purge
module load scikit-learn/intel/0.15.1
module load gensim/intel/0.10.3
echo "After loading gensim/intel/0.13.2"
#module load nltk/3.0.2
python 05_entities_avg.py > result.txt
echo "After running python script"