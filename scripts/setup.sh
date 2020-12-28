#!/bin/bash

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

mass=$1
contrib=${2}	# incl, t, b or tb # Combinations are (contrib-scale): incl-t/b/tb, t-t, b-b, tb-tb, t-tb, b-tb 

#set width depending on mass

width=0.00407
if (( $(echo $mass'<'145 | bc -l) )); then 
  width=0.00407
elif (( $(echo $mass'<'605 | bc -l) )); then 
  width=0.1
elif (( $(echo $mass'<'2005 | bc -l) )); then
  width=1
else
  width=2
fi

# set hfact depending on mass and contrib

#for h125 t = 48, b = 18, t+b = 9
hfact=9 

inline=$(cat scripts/scales-higgs-mass-scan.dat | grep -P "^${mass}\t")

if [ "$inline" == "" ]; then
  echo "Error: There are no hfact damping scales for your chosen mass point, exiting."
  exit
fi

stringarray=($inline)
if [ "${contrib}" == "t" ]; then
  hfact=${stringarray[1]}
elif [ "${contrib}" == "b" ]; then
  hfact=${stringarray[2]}
elif [ "${contrib}" == "tb" ]; then
  hfact=${stringarray[3]}
else
  echo "Error: Your chosen contribution must can only be t, b, tb, exiting"
  exit
fi

if [ "$3" == 1 ]; then hfact=`awk "BEGIN {print 2*${hfact}}"`; fi
if [ "$3" == 2 ]; then hfact=`awk "BEGIN {print 0.5*${hfact}}"`; fi

echo "hfact set to: " $hfact

workdir=`pwd`
massdir=$workdir/m${mass}_${contrib}

if [ "$3" == 1 ]; then massdir=$workdir/m${mass}_${contrib}_up; fi
if [ "$3" == 2 ]; then massdir=$workdir/m${mass}_${contrib}_down; fi

CMSSWdir=$massdir/CMSSW_10_2_3/src
template=$workdir/template

mkdir $massdir
cd $massdir

export SCRAM_ARCH=slc7_amd64_gcc700
scramv1 project CMSSW CMSSW_10_2_3
cd $CMSSWdir ; eval `scramv1 runtime -sh` ; cd $massdir

echo "Copying files:"
cp -r $template/* $CMSSWdir

sed -i "s/XHMASSX/${mass}/g" $CMSSWdir/powheg.input-*
sed -i "s/XHWIDTHX/${width}/g" $CMSSWdir/powheg.input-*
sed -i "s/XHFACTX/${hfact}/g" $CMSSWdir/powheg.input-*
sed -i "s/XHFACTX/${hfact}/g" $CMSSWdir/runcmsgrid.sh

# tanb = 15 for h and A
# tanb = 50 for H
# alpha always pi/4



tanb=15

#if (( $(echo $mass'<'200 | bc -l) )); then
#  tanb=5
#elif (( $(echo $mass'<'300 | bc -l) )); then
#  tanb=7
#elif (( $(echo $mass'<'400 | bc -l) )); then
#  tanb=12
#else
#  tanb=15
#fi

echo tanb set to ${tanb}

sed -i "s/XTANBX/${tanb}/g" $CMSSWdir/powheg.input-*
sed -i "s/XALPHAX/0.785398163397448/g" $CMSSWdir/powheg.input-*

# we produce every nominal distribution as t-only as this has better stats at high pT, then the ME reweighting takes care of the difference
sed -i "s/XNOBOTX/1/g" $CMSSWdir/powheg.input-*
sed -i "s/XNOTOPX/0/g" $CMSSWdir/powheg.input-*
## depending on contribution requested disable top or bottom couplings
#if [ "${contrib}" == "t" ]; then 
#  sed -i "s/XNOBOTX/1/g" $CMSSWdir/powheg.input-*
#  sed -i "s/XNOTOPX/0/g" $CMSSWdir/powheg.input-*
#elif [ "${contrib}" == "b" ]; then
#  sed -i "s/XNOBOTX/0/g" $CMSSWdir/powheg.input-*
#  sed -i "s/XNOTOPX/1/g" $CMSSWdir/powheg.input-*
#else
#  sed -i "s/XNOBOTX/0/g" $CMSSWdir/powheg.input-*
#  sed -i "s/XNOTOPX/0/g" $CMSSWdir/powheg.input-*
#fi

cd $workdir 
