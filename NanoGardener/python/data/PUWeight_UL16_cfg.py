####################### PU UL16 Weight CFG ##################################

PUCfg = {

 'Full2016v8HIPM' : {
                   'srcfile'     : "auto" ,
                   'targetfiles' : { '1-3' : 'LatinoAnalysis/NanoGardener/python/data/PUweights/2016/UL2016HIPM_PU.root' ,
                                   } ,
                   'srchist'     : "pileup"   ,
                   'targethist'  : "pileup"   ,
                   'name'        : "puWeightHIPM" ,
                   'norm'        : True       ,
                   'verbose'     : False      ,
                   'nvtx_var'    : "Pileup_nTrueInt" ,
                   'doSysVar'    : True ,
                } ,


 'Full2016v8noHIPM' : {
                   'srcfile'     : "auto" ,
                   'targetfiles' : { '4-7' : 'LatinoAnalysis/NanoGardener/python/data/PUweights/2016/UL2016noHIPM_PU.root' ,
                                   } ,
                   'srchist'     : "pileup"   ,
                   'targethist'  : "pileup"   ,
                   'name'        : "puWeightnoHIPM" ,
                   'norm'        : True       ,
                   'verbose'     : False      ,
                   'nvtx_var'    : "Pileup_nTrueInt" ,
                   'doSysVar'    : True ,
                } ,

}


