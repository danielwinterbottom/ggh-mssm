#!/bin/bash

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

mass=$1
contrib=${2}	# incl, t, b or tb # Combinations are (contrib-scale): incl-t/b/tb, t-t, b-b, tb-tb, t-tb, b-tb 


workdir=`pwd`
massdir=$workdir/m${mass}_${contrib}

x=${contrib}

if [ "$3" == 1 ]; then 
  massdir=$workdir/m${mass}_${contrib}_up
  x=${contrib}_up
fi
if [ "$3" == 2 ]; then 
  massdir=$workdir/m${mass}_${contrib}_down
  x=${contrib}_down
fi

CMSSWdir=$massdir/CMSSW_10_2_3/src
scripts=$workdir/scripts

mkdir $massdir
cd $massdir

scramv1 project CMSSW CMSSW_10_2_3
cd $CMSSWdir ; eval `scramv1 runtime -sh` ; cd $massdir

echo "Copying files:"
cp -r $scripts/gensim.py $CMSSWdir/.
cp -r $scripts/crab_sub.py $CMSSWdir/.

sed -i "s/XHMASSX/${mass}/g" $CMSSWdir/gensim.py
sed -i "s/XCONTRIBX/${x}/g" $CMSSWdir/gensim.py
sed -i "s/XHTYPEINTX/25/g" $CMSSWdir/gensim.py
sed -i "s/#SM-ON#//g" $CMSSWdir/gensim.py
sed -i "s/XHMASSX/${mass}/g" $CMSSWdir/crab_sub.py
sed -i "s/XCONTRIBX/${x}/g" $CMSSWdir/crab_sub.py

cd $CMSSWdir
cp gridpack/*.tar.gz .

pwd
#crab submit crab_sub.py

cd $workdir 
