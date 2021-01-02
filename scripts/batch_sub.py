import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--numEvents'     , dest="numEvents",     default= '2000',         help='number of events for a single job [2000]')
parser.add_argument('-j', '--numJobs'       , dest="numJobs",       default= '10',           help='number of jobs to be used for multicore grid step 1,2,3')
parser.add_argument('-x', '--xgrid'         , dest="xgrid",         default= '1',            help='loop number for the grids production [1]')
parser.add_argument('-p', '--parstage'      , dest="parstage",      default= '0',            help='stage of the production process [0]')

args = parser.parse_args ()

numEvents = args.numEvents
numJobs = args.numJobs
xgrid = args.xgrid
parstage = args.parstage

inputName = 'powheg.input'

os.system('cp powheg.input-base powheg.input')
os.system('sed -i "s/^numevts.*/numevts '+args.numEvents+'/" powheg.input')


if not 'parallelstage' in open(inputName).read() :
    parstage_ = parstage
    if int(parstage)>4: parstage_ = '4'
    os.system("echo \'\n\nparallelstage "+parstage_+"\' >> "+inputName)


jobtag = 'pstage_'+parstage

if parstage == '1':
  if not 'xgriditeration' in open(inputName).read() :
      os.system("echo \'xgriditeration "+xgrid+"\' >> "+inputName)
#  if not 'fakevirt' in open(inputName).read() :
#      os.system("echo \'fakevirt 1\' >> "+inputName) # this was used in standard script for condor - check what this does!!
  jobtag+='_xgrid_'+xgrid
else:
  if not 'xgriditeration' in open(inputName).read() :
    os.system("echo \'xgriditeration 1\' >> "+inputName)

if parstage in ['5','6','7']:
  os.system('sed -i "/compute_rwgt/c\compute_rwgt 1" powheg.input')
  if parstage == '5':
    os.system('sed -i "/lhrwgt_id/c\lhrwgt_id \'reweight\'" powheg.input')
    os.system('sed -i "/notop/c\\notop 1" powheg.input')
    #os.system('sed -i "/notop/c\notop 1" powheg.input')
#  if parstage == '6':
#    os.system('sed -i "/lhrwgt_id/c\lhrwgt_id \'ps_weight\'" powheg.input')
#    os.system('sed -i "/MGcosa/c\MGcosa    0d0" powheg.input')
#  if parstage == '7':
#    os.system('sed -i "/lhrwgt_id/c\lhrwgt_id \'mm_weight\'" powheg.input')
#    os.system('sed -i "/MGcosa/c\MGcosa    -0.707107d0" powheg.input')

for i in range (1, int(numJobs)+1) :

  jobID = jobtag + '_' + str(i)

  jobname = 'run_' + jobID + '.sh'

  os.system('echo \"cd $CMSSW_BASE/src\" > %(jobname)s' % vars())
  os.system('echo \"export SCRAM_ARCH=$SCRAM_ARCH\" >> %(jobname)s' % vars())
  os.system('echo \"eval \`scramv1 runtime -sh\`\" >> %(jobname)s' % vars())
  os.system('echo \"ulimit -c 0\" >> %(jobname)s' % vars())
  os.system('echo \"cd $PWD\" >> %(jobname)s' % vars())
  os.system('echo \"export LD_LIBRARY_PATH=/vols/cms/dw515/ggh_mc/ggh-mssm/m125/CMSSW_10_2_3/biglib/slc7_amd64_gcc700:/vols/cms/dw515/ggh_mc/ggh-mssm/m125/CMSSW_10_2_3/lib/slc7_amd64_gcc700:/vols/cms/dw515/ggh_mc/ggh-mssm/m125/CMSSW_10_2_3/external/slc7_amd64_gcc700/lib:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_3/biglib/slc7_amd64_gcc700:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_3/lib/slc7_amd64_gcc700:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_3/external/slc7_amd64_gcc700/lib:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/llvm/6.0.0-ogkkac/lib64:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/gcc/7.0.0-omkpbe2/lib64:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/gcc/7.0.0-omkpbe2/lib:/usr/lib64:/cvmfs/grid.cern.ch/centos7-umd4-ui-4.0.3-1_191004/lib64:/cvmfs/grid.cern.ch/centos7-umd4-ui-4.0.3-1_191004/lib:/cvmfs/grid.cern.ch/centos7-umd4-ui-4.0.3-1_191004/usr/lib64:/cvmfs/grid.cern.ch/centos7-umd4-ui-4.0.3-1_191004/usr/lib:/vols/build/cms/dw515/LHAPDF/lib:/vols/cms/dw515/lib\" >> %(jobname)s' % vars())
  sleep=(i-1)*2
  os.system('echo \"sleep %(sleep)is\" >> %(jobname)s' % vars())
  if parstage in ['5','6','7']:
    innum = '{0:04}'.format(i)
    os.system('echo \"echo $\'%(i)i\\npwgevents-%(innum)s.lhe\' | ./pwhg_main &> run_%(jobID)s.log \" >> %(jobname)s' % vars())
    os.system('echo mv pwgevents-rwgt-%(innum)s.lhe pwgevents-%(innum)s.lhe >> %(jobname)s' % vars())
  else:
    os.system('echo \"echo %(i)i | ./pwhg_main &> run_%(jobID)s.log \" >> %(jobname)s' % vars())
  os.system('chmod +x %(jobname)s' % vars())

  qsub_command = 'qsub -e /dev/null -o /dev/null -cwd -V -q hep.q -l h_rt=3:0:0 '
  os.system(qsub_command+' '+jobname)

