#!/bin/bash

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

mass=$1
contrib=${2}	# incl, t, b or tb # Combinations are (contrib-scale): incl-t/b/tb, t-t, b-b, tb-tb, t-tb, b-tb 

#set width depending on mass

width=0.0041
if (( $(echo $mass'<'145 | bc -l) )); then 
  width=0.0041
elif (( $(echo $mass'<'605 | bc -l) )); then 
  width=0.1
elif (( $(echo $mass'<'2005 | bc -l) )); then
  width=1
else
  width=2
fi

# set hfact depending on mass and contrib (to do)
hfact=`awk "BEGIN {print ($mass+8.36)/4}"`
if [ "$3" == 1 ]; then hfact=`awk "BEGIN {print 2*($mass+8.36)/4}"`; fi
if [ "$3" == 2 ]; then hfact=`awk "BEGIN {print 0.5*($mass+8.36)/4}"`; fi

#for h125 t = 48, b = 18, t+b = 9
hfact=9 # this 

workdir=`pwd`
massdir=$workdir/m${mass}

if [ "$3" == 1 ]; then massdir=$workdir/m${mass}_up; fi
if [ "$3" == 2 ]; then massdir=$workdir/m${mass}_down; fi

CMSSWdir=$massdir/CMSSW_10_2_3/src
template=$workdir/template

mkdir $massdir
cd $massdir

scramv1 project CMSSW CMSSW_10_2_3
cd $CMSSWdir ; eval `scramv1 runtime -sh` ; cd $massdir

echo "Copying files:"
#cp -v $template/pwgseeds.dat $CMSSWdir
#cp -v $template/pwhg_main $CMSSWdir
#cp -v $template/pwg-rwl.dat $CMSSWdir
#cp -v $template/powheg.input-* $CMSSWdir
#cp -v $template/runcmsgrid.sh $CMSSWdir
cp -r $template/* $CMSSWdir

sed -i "s/XHMASSX/${mass}/g" $CMSSWdir/powheg.input-*
sed -i "s/XHWIDTHX/${width}/g" $CMSSWdir/powheg.input-*
sed -i "s/XHFACTX/${hfact}/g" $CMSSWdir/powheg.input-*
sed -i "s/XHFACTX/${hfact}/g" $CMSSWdir/runcmsgrid.sh

# tanb = 15 for h and A
# tanb = 50 for H
# alpha always pi/4

sed -i "s/XTANBX/15/g" $CMSSWdir/powheg.input-*
sed -i "s/XALPHAX/0.785398163397448/g" $CMSSWdir/powheg.input-*

# depending on contribution requested disable top or bottom couplings
if [ "${contrib}" == "t" ]; then 
  sed -i "s/XNOBOTX/1/g" $CMSSWdir/powheg.input-*
  sed -i "s/XNOTOPX/0/g" $CMSSWdir/powheg.input-*
elif [ "${contrib}" == "b" ]; then
  sed -i "s/XNOBOTX/0/g" $CMSSWdir/powheg.input-*
  sed -i "s/XNOTOPX/1/g" $CMSSWdir/powheg.input-*
else
  sed -i "s/XNOBOTX/0/g" $CMSSWdir/powheg.input-*
  sed -i "s/XNOTOPX/0/g" $CMSSWdir/powheg.input-*
fi

cd $workdir 
