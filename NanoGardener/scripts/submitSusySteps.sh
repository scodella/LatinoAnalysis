#!/bin/bash

year=$1
step=$2

queue=cms_med
if [ $# -gt 2 ]; then
    queue=cms_$3
fi

if [ $step == 'syst' ]; then

    for syst in Nomin JESUp JESDo ; do
        ./mkPostProc.py -p Summer20UL${year}_106X_nAODv8_Full20${year}v8 -i MCSusy20${year}v8__MCSusyCorr20${year}v8 -s MCSusy${syst}20${year}v8 -b -Q $queue
    done

elif [[ $step == 'reco' ]] || [[ $step == 'ctrl' ]] ; then

    for met in Nomin Smear SMTUp SMTDo ; do
        ./mkPostProc.py -p Summer20UL${year}_106X_nAODv8_Full20${year}v8 -i MCSusy20${year}v8__MCSusyCorr20${year}v8__MCSusyNomin20${year}v8 -s susyMT2${step}$met -b -Q $queue
    done

    ./mkPostProc.py -p Summer20UL${year}_106X_nAODv8_Full20${year}v8 -i MCSusy20${year}v8__MCSusyCorr20${year}v8__MCSusyJESUp20${year}v8 -s susyMT2${step}SJSUp -b -Q $queue
    ./mkPostProc.py -p Summer20UL${year}_106X_nAODv8_Full20${year}v8 -i MCSusy20${year}v8__MCSusyCorr20${year}v8__MCSusyJESDo20${year}v8 -s susyMT2${step}SJSDo -b -Q $queue

fi

