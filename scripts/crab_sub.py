from CRABClient.UserUtilities import config
config = config()

config.General.requestName     = 'ggh_mXHMASSX_XCONTRIBX_GENSIM'
config.General.workArea        = 'ggh_mXHMASSX_XCONTRIBX_GENSIM'
config.General.transferOutputs = True
config.General.transferLogs    = True
#config.JobType.numCores = 4
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName   = 'gensim.py'

config.JobType.allowUndistributedCMSSW = True
config.Data.outputPrimaryDataset = 'ggh_mXHMASSX_XCONTRIBX_GENSIM'
config.Data.inputDBS             = 'global'
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 1000
config.Data.totalUnits           = 200000
config.Data.outLFNDirBase        = '/store/user/dwinterb/ggH_MC/ggh_mXHMASSX_XCONTRIBX_GENSIM/'
config.Data.publication          = True
config.Data.outputDatasetTag     = 'ggh_mXHMASSX_XCONTRIBX_GENSIM'
config.JobType.inputFiles = ['ggh_powheg_mXHMASSX_XCONTRIBX.tar.gz']


config.Site.storageSite = 'T2_UK_London_IC'
