#!/bin/bash

prod=$1
step=$2

queue=cms_med
if [ $step == 'sel' ]; then
    queue=cms_main
elif [ $step == 'data' ]; then
    queue=cms_main
fi
if [ $# -gt 2 ]; then
    queue=cms_$3
fi

naod='nAODv8'

if [ $prod == '16HIPM' ]; then
    year='16'
    naod='nAODv9_HIPM'
elif [ $prod == '16noHIPM' ]; then
    year='16'
    naod='nAODv9_noHIPM'
else:
    year=$prod
fi

if [ $step == 'data' ]; then

    ./mkPostProc.py -p Run20${year}_106X_${naod}_Full20${year}v8 -s DATASusy20${year}v8 -b -Q $queue -T MuonEG_Run2016C_HIPM_UL2016-v1

elif [ $step == 'sel' ]; then

    ./mkPostProc.py -p Summer20UL${year}_106X_${naod}_Full20${year}v8 -s MCSusy20${year}v8 -b -Q $queue

elif [ $step == 'corr' ]; then

    ./mkPostProc.py -p Summer20UL${year}_106X_${naod}_Full20${year}v8 -i MCSusy20${year}v8 -s MCSusyCorr20${year}v8 -b -Q $queue

elif [ $step == 'syst' ]; then

    for syst in Nomin JESUp JESDo ; do
        ./mkPostProc.py -p Summer20UL${year}_106X_${naod}_Full20${year}v8 -i MCSusy20${year}v8__MCSusyCorr20${year}v8 -s MCSusy${syst}20${year}v8 -b -Q $queue
    done

elif [[ $step == 'reco' ]] || [[ $step == 'ctrl' ]] ; then

    for met in Nomin Smear SMTUp SMTDo ; do
        ./mkPostProc.py -p Summer20UL${year}_106X_${naod}_Full20${year}v8 -i MCSusy20${year}v8__MCSusyCorr20${year}v8__MCSusyNomin20${year}v8 -s susyMT2${step}$met -b -Q $queue
    done

    ./mkPostProc.py -p Summer20UL${year}_106X_${naod}_Full20${year}v8 -i MCSusy20${year}v8__MCSusyCorr20${year}v8__MCSusyJESUp20${year}v8 -s susyMT2${step}SJSUp -b -Q $queue
    ./mkPostProc.py -p Summer20UL${year}_106X_${naod}_Full20${year}v8 -i MCSusy20${year}v8__MCSusyCorr20${year}v8__MCSusyJESDo20${year}v8 -s susyMT2${step}SJSDo -b -Q $queue

fi

