#!/usr/bin/env python
import os
import subprocess
import math
from optparse import OptionParser
import optparse
import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM

mcm = McM(dev=True)
mcmurl = "https#//cms-pdmv.cern.ch/mcm/requests?prepid=PREPID&page=0&shown=127"
testcolor='95m'
if 'pmatorra' in os.environ.get('USER'):
    cmssw_directory= '/afs/cern.ch/work/p/pmatorra/private/CMSSW_10_6_19/'
    errorcolor = '93m'
    warningcolor = '96m'
    okcolor = '92m'
else:
    cmssw_directory = '/afs/cern.ch/work/s/scodella/SUSY/CMSSW_10_6_19_patch2/'
    errorcolor = '93m'
    warningcolor = '96m'
    okcolor = '92m'

gardening_directory = 'src/LatinoAnalysis/NanoGardener/python/framework/samples/'
production_directory = 'src/LatinoAnalysis/NanoProducer/python/samples/'

campaigns = { 'UL16preVPF' : { 'MC'   : { 'AODSIM' : 'RunIISummer20UL16RECOAPV', 'MINIAODSIM' : 'RunIISummer20UL16MiniAODAPVv2', 'NANOAODSIM' : 'RunIISummer20UL16NanoAODAPVv9', 'GEN' : 'RunIISummer20UL16*GENAPV-' },
                            'FS'   : { 'AODSIM' : '',                         'MINIAODSIM' : '',                            'NANOAODSIM' : ''                             , 'GEN' : ''                         }, },
              'UL16postVPF'  : { 
                          'MC'   : { 'AODSIM' : 'RunIISummer20UL16RECO-', 'MINIAODSIM' : 'RunIISummer20UL16MiniAODv2-', 'NANOAODSIM' : 'RunIISummer20UL16NanoAODv9', 'GEN' : 'RunIISummer20UL16*GEN-' },    
                          'FS'   : { 'AODSIM' : '',                       'MINIAODSIM' : '',                          'NANOAODSIM' : ''                          , 'GEN' : ''                      }, },
              'UL16'  : { 'Data' : { 'AOD'    : '21Feb2020_UL2016-',      'MINIAOD'    : '21Feb2020_UL2016-',         'NANOAOD'    : 'UL2016_MiniAODv1_NanoAODv2'  }, },
              'UL17'  : { 'Data' : { 'AOD'    : '09Aug2019_UL2017-',      'MINIAOD'    : '09Aug2019_UL2017-',         'NANOAOD'    : 'UL2017_MiniAODv1_NanoAODv2'                                  },             
                          'MC'   : { 'AODSIM' : 'RunIISummer20UL17RECO',   'MINIAODSIM' : 'RunIISummer20UL17MiniAOD',   'NANOAODSIM' : 'RunIISummer20UL17NanoAODv2',  'GEN' : 'RunIISummer20UL17*GEN'  },
                          'FS'   : { 'AODSIM' : '',                       'MINIAODSIM' : '',                          'NANOAODSIM' : ''                          , 'GEN' : ''                      }, }, 
              'UL18'  : { 'Data' : { 'AOD'    : '12Nov2019_UL2018-',      'MINIAOD'    : '12Nov2019_UL2018-',         'NANOAOD'    : 'UL2018_MiniAODv1_NanoAODv2'                                  },             
                          'MC'   : { 'AODSIM' : 'RunIISummer20UL18RECO',  'MINIAODSIM' : 'RunIISummer20UL18MiniAOD',  'NANOAODSIM' : 'RunIISummer20UL18NanoAODv2', 'GEN' : 'RunIISummer20UL18*GEN'  },
                          'FS'   : { 'AODSIM' : '',                       'MINIAODSIM' : '',                          'NANOAODSIM' : ''                          , 'GEN' : ''                      }, }, 
            }

#Get the latest version if requested
def renewSampleFile(filename):
    os.system('wget --output-file="logs.txt" "https://docs.google.com/spreadsheets/d/1ABl2p2uwr2EfEbolBEVNcKb_fIXigYY9sqCRT8XIi1Q/export?format=csv&gid=1318927481" -O "downloaded_content.csv"')
    with open("downloaded_content.csv", "r") as file_input:
        with open(filename, "w") as output:
            isHeader=True
            for i,line in enumerate(file_input):
                if 'Total' and 'Samples' in line.split(',')[0]: #More refined feature can be added, but works now
                    isHeader=False
                    continue
                
                if isHeader is False:
                    if line.startswith(",,,"): continue
                    output.write(line)
        print line

#Read Csv file
def readSampleFile(filename):
    samhere=[]
    with open(filename) as f:
        for row in f:
            samhere.append(row.split(",")[0])
    return samhere

def substringinlist(sample_list,substring):
    inlist=set() #defined so that duplicates are removed
    #loop to find samples with the substring
    for item in sample_list:
        if (substring in item) : 
            inlist.add(item)
            #print "satisfies", substring, item
    return list(inlist)

def getEventsFromDAS(dassample): 

    nEvents = -1
    summaryDAS = subprocess.check_output('dasgoclient -query=\"instance=prod/global summary dataset='+dassample+'\"', shell=True)
    for dasInfo in summaryDAS.split(','):
        if 'nevents' in dasInfo:
            nEvents = dasInfo.split(':')[1]
    return nEvents

def getReadableNumber(rawstringnumber):
    rawnumber = int(rawstringnumber)
    if rawnumber<1000: return rawstringnumber
    elif rawnumber<10000: return str(round(float(rawstringnumber)/1000.,1))+'K'
    elif rawnumber<1000000: return str(round(float(rawstringnumber)/1000.,0)).replace('.0','')+'K'
    elif rawnumber<10000000: return str(round(float(rawstringnumber)/1000000.,1))+'M'
    else: return str(round(float(rawstringnumber)/1000000.,0)).replace('.0','')+'M'

def isBackupSample(sampleName):
    for backupSample in [ 'WJetsToLNu-LO', 'WJetsToLNu_HT', 'tZq_ll', 'ttHToNonbb', 'TTJetsDilep', 'HZJ' ]:
        if backupSample in sampleName:
            return True
    return False

# Main
if __name__ == '__main__':

    # Input parameters
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('-d', '--directory' , dest='directory' , help='CMSSW directory' , default=cmssw_directory)
    parser.add_option('-s', '--samplefile', dest='samplefile', help='Sample file'     , default='Run2016_102X_nAODv6')
    parser.add_option('-c', '--campaign'  , dest='campaign',   help='Campaign'        , default='UL16')
    parser.add_option('-t', '--tier'      , dest='tier',       help='Tier'            , default='nanoAOD')
    parser.add_option('-o', '--outputfile', dest='outputfile', help='Output file'     , default='test')
    parser.add_option('-m', '--mute'      , dest='mute'      , help='mute'            , default=False, action='store_true')
    parser.add_option('-l', '--list'      , dest='list'      , help='List in csv'     , default=False, action='store_true')
    parser.add_option('-n', '--newcsv'    , dest='newcsv'    , help='Download new csv', default=False, action='store_true')
    
    (opt, args) = parser.parse_args()
 
    csvfile = "Summer20ULPlanning.csv"
    if opt.newcsv: renewSampleFile(csvfile)
    csvsamples = readSampleFile(csvfile)

    if opt.samplefile==opt.outputfile:
        print 'Error: overwriting input file', opt.samplefile
        exit()
    else:
        opt.outputfile = opt.outputfile.replace('.py', '')
    run2Samples=False
    isData=False

    verbose = not opt.mute

    if 'run2' in opt.campaign:
        campaign_years=campaigns.keys()
        run2Samples=True
        if 'data' in opt.campaign: isData=True
    elif opt.campaign in campaigns:
        campaign_years=[opt.campaign]
    else:
        print 'Error: missing information for campaign', opt.campaign
        exit()
    
    for campaign_year in campaign_years:
        if run2Samples:
            if   '16' in campaign_year: 
                if isData: opt.samplefile='Run2016_102X_nAODv6'
                else:      opt.samplefile='Summer16_susy_102X_nAODv6'
            elif '17' in campaign_year: 
                if isData: opt.samplefile='Run2017_102X_nAODv6'
                else:      opt.samplefile='fall17_susy_102X_nAODv6'
            elif '18' in campaign_year:
                if isData: opt.samplefile='Run2018_102X_nAODv6'
                else :     opt.samplefile='Autumn18_susy_102X_nAODv6'
            print campaign_year
        if 'Run' in opt.samplefile:
            Sim = '' 
            if "VPF" in opt.campaign: 
                print "Data doesn't have pre/post vpf"
                answer = raw_input("did you mean -c UL16? ").lower()
                if "y" in answer:
                    print "Switching to UL16"
                    campaign_year= 'UL16'
                else:
                    print "Exiting..."
                    exit()
            print "Campaign year", campaign_year, campaigns[campaign_year].keys()
            campaign = campaigns[campaign_year]['Data']
            isData=True
        else:      
            isData=False
            Sim  = 'SIM'
            if 'FS_' in opt.samplefile:
                campaign = campaigns[campaign_year]['FS']
            else:
                campaign = campaigns[campaign_year]['MC'] 
        
        tiers = [ ]
        for tier in [ 'NANOAOD', 'MINIAOD', 'AOD' ]:
            if opt.tier!='miniAOD' or tier!='NANOAOD': 
                tiers.append(tier+Sim)

        sample_directory = production_directory if opt.tier=='miniAOD' else gardening_directory 

        exec(open(opt.directory+sample_directory+opt.samplefile.replace('.py', '')+'.py').read())

        if opt.outputfile=='test' and ('UL' in opt.campaign or 'run2' in opt.campaign):
            opt.outputfile = opt.samplefile.replace('102X_nAODv6', '106X_nAODv8').replace('.py', '')
            opt.outputfile = opt.outputfile.replace('Summer16','Summer20UL16').replace('fall17','Summer20UL17').replace('Autumn18','Summer20UL18')
            if 'preVPF' in opt.campaign:
                opt.outputfile = opt.outputfile.replace('16', '16preVPF')
            elif 'postVPF' in opt.campaign:
                opt.outputfile = opt.outputfile.replace('16', '16postVPF')

            print opt.samplefile
        OutputSamples = { }
        print "OUTPUT FILE",opt.outputfile
        #testout=opt.outputfile+'.py'
        if opt.list:
            outList = open(opt.outputfile+'.csv' , 'w')
        else: 
            writeList = open(opt.outputfile+'.py','w')
            writeList.write("Samples = {} \n\n")

        print opt.tier, campaign_year
        thistier=opt.tier.upper()+Sim
        print "CAMPAIGN:", campaign[thistier].upper(), thistier
        lastSampleInit = ''
        for sample in sorted (Samples.keys()):
            #print sample
            #if ("WWTo2L" not in sample): continue
 
            nEvents, nOriginalEvents = '-1', getEventsFromDAS(Samples[sample][opt.tier])
         
            process = Samples[sample][opt.tier].split('/')[1]
            period = '' if Sim=='SIM' else Samples[sample][opt.tier].split('/')[2].split('-')[0].split('_')[0]

            status = 'Missing:'

            if verbose: print '\n', 'Original process name', process, period, '(original events =', nOriginalEvents, ')'

            if not isData:
                process = process.replace('_PSweights', '')
                if 'Tune' not in process: process = process.replace('13TeV', '*13TeV')
                process = process.replace('pythia8_TuneCP5', 'pythia8')
                process = process.replace('13TeV_powheg_pythia', '13TeV*powheg*pythia')
                process = process.replace('TuneCUETP8M1', 'TuneCP5')
                process = process.replace('TuneCUETP8M2', 'TuneCP5')         
                process = process.replace('_ttHtranche3', '')
                process = process.replace('DYJetsToLL_M-5to50', 'DYJetsToLL_M-4to50')
                process = process.replace('_ext1', '')
                process = process.replace('_NNPDF31_', '_')
                process = process.replace('_13TeV_powheg_jhugen724_pythia8', '_13TeV*powheg*jhugen727*pythia8')
                process = process.replace('_13TeV_powheg_jhugen714_pythia8', '_13TeV*powheg*jhugen727*pythia8')
                if 'UL16' in campaign_year:
                    if 'GluGluToContinToZZ' in process:
                        process = process.replace('13TeV_TuneCP5_MCFM701_pythia8', 'TuneCP5_13TeV-mcfm701-pythia8')
                        process = process.replace('13TeV_MCFM701_pythia8', 'TuneCP5_13TeV-mcfm701-pythia8')
                    elif 'DYJetsToLL_M-50_HT' in process:
                        process = process.replace('TuneCP5', 'TuneCP5_PSweights')
                    elif 'HWminusJ_HToWW' in process or 'HWplusJ_HToWW' in process or 'HZJ_HToWWTo2L2Nu' in process:
                        process = process.replace('_M125_', '_M-125_*')
                elif campaign_year:
                    if 'GluGluToContinToZZ' in process: 
                        process = process.replace('13TeV_TuneCP5_MCFM701_pythia8', 'TuneCP5_13TeV-mcfm701-pythia8')
                        process = process.replace('13TeV_MCFM701_pythia8', 'TuneCP5_13TeV-mcfm701-pythia8')
                    elif 'ST_t-channel_antitop_5f_' in process or 'ST_t-channel_antitop_5f_' in process: 
	                process = process.replace('_5f_', '_5f_InclusiveDecays_')
                    elif 'DYJetsToLL_M-50_HT' in process:
                        process = process.replace('_TuneCP5_', '_TuneCP5_PSweights_')
                    elif 'HWminusJ_HToWW' in process or 'HWplusJ_HToWW' in process or 'HZJ_HToWWTo2L2Nu' in process:
                        process = process.replace('_M125_', '_M-125_*')  
                elif campaign_year=='UL18':
                    if 'GluGluToContinToZZ' in process:
                        process = process.replace('13TeV_TuneCP5_MCFM701_pythia8', 'TuneCP5_13TeV-mcfm701-pythia8')
                        process = process.replace('13TeV_MCFM701_pythia8', 'TuneCP5_13TeV-mcfm701-pythia8')
                    elif 'DYJetsToLL_M-50_HT' in process:
                        process = process.replace('_TuneCP5_', '_TuneCP5_PSweights_')
                    elif 'DYJetsToLL_M-4to50_HT' in process:
                        process = process.replace('_TuneCP5_PSweights_', '_TuneCP5_')
                        process = process.replace('_TuneCP5_PSWeights_', '_TuneCP5_')
                    elif 'GluGluZH_HToWWTo2L2Nu_' in process:
                        process = process.replace('_M125_', '_M*125_').replace('pythia8', 'pythia8*')
                    elif 'HWminusJ_HToWW' in process or 'HWplusJ_HToWW' in process or 'HZJ_HToWWTo2L2Nu' in process:
                        process = process.replace('_M125_', '_M-125_*')
                    elif 'tZq_ll_4f' in process:
                        process = process.replace('13TeV-madgraph-pythia8', '13TeV-amcatnlo-pythia8')
<<<<<<< HEAD
                process = process.replace('_5f_Tune', '_5f_InclusiveDecays_Tune')
=======
                    elif 'WWZ_Tune' in process:
                        process = process.replace('WWZ_Tune', 'WWZ_4F_Tune')
                process = process.replace('_5f_Tune', '_5f_InclusiveDecays_Tune')
                if 'ZZTo4L' in process:
                    process = process.replace('ZZTo4L_*13TeV*powheg*pythia8', 'ZZTo4L_T*13TeV*powheg*pythia8')
>>>>>>> upstream/UL_worker
                if 'ST_tW' in process:
                    process = process.replace('InclusiveDecays', 'NoFullyHadronicDecays')
                    process = process.replace('inclusiveDecays', 'NoFullyHadronicDecays')
            if verbose: print 'Corrected process name', process, period

            datasetsFound = [ ] 
            parentsFound = [ ]

            for tier in tiers:

                if campaign[tier]=='':
                    print 'Error: missing information for campaign', campaign, 'tier', tier
                    exit()

                query = '\"instance=prod/global dataset=/'+process+'/'+period+'*'+campaign[tier]+'*/'+tier+'\"'
                query_output = subprocess.check_output('dasgoclient -query='+query, shell=True)
                #print query
                for line in query_output.split('\n'):
                    if opt.tier.upper() in line:
                        datasetsFound.append(line)
                    elif '/' in line:
                        parentsFound.append(line)

            datasetFound = ''
            if period!='': period = '_'+period 
            if len(datasetsFound)==1:
                datasetFound = datasetsFound[0]
                status = 'NanoAODv2 ready:, ' + datasetFound
                nEvents = getEventsFromDAS(datasetFound)
                if verbose:
                    print '\033['+okcolor + 'Dataset found for sample', process+period, 'in campaign', campaign[thistier], '-->', datasetFound + '\033[0m'
            elif len(datasetsFound)>1:
                if verbose: 
                    print '\033['+okcolor + 'Warning: multiple datasets found for sample', process+period, 'in campaign', campaign[thistier], '-->', datasetsFound, '\033[0m'
                version = 0
                saveset = ''
                for dataset in datasetsFound:  
                    if "FlatPU" in dataset: continue
                    if '_ext' in dataset: continue # To be improved, by chosing the dataset with larger statistics
                    #print "DATASET", dataset, dataset.split('-v')
                    if len(dataset.split('ver'))>1: ver = 'ver'
                    else:  ver = 'v'
                    if len(dataset.split(ver))>1: 
                        #print dataset.split(ver)[1], ver,  dataset.split(ver)[1][0]
                        if (version < int(dataset.split(ver)[1][0])):
                            #print "new sample", dataset, version
                            saveset=dataset
                            version = int(dataset.split(ver)[1][0])
                        elif (version == int(dataset.split(ver)[1][0])):
                            print "WARNING: "+ dataset+" and "+saveset+" have the same version" 
                    else: print "TRY DIFFERENT CODING" #May have to be updated in the future
                if verbose: print 'Dataset picked for sample', process+period, 'in campaign', campaign[thistier], '-->', saveset
                datasetFound = saveset
                status       = 'NanoAODv2 ready:, ' + saveset
                nEvents = getEventsFromDAS(datasetFound)
            else:   
                if verbose: 
                    print 'Warning: no dataset found for sample', process+period, 'in tier', opt.tier, 'for campaign', campaign[thistier] 
                if len(parentsFound)>0:
                    for parent in parentsFound:
                        if 'MINIAOD' in parent: 
                            status = 'MiniAOD ready:, ' + parent
                            nEvents = getEventsFromDAS(parent)
                            miniquery = 'dataset_name='+parent.split('/')[1]+'&prepid=*'+parent.split('/')[2].split('-')[0]+'*'
                            minirequests = mcm.get('requests', None, miniquery)
                            for minirequest in minirequests:
                                if len(minirequest['output_dataset'])==0: continue
                                if minirequest['output_dataset'][0]==parent:
                                    for chainrequest in minirequest['member_of_chain']:
                                        if 'NanoAODv2' in chainrequest:
                                            status = 'NanoAODv2 request in chain:' + mcmurl.replace('requests?', 'chained_requests?').replace('PREPID', chainrequest)
                                            chainedrequests = mcm.get('chained_requests', None, 'prepid='+chainrequest)
                                            for chainedrequest in chainedrequests:
                                                print chainedrequest['chain']
                                                for requestinchain in chainedrequest['chain']:
                                                    if 'NanoAODv2' in requestinchain:
                                                        nanorequests = mcm.get('requests', None, 'prepid='+requestinchain)
                                                        for nanorequest in nanorequests:
                                                            status = 'NanoAODv2 request ' + nanorequest['status'] + ':' + mcmurl.replace('PREPID', nanorequest['prepid'])
                        elif 'MiniAOD' not in status and 'NanoAODv2' not in status:
                            status = 'AOD ready:, ' + parent
                            nEvents = getEventsFromDAS(parent)
                    if verbose:
                        print '\033['+okcolor + '        available parents are', parentsFound, '' + '\033[0m'

                elif not isData:
                    
                    mcm_status = 0

                    mcm_query = 'dataset_name='+process+'&prepid=*'+campaign['GEN']+'*'
                    #print mcm_query
                    requests = mcm.get('requests', None, mcm_query)
                    #print mcm_query, requests
                    if len(requests)>0:
                        status = 'McM:, '
                        for request in requests:

                            if request['status']=='new': mcm_status = 1
                            elif request['status']=='validation': mcm_status = 2
                            elif request['status']=='defined': mcm_status = 3
		            elif request['status']=='approved': mcm_status = 4
                            elif request['status']=='submitted': mcm_status = 5                         

                            status += request['prepid'] + ' / ' + request['status'] + ' / ' + str(request['total_events']) + ' - '

                            if verbose:
                                textcolor = okcolor if mcm_status==5 else warningcolor
                                print '\033['+textcolor + 'Request', request['prepid'], 'for sample', request['dataset_name'], 'in status', request['status'] + '\033[0m'

                    if mcm_status<1:

                        if verbose:
                            print 'Warning: no request found for sample', process, 'in McM campaign', campaign['GEN'], 'check PC planning'

                        incsv=substringinlist(csvsamples,process)
                        if   (len(incsv)==0) :
                            incsvsample = substringinlist(csvsamples,sample)
                            print "---------->", process, sample, "\n", incsvsample
                            
                            if len(incsvsample)==0: 
                                print '\033['+errorcolor + 'Warning: sample', process, 'not in the planned production campaign' + '\033[0m'
                            else:
                                status = 'Planned alternative: '
                                sample_options = ['-powheg','-pythia8', '_TuneCP5']
                                skim_process = process
                                in_skim_proc = []
                                best_altern  = ''
                                notincommon  = 2*len(sample_options)
                                print "sample and process", sample, process
                                
                                #Cover from cases from TTSemilepton->Semileptonic or incorrectly read *
                                if sample not in process or "*" in process: 
                                    maxopts = 0
                                    if len(incsvsample)==1: bestcandidate=incsvsample[0]
                                    else: bestcandidate=''
                                    for alt_sample in incsvsample:
                                        #print sample, alt_sample, process, bool(sample in alt_sample), bool(process in alt_sample)

                                        if sample  not in alt_sample: continue
                                        nopts = 0
                                        for sample_option in sample_options:
                                            #print sample_option, incsvbool(sample_option in incsvsample)
                                            if sample_option in alt_sample: nopts+=1
                                        if nopts> maxopts:
                                            maxopts       = nopts
                                            bestcandidate = alt_sample
                                    print alt_sample, maxopts, len(sample_options)

                                    print '\033['+warningcolor + 'Warning: sample', process, 'not in the planned production campaign,',
                                    if maxopts==len(sample_options): print '\033['+testcolor +"but the sample ", bestcandidate, "should be equivalent"
                                    else: print "with the sample being the closest", bestcandidate
                                    print "\033[0m"
                                
                                #If many, check which one resembles closer to the input parametre
                                else:
                                    for sample_option in sample_options:
                                        if(sample_option in skim_process): 
                                            skim_process = skim_process.replace(sample_option,'')
                                            in_skim_proc.append(sample_option)
                                    for alt_sample in incsvsample:
                                        status     += alt_sample + ' - '
                                        skim_alt    = alt_sample
                                        in_skim_alt = []
                                        for sample_option in sample_options:
                                            if sample_option in skim_alt:
                                                skim_alt = skim_alt.replace(sample_option,'')
                                                in_skim_alt.append(sample_option)
                                        not_inproc=[x for x in in_skim_proc+in_skim_alt if x not in in_skim_proc]
                                        not_inalt =[x for x in in_skim_proc+in_skim_alt if x not in in_skim_alt] #Both could be combined

                                        if skim_process in skim_alt:
                                            if notincommon> len(not_inproc)+len(not_inalt):
                                                notincommon = len(not_inproc)+len(not_inalt)
                                                best_altern = alt_sample
                                            elif notincommon == len(not_inproc)+len(not_inalt): best_altern+= alt_sample

                                    print '\033['+warningcolor + 'Warning: sample', process, 'not in the planned production campaign,',
                                    if notincommon<2*len(sample_options):
                                        if notincommon==0: print '\033['+testcolor +"but the sample "+ best_altern+ " should be equivalent"
                                        else: print"should be similar with the exception of "+ not_inproc+ "not in the process name, and "+ not_inalt+ " not in the CSV"
                                    else: print 'but alternative samples are there:', incsvsample
                                    print '\033[0m',
                                    #if len(incsvsample)>1:exit()
                        elif (len(incsv)>1)  : 
                            status = 'Planned:'
                            if verbose: print '\033['+testcolor+"MULTIPLE OPTIONS AVAILABLE FOR THE CSV FILE", ' \033[0m', incsv, set(incsv), len(set(incsv))
                            exit()
                        elif verbose: 
                            status = 'Planned:'
                            print '\033['+warningcolor + 'SAMPLES IN CSV:', process, incsv, ' \033[0m'
                            #exit()
                            
            line='\n'
            for data in datasetFound.split('/'): # Isn't this useless given that later we have: elif "_ext" in datasetFound: ?
                if 'ext' in data:
                    datasetFlag='_extN' 
                    #print "................................\n", datasetFound
                    continue
            
            status = status.replace(':,',':')
            print "STATUS", status
            if len(datasetFound) == 0 : 
                datasetFlag = ''
                line+='#'
            elif isData: datasetFlag = '_'+datasetFound.split('/')[2]
            elif "_ext" in datasetFound:#.split('/')[2]: 
                datasetFlag = "_ext"+datasetFound.split('/')[2].split("_ext")[1].split('-')[0]#+Samples[sample][opt.tier].split("_ext")[1].split("-")[0]
                #print '\033['+testcolor+ " REEEMOVING THE _EXT", datasetFlag, "\033[0m"
                #exit()
            else: 
                datasetFlag = ''#'_'+Samples[sample][opt.tier].split('/')[2]
                #print "##############\nDATASET FLAG\n", datasetFlag,"\nsamples[sample]",  Samples[sample][opt.tier], "\nprocess", process, "\nsample", sample, "\n##############"

                #if 'TTTo2L2Nu' in sample : 
                #    print "#################################\nFLAG#####", Samples[sample][opt.tier], process, sample
                    #exit()
            if 'ST_tW' in process and 'NoFullyHadronicDecays':
                datasetFlag += '_nohad'

            if opt.list:
                statuslist = status.split(':')
                nMeventsOriginal = getReadableNumber(nOriginalEvents)
                if 'McM' not in status:
                    nMevents = getReadableNumber(nEvents)
                    eventString = '?/'+nMeventsOriginal
                    if nEvents!='-1':
                        eventString = nMevents + '/' + nMeventsOriginal + '('+str(int(100.*float(nEvents)/float(nOriginalEvents)))+'%)'
                    outList.write(process + ',' + statuslist[0] + ',' + eventString + ',' + statuslist[1].replace('https#','https:') + '\n')
                else: 
                    nmcm = 0
                    for mcmRequest in statuslist[1].split(' - '):
                        if nmcm<(len(statuslist[1].split(' - '))-1):
                            nMevents = getReadableNumber(mcmRequest.split(' / ')[2])
                            eventString = nMevents + '/' + nMeventsOriginal + '('+str(int(100.*float(mcmRequest.split(' / ')[2])/float(nOriginalEvents)))+'%)'
                            processString = process if nmcm==0 else ' '
                            outList.write(processString + ',McM: ' + mcmRequest.split(' / ')[1] + ',' + eventString + ',' + mcmurl.replace('PREPID', mcmRequest.split(' / ')[0].replace(' ','')).replace('https#','https:') + '\n')
                            nmcm += 1
            else:
                sampleName = process if Sim=='' else sample.replace('_newpmx','').replace('_PSWeights', '').split('_ext')[0]
                sampleName += datasetFlag # -> to be refined
                #print "Samplename", sampleName
                OutputSamples[sampleName] = { }
                OutputSamples[sampleName][opt.tier] = datasetFound
                line+="Samples[\'"+sampleName+"\'] \t = {\'"+opt.tier+"\': \'"+datasetFound+"\'}"
                if "#" not in line: print "Add to line", line
                if sampleName[0:2]!=lastSampleInit:
                    writeList.write('\n')
                    lastSampleInit = sampleName[0:2]
                if isBackupSample(sampleName):
                    line = line.replace('Samples', '#Samples') 
                writeList.write(line)
            
        if lastSampleInit!='':
            writeList.write('\n')

