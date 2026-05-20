from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'SMP-Run3Summer23wmLHEGS-00186-NanoGEN'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '../configs/SMP-Run3Summer23wmLHEGS-00186_NanoGEN_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 5000

config.Data.outputPrimaryDataset = 'SMP-Run3Summer23wmLHEGS-00186'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 100
NJOBS = 5000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.outLFNDirBase = '/store/user/YOUR_USERNAME/'
config.Data.publication = False
config.Data.outputDatasetTag = 'Run3Summer23_NanoGEN_v1'

config.Site.storageSite = 'T2_CH_CERN'
