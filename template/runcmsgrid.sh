#!/bin/bash

nevt=${1}
rnum=${2}	# SEED

scram_arch_version=slc6_amd64_gcc530
cmssw_version=CMSSW_10_2_3

LHEWORKDIR=`pwd`

export SCRAM_ARCH=$scram_arch_version
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r ${cmssw_version}/src ] ; then
	echo release ${cmssw_version} already exists
else
	scram p CMSSW ${cmssw_version}
fi
cd ${cmssw_version}/src
eval `scram runtime -sh`
cd -

#cd $LHEWORKDIR


cat powheg.input-base > powheg.input
sed -i "s/NEVENTS/${nevt}/g" powheg.input
sed -i "s/SEED/${rnum}/g" powheg.input
echo "parallelstage 4" >> powheg.input
echo $rnum > pwgseeds.dat


if [ -f pwgevents-0001.lhe ] ; then
        mv pwgevents-0001.lhe pwgevents-0001.lhe_old
fi

libs=$LHEWORKDIR"/lib"
#LD_LIBRARY_PATH=$(echo $LD_LIBRARY_PATH":/vols/cms/dw515/lib")
LD_LIBRARY_PATH=$(echo ${LD_LIBRARY_PATH}:${libs})

echo $LD_LIBRARY_PATH

echo "Start generating events on " `date`
#echo $rnum | ./pwhg_main > lhe_generation.log 2>&1 &
echo 1 | ./pwhg_main > lhe_generation.log 2>&1 &
wait

# do reweighting

sed -i "/compute_rwgt/c\compute_rwgt 1" powheg.input

# rweight h tb
sed -i "/lhrwgt_id/c\lhrwgt_id \'h_tb\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 1" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# rweight h t-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'h_t\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 1" powheg.input
sed -i "/higgstype/c\higgstype 1" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# rweight h b-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'h_b\'" powheg.input
sed -i "/notop/c\notop 1" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 1" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# rweight A tb
sed -i "/lhrwgt_id/c\lhrwgt_id \'A_tb\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 3" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# rweight A t-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'A_t\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 1" powheg.input
sed -i "/higgstype/c\higgstype 3" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# rweight A b-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'A_b\'" powheg.input
sed -i "/notop/c\notop 1" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 3" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# rweight H tb
sed -i "/lhrwgt_id/c\lhrwgt_id \'H_tb\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 2" powheg.input
sed -i "/tanb/c\tanb 50" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# rweight H t-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'H_t\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 1" powheg.input
sed -i "/higgstype/c\higgstype 2" powheg.input
sed -i "/tanb/c\tanb 50" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# rweight H b-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'H_b\'" powheg.input
sed -i "/notop/c\notop 1" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 2" powheg.input
sed -i "/tanb/c\tanb 50" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# hfact variation weights for testing
sed -i "/tanb/c\tanb 15" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 1" powheg.input
sed -i "/higgstype/c\higgstype 1" powheg.input
sed -i "/#hfact/c\ " powheg.input

hfact=XHFACTX
hfact_up=`awk "BEGIN {print 2*${hfact}}"`
hfact_down=`awk "BEGIN {print 0.5*${hfact}}"`

# nominal

sed -i "/lhrwgt_id/c\lhrwgt_id \'hfact_nominal\'" powheg.input
sed -i "/^hfact/c\hfact ${hfact}" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# up

sed -i "/lhrwgt_id/c\lhrwgt_id \'hfact_up\'" powheg.input
sed -i "/^hfact/c\hfact ${hfact_up}" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# down

sed -i "/lhrwgt_id/c\lhrwgt_id \'hfact_down\'" powheg.input
sed -i "/^hfact/c\hfact ${hfact_down}" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# change hfact back to nominal value
sed -i "/^hfact/c\hfact ${hfact}" powheg.input

# change mass schemes

sed -i "/tanb/c\tanb 15" powheg.input
sed -i "/scheme 0/c\scheme 1" powheg.input
sed -i "/topmass/c\topmass 163.0" powheg.input
sed -i "/bottommass/c\bottommass 4.18d0" powheg.input

# reweight h tb
sed -i "/lhrwgt_id/c\lhrwgt_id \'h_tb_msbar\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 1" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# reweight h t-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'h_t_msbar\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 1" powheg.input
sed -i "/higgstype/c\higgstype 1" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# reweight h b-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'h_b_msbar\'" powheg.input
sed -i "/notop/c\notop 1" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 1" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# reweight A tb
sed -i "/lhrwgt_id/c\lhrwgt_id \'A_tb_msbar\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 3" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# reweight A t-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'A_t_msbar\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 1" powheg.input
sed -i "/higgstype/c\higgstype 3" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# reweight A b-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'A_b_msbar\'" powheg.input
sed -i "/notop/c\notop 1" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 3" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# reweight H tb
sed -i "/lhrwgt_id/c\lhrwgt_id \'H_tb_msbar\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 2" powheg.input
sed -i "/tanb/c\tanb 50" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# reweight H t-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'H_t_msbar\'" powheg.input
sed -i "/notop/c\notop 0" powheg.input
sed -i "/nobot/c\nobot 1" powheg.input
sed -i "/higgstype/c\higgstype 2" powheg.input
sed -i "/tanb/c\tanb 50" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe

# reweight H b-only
sed -i "/lhrwgt_id/c\lhrwgt_id \'H_b_msbar\'" powheg.input
sed -i "/notop/c\notop 1" powheg.input
sed -i "/nobot/c\nobot 0" powheg.input
sed -i "/higgstype/c\higgstype 2" powheg.input
sed -i "/tanb/c\tanb 50" powheg.input

echo $'1\npwgevents-0001.lhe' | ./pwhg_main &> run_pstage_5_1_test.log
mv pwgevents-rwgt-0001.lhe pwgevents-0001.lhe


cat pwgevents-0001.lhe | grep -v "Random number generator exit values" > cmsgrid_final.lhe
python mod_scalup.py cmsgrid_final.lhe XHFACTX

cp cmsgrid_final*.lhe ..
mv cmsgrid_final_mod.lhe cmsgrid_final.lhe

sed -i '/^#new weight/d' cmsgrid_final.lhe

xmllint --noout cmsgrid_final.lhe > /dev/null 2>&1; test $? -eq 0 || fail_exit "xmllint integrity check failed on pwgevents.lhe"

echo "End of job on " `date`
