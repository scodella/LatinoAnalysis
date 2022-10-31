
Productions = { 
   
   'Fall2017_nAOD_v2_94X':  {
                         'isData'       : False ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/fall17_mAOD_v1.py' ,
                         'GlobalTag'    : '94X_mc2017_realistic_v14' ,
                         'EraModifiers' : 'Run2_2017,run2_nanoAOD_94XMiniAODv2' ,
                   },     


  # ---- Relaxed loose ID / misHit / ...

   'Run2017_nAOD_v2_94X':  {
                         'isData'  : True ,
                         'jsonFile'     : '"%s/src/LatinoAnalysis/NanoGardener/python/data/certification/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"  % os.environ["CMSSW_BASE"]',
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Run2017_mAOD_v1.py' ,
                         'GlobalTag'    : '94X_mc2017_realistic_v14' ,
                         'EraModifiers' : 'Run2_2017,run2_nanoAOD_94XMiniAODv2' ,
                   },

   'Summer16_102X_nAODv4_Full2016v4': {
                         'isData'       : False ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Summer16_102X_mAODv3.py' ,
                         'GlobalTag'    : '102X_mcRun2_asymptotic_v6' ,
                         'EraModifiers' : 'Run2_2016,run2_nanoAOD_94X2016' ,
   },
   'Summer16FS_102X_nAODv4_Full2016v4': {
                         'isData'       : False ,
                         'isFastSim'    : True ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Summer16FS_102X_mAODv3.py' ,
                         'GlobalTag'    : '102X_mcRun2_asymptotic_v6' ,
                         'EraModifiers' : 'Run2_2016,run2_nanoAOD_94X2016' ,
                         'tagJEC'       : 'Spring16_25nsFastSimV1_MC', 
   },
   'Summer16FS_102X_nAODv6' : {
                         'isData'       : False ,
                         'isFastSim'    : True ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Summer16FS_102X_mAODv3.py' ,
                         'GlobalTag'    : '102X_mcRun2_asymptotic_v7' ,
                         'EraModifiers' : 'Run2_2016,run2_nanoAOD_94X2016' ,
                         'tagJEC'       : 'Summer16_FastSimV1_MC', 
   },
   'Fall17_102X_nAODv4_Full2017v4': {
                         'isData'       : False ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Fall17_102X_mAODv3.py' ,
                         'GlobalTag'    : '102X_mc2017_realistic_v6' ,
                         'EraModifiers' : 'Run2_2017,run2_nanoAOD_94XMiniAODv2' ,
   },
   'Fall17FS_102X_nAODv4_Full2017v4': {
                         'isData'       : False ,
                         'isFastSim'    : True ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Fall17FS_102X_mAODv3.py' ,
                         'GlobalTag'    : '102X_mc2017_realistic_v6' ,
                         'EraModifiers' : 'Run2_2017,run2_nanoAOD_94XMiniAODv2' ,
                         'tagJEC'       : 'Fall17_FastSimV1_MC', 
   },
   'Fall17FS_102X_nAODv6': {
                         'isData'       : False ,
                         'isFastSim'    : True ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Fall17FS_102X_mAODv3.py' ,
                         'GlobalTag'    : '102X_mc2017_realistic_v7' ,
                         'EraModifiers' : 'Run2_2017,run2_nanoAOD_94XMiniAODv2' ,
                         'tagJEC'       : 'Fall17_FastSimV1_MC', 
   },
   'Autumn18_102X_nAODv4_GTv16_Full2018v4': {
                         'isData'       : False ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Autumn18_102X_mAODv3.py' ,
                         'GlobalTag'    : '102X_upgrade2018_realistic_v16' ,
                         'EraModifiers' : 'Run2_2018,run2_nanoAOD_102Xv1' ,
   },
   'Autumn18FS_102X_nAODv4_GTv16_Full2018v4': {
                         'isData'       : False ,
                         'isFastSim'    : True ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Autumn18FS_102X_mAODv3.py' ,
                         'GlobalTag'    : '102X_upgrade2018_realistic_v16' ,
                         'EraModifiers' : 'Run2_2018,run2_nanoAOD_102Xv1' ,
                         'tagJEC'       : 'Autumn18_FastSimV1_MC', 
   },
   'Autumn18FS_102X_nAODv6': { 
                         'isData'       : False ,
                         'isFastSim'    : True ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Autumn18FS_102X_mAODv3.py' ,
                         'GlobalTag'    : '102X_upgrade2018_realistic_v20' ,
                         'EraModifiers' : 'Run2_2018,run2_nanoAOD_102Xv1' ,
                         'tagJEC'       : 'Autumn18_FastSimV1_MC', 
   },
   # UL
   'Spring21UL16FS_106X_nAODv9_Full2016v9': {
                         'isData'       : False ,
                         'isFastSim'    : True ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Spring21UL16FS_106X_mAODv2.py' ,
                         'GlobalTag'    : '106X_mcRun2_asymptotic_v17' ,
                         'EraModifiers' : 'Run2_2016,run2_nanoAOD_106Xv2' ,
                         #'tagJEC'       : '',
   },
   'Spring21UL17FS_106X_nAODv9_Full2016v9': {
                         'isData'       : False ,
                         'isFastSim'    : True ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Spring21UL17FS_106X_mAODv2.py' ,
                         'GlobalTag'    : '106X_mc2017_realistic_v9' ,
                         'EraModifiers' : 'Run2_2017,run2_nanoAOD_106Xv2' ,
                         #'tagJEC'       : '',
   },
   'Spring21UL18FS_106X_nAODv9_Full2016v9': {
                         'isData'       : False ,
                         'isFastSim'    : True ,
                         'samples'      : 'LatinoAnalysis/NanoProducer/python/samples/Spring21UL18FS_106X_mAODv2.py' ,
                         'GlobalTag'    : '106X_upgrade2018_realistic_v16_L1v1' ,
                         'EraModifiers' : 'Run2_2018,run2_nanoAOD_106Xv2' ,
                         #'tagJEC'       : '',
   },

}
