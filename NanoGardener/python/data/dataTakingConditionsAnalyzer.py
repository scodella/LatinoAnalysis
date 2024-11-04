#!/usr/bin/env python3
import os
import sys
import ROOT
import math
import json
import csv
import optparse

args=sys.argv

minBiasXsec = { 'Run2' : { 'pileup' : '69200', 'pileup_minus' : '66017', 'pileup_plus' : '72383' },
                'Run3' : { 'pileup' : '80000', 'pileup_minus' : '76320', 'pileup_plus' : '83680' },
               }

DirectoryDQM = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/'
WebCAF = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/'

yearsInfos  = { 'UL2016' : { 'Run' : 'Run2', 'runs' : [ 272007, 284044 ], 'numPileupBins' : '100',
                             'jsonFile'    : DirectoryDQM+'Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt', 
                             'pileupFile'  : DirectoryDQM+'Collisions16/13TeV/PileUp/pileup_latest.txt',
                             'normtagFile' : '/afs/cern.ch/user/l/lumipro/public/Normtags/normtag_BRIL.json' },
                'UL2017' : { 'Run' : 'Run2', 'runs' : [ 297020, 306462 ], 'numPileupBins' : '100',
                             'jsonFile'    : DirectoryDQM+'Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt',
                             'pileupFile'  : DirectoryDQM+'Collisions17/13TeV/PileUp/pileup_latest.txt',
                             'normtagFile' : '/afs/cern.ch/user/l/lumipro/public/Normtags/normtag_BRIL.json' },
                'UL2018' : { 'Run' : 'Run2', 'runs' : [ 315252 , 325175 ], 'numPileupBins' : '100',
                             'jsonFile'    : DirectoryDQM+'Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt',
                             'pileupFile'  : DirectoryDQM+'Collisions18/13TeV/PileUp/pileup_latest.txt',
                             'normtagFile' : '/afs/cern.ch/user/l/lumipro/public/Normtags/normtag_BRIL.json' },
                '2022'   : { 'Run' : 'Run3', 'runs' : [ 355100, 362760 ], 'numPileupBins' : '100',
                             'jsonFile'    : WebCAF+'Collisions22/Cert_Collisions2022_355100_362760_Golden.json',
                             'pileupFile'  : '/afs/cern.ch/user/s/smitra/public/xBTV/pileup_JSON.txt',
                             'normtagFile' : '/afs/cern.ch/user/l/lumipro/public/Normtags/normtag_BRIL.json' },
                '2023'   : { 'Run' : 'Run3', 'runs' : [ 366442, 370790 ], 'numPileupBins' : '100',
                             'jsonFile'    : WebCAF+'Collisions23/Cert_Collisions2023_366442_370790_Golden.json',
                             'pileupFile'  : WebCAF+'Collisions23/PileUp/BCD/pileup_JSON.txt',
                             'normtagFile' : '/afs/cern.ch/user/l/lumipro/public/Normtags/normtag_BRIL.json' },
               }

runPeriods = { '2016' : { '2016B'   : [ 272007,   275376 ],
                          '2016C'   : [ 275657,   276283 ],
	                      '2016D'   : [ 276315,   276811 ],
                          '2016E'   : [ 276831,	  277420 ],
                          '2016F'   : [ 277772,   278808 ],
                          '2016G'   : [ 278820,   280385 ],
                          '2016H'   : [ 280919,	  284044 ], }, 
               '2022' : { '2022CD'  : [ 355794,   359021 ],
                          '2022EFG' : [ 359022,   362760 ], },
               '2023' : { '2023B'   : [ 366365,   367079 ],
                          '2023C'   : [ 367080,   369802 ], 
                          '2023BC'  : [ 366365,   369802 ],
                          '2023D'   : [ 369803,   372415 ], },
              }
runPeriods['UL2016'] = runPeriods['2016']
runPeriods['UL2018'] = { '2018A'   : [ 315252 , 319076 ], '2018B' : [ 319077 , 325175 ] }

def brilcalcSetup():

    return 'source /cvmfs/cms-bril.cern.ch/cms-lumi-pog/brilws-docker/brilws-env'
    #brilcalcSetupList = [ 'export LD_LIBRARY_PATH=/afs/cern.ch/cms/lumi/brilconda-1.1.7/root/lib' ]
    #brilcalcSetupList.append('export PYTHONPATH=/afs/cern.ch/cms/lumi/brilconda-1.1.7/root/lib')
    #brilcalcSetupList.append('export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH')
    #brilcalcSetupList.append('export ROOTSYS=/afs/cern.ch/cms/lumi/brilconda-1.1.7/root')
    #brilcalcSetupList.append('export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH')
    #brilcalcSetupList.append('pip uninstall brilws -y')
    #brilcalcSetupList.append('pip install --install-option="--prefix=$HOME/.local" brilws')
    #return ' ; '.join(brilcalcSetupList)

def loadJSON(jsonFile):

    if 'http' in jsonFile:
        jsonFileLocal = './'+jsonFile.split('/')[-1]
        if not os.path.isfile(jsonFileLocal): os.system('wget '+jsonFile)
        jsonFile = jsonFileLocal

    return json.load(open(jsonFile, 'r'))

if __name__ == '__main__':

    # Input parameters
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--action'          , dest='action'          , help='Action to be performed'         , default='lumi')
    parser.add_option('--years'           , dest='years'           , help='Years'                          , default='Run3')
    parser.add_option('--periods'         , dest='periods'         , help='Periods'                        , default='All')
    parser.add_option('--hltPaths'        , dest='hltPaths'        , help='HLT paths'                      , default='')
    parser.add_option('--outputDir'       , dest='outputDir'       , help='Output directory'               , default='./')
    parser.add_option('--lumiunit'        , dest='lumiunit'        , help='Luminosity unit'                , default='pb')
    parser.add_option('--readPS'          , dest='readPS'          , help='Do not redo prescale files'     , default=False, action='store_true')
    parser.add_option('--saveJSON'        , dest='saveJSON'        , help='Save prescales in json format'  , default=False, action='store_true')
    parser.add_option('--mergePS'         , dest='mergePS'         , help='Merge prescales json files'     , default=False, action='store_true')
    (opt, args) = parser.parse_args()

    yearList = []
    for year in opt.years.split('-'):
        if year in yearsInfos: yearList.append(year)
        else:
            for key in yearsInfos:
                if year==yearsInfos[key]['Run']: yearList.append(key)

    for year in yearList: 

        yearInfos = yearsInfos[year]
        yearPeriods = { }

        if opt.periods=='All': yearPeriods[year] = yearInfos['runs']
        else:
            for period in opt.periods.split('-'):
                if 'To' not in period:
                    if year in runPeriods:
                        if period=='Split': 
                            yearPeriods = runPeriods[year]
                        elif period==runPeriods[year] or year.replace('UL','')+period==runPeriods[year]:
                            periodYear = year if year not in period else ''
                            yearPeriods[periodYear+period] = runPeriods[year][periodYear+period]
                        else:
                            firstRun, lastRun = 99999999999999, 0
                            for prd in runPeriods[year]:
                                if prd.replace(year, '') in period:
                                    firstRun = min(firstRun, runPeriods[year][prd][0])
                                    lastRun  = max(lastRun,  runPeriods[year][prd][1])
                            periodYear = year if year not in period else ''
                            yearPeriods[periodYear+period] = [ firstRun, lastRun ]
                    else: print('Warning:', year, 'not in runPeriods')
                elif ':' in period:
                    periodname = period.split(':')[0]
                    periodrange = period.split(':')[1]
                    yearPeriods[periodname] = [ int(periodrange.split('To')[0]), int(periodrange.split('To')[1]) ]
                else: print('Warning:', period, 'has not a good period structure. It should be "PeriodName:FirstRunToLastRun"')

        if len(list(yearPeriods.keys()))==0: 
            print('Error: no run periods selected')
            exit()

        goodRuns = loadJSON(yearInfos['jsonFile'])

        for period in yearPeriods:

            selectedGoodRuns = { }

            for run in goodRuns:
                if int(run)>=yearPeriods[period][0] and int(run)<=yearPeriods[period][1]:
                    selectedGoodRuns[run] = goodRuns[run]

            if 'prescale' in opt.action.lower() or 'ps' in opt.action.lower():

                if opt.hltPaths=='':
                    print('Error: need to specify an HLT path to compute the prescales')
                    exit()

                periodPrescales = { }

                for hltPath in opt.hltPaths.split('-'):

                    periodPrescales[hltPath] = { } 

                    if not opt.readPS:
 
                        brilcalcCommand = [ brilcalcSetup() ] 

                        brilcalcCommand.extend(['mkdir -p '+opt.outputDir+'/Prescales', 'rm -f '+opt.outputDir+'/Prescales/Prescales_'+period+'_'+hltPath+'.csv' ])

                        for run in selectedGoodRuns:
                            brilcalcCommand.append('brilcalc trg -r '+run+' --prescale --hltpath "'+hltPath+'_v*" -o '+opt.outputDir+'/Prescales/Prescales_'+period+'_'+hltPath+'_'+run+'.csv')

                        brilcalcCommand.append('cat '+opt.outputDir+'/Prescales/Prescales_'+period+'_'+hltPath+'_*.csv > '+opt.outputDir+'/Prescales/Prescales_'+period+'_'+hltPath+'.csv')
                        brilcalcCommand.append('rm -f '+opt.outputDir+'/Prescales/Prescales_'+period+'_'+hltPath+'_*.csv')

                        os.system('\n'.join(brilcalcCommand))

                    if opt.saveJSON or opt.mergePS:

                        with open(opt.outputDir+'/Prescales/Prescales_'+period+'_'+hltPath+'.csv', 'r') as file:
                            csvreader = csv.reader(file)
                            for row in csvreader:
                                if hltPath in row[4]:

                                    run, lumiblock, prescale = row[0], row[1], row[3]
  
                                    if int(run)>=yearPeriods[period][0] and int(run)<=yearPeriods[period][1]:

                                        if run not in periodPrescales[hltPath]: 
                                            periodPrescales[hltPath][run] = { }
   
                                        periodPrescales[hltPath][run][lumiblock] = { }
                                        periodPrescales[hltPath][run][lumiblock]['prescale'] = prescale
  
                        for run in periodPrescales[hltPath]:
                            for lumiblock in periodPrescales[hltPath][run]:
                                lastblock = 99999999999999999
                                for otherblock in periodPrescales[hltPath][run]:
                                    if otherblock!=lumiblock:
                                        if int(otherblock)>int(lumiblock) and int(otherblock)<=lastblock:
                                            lastblock = int(otherblock)-1
                                periodPrescales[hltPath][run][lumiblock]['lastblock'] = str(lastblock)

                        if len(list(periodPrescales[hltPath].keys()))==0:
                            del periodPrescales[hltPath]
                        elif opt.saveJSON:
                            with open(opt.outputDir+'/Prescales/TriggerPrescales_'+period+'_'+hltPath+'.json', 'w') as file:
                                file.write(json.dumps(periodPrescales[hltPath]))

                if opt.mergePS:
                    with open(opt.outputDir+'/Prescales/TriggerPrescales_'+period+'.json', 'w') as file:
                        file.write(json.dumps(periodPrescales))

            else:

                json.dump(selectedGoodRuns, open('temporary_'+period+'.json', 'w'))

                if 'lumi' in opt.action.lower():

                    brilcalcCommand = [ brilcalcSetup() ]

                    brilcalcCommand.append('mkdir -p '+opt.outputDir+'/Luminosity')
     
                    brilcalcBaseCommand = 'brilcalc lumi -b "STABLE BEAMS" -i temporary_'+period+'.json --normtag '+yearInfos['normtagFile']+' -u /'+opt.lumiunit

                    if opt.hltPaths=='':
                        brilcalcCommand.append(brilcalcBaseCommand+' > '+opt.outputDir+'/Luminosity/Luminosity_'+period+'.txt')
                    else:
                        for hltPath in opt.hltPaths.split('-'):
                            brilcalcCommand.append(brilcalcBaseCommand+' --hltpath "'+hltPath+'_v*" > '+opt.outputDir+'/Luminosity/Luminosity_'+hltPath+'_'+period+'.txt')

                    os.system('\n'.join(brilcalcCommand))

                elif 'pileup' in opt.action.lower() or 'pu' in opt.action.lower():

                    os.system('mkdir -p '+opt.outputDir+'/Pileup')

                    pileupJSON = yearInfos['pileupFile']
                    if 'http' in pileupJSON:
                        pileupJSON = './'+yearInfos['pileupFile'].split('/')[-1]
                        os.system('wget '+yearInfos['pileupFile'])

                    for xSec in minBiasXsec[yearInfos['Run']]:
                        os.system('pileupCalc.py -i temporary_'+period+'.json --inputLumiJSON ' + pileupJSON + ' --calcMode true --minBiasXsec ' + minBiasXsec[yearInfos['Run']][xSec] + ' --maxPileupBin ' + yearInfos['numPileupBins'] + ' --numPileupBins ' + yearInfos['numPileupBins'] + ' --pileupHistName ' + xSec + ' ' + opt.outputDir + '/Pileup/' + period+'_'+xSec+'.root')

                    os.system('hadd -f -k '+opt.outputDir+'/Pileup/'+period+'.root'+' '+opt.outputDir+'/Pileup/'+period+'_*.root; rm '+opt.outputDir+'/Pileup/'+period+'_*.root')
 
                os.system('rm -r temporary_'+period+'.json')


