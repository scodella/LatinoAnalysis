#!/bin/bash

if [[ $HOST == 'lxplus'* ]] ; then
    #baseOutputDirectory='/eos/cms/store/user/scodella/SUSY/Nano/'
    #baseOutputDirectory='/eos/cms/store/caf/user/scodella/BTV/Nano/'
    baseOutputDirectory='/eos/cms/store/group/phys_susy/Chargino/Nano/'
    baseInputDirectory=$baseOutputDirectory
    #baseInputDirectory='/eos/cms/store/caf/user/scodella/BTV/Nano/'
    #baseInputDirectory='/eos/user/s/scodella/SUSY/Nano/'
else
    baseInputDirectory='/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'
    baseOutputDirectory=$baseInputDirectory
fi

prods=$1
steps=$2

sigSamples='T2tt_mStop-525_mLSP-350,T2tt_mStop-525_mLSP-438,TChipmSlepSnu_mC-1150_mX-1,TChipmSlepSnu_mC-900_mX-475'

isAllDone () {

    datasetsToExclude=$sample
 
    inputDirectory=$baseInputDirectory/$2/$3/
    if [ -d "$inputDirectory" ]; then
        inputFiles=$(ls $inputDirectory/*root | grep -c root)
        if [ "$inputFiles" == "0" ] ; then
            return 1
        fi
    else 
        return 1
    fi

    if [[ $1 == 'hadd' || $1 == 'corr' || $1 == 'swgt' ]] ; then
        # This is treaky
        if [[ "$datasetsToExclude" == *"-T "* ]] ; then
            echo Will not proceed with submission for $2 step $4: option -T not supported by this script for the required step
            return 2
        fi
        ls $inputDirectory | grep .root > filesToHadd_${2}_${3}.txt
        dataset=""
        noAvailableDatasets=1
        while read line ; do
            line="${line/nanoLatino_/}"
            line=${line%__part*}
            if [ "$line" != "$dataset" ] ; then
                datasetFiles=$(ls $inputDirectory/nanoLatino_${line}__part*.root | grep -c root)
                missingFiles=0
                for i in $(seq $datasetFiles); do 
                    if [ ! -f "$inputDirectory/nanoLatino_${line}__part$((i-1)).root" ]; then
                        missingFiles=1
                    fi
                done
                if  [ "$missingFiles" == "1" ] ; then
                    if [ "$datasetsToExclude" != "" ] ; then
                        datasetsToExclude=${datasetsToExclude},
                    fi
                    datasetsToExclude=$datasetsToExclude$line
                else
                    noAvailableDatasets=0
                fi
                dataset=$line
            fi
        done < filesToHadd_${2}_${3}.txt
        rm filesToHadd_${2}_${3}.txt
        if [[ "$datasetsToExclude" != "" &&  "$datasetsToExclude" != *"-E "* ]] ; then
            datasetsToExclude="-b -E "$datasetsToExclude
        fi
        return $noAvailableDatasets
    else
        outputDirectory=$baseOutputDirectory/$2/${3}__${4}/
        if [ -d "$outputDirectory" ]; then
            outputFiles=$(ls $outputDirectory/*root | grep -c root)
            if [[ $inputFiles -eq $outputFiles ]] ; then
                return 1
            else
                return 0
            fi
        else 
            return 0
        fi
    fi 

}

submitJobs () {

    if [[ $1 == 'lep' || $1 == 'sel' || $1 == 'sgen' ]] ; then
        if [ $1 == 'lep' ]; then
            samples=$sample
        elif [ $1 == 'sel' ]; then
            samples=" -E "$sigSamples
        elif [ $1 == 'sgen' ]; then
            samples=" -T "$sigSamples
        fi
        ./mkPostProc.py -p $2 -s $3 -b -Q $queue $samples
    else
        isAllDone $step $2 $3 $4
        allDone=$?
        if [ "$allDone" == "0" ] ; then
            ./mkPostProc.py -p $2 -i $3 -s $4 -b -Q $queue $datasetsToExclude
        elif [ "$allDone" == "1" ] ; then
            echo Nothing to submit for $2 step $4
        fi
    fi

}

for prod in 16HIPM 16noHIPM 17 18 ; do
    if [[ $prods == 'all' || $prods == *${prod}* ]]; then
       
        dataSteps=(lep hadd mt2)
        mcSteps=(sel corr syst reco ctrl)
        sigSteps=(sgen swgt ssel scorr ssyst sreco sctrl)
        for step in ${dataSteps[@]} ${mcSteps[@]} ${sigSteps[@]} ; do
            stepType=''
            sigPreDir=''
            if echo ${dataSteps[@]} | grep -w -q $step ; then
                stepType=data
            elif echo ${mcSteps[@]} | grep -w -q $step ; then
                stepType=mc
            elif echo ${sigSteps[@]} | grep -w -q $step ; then
                stepType=sig
                sigPreStep='susyGen__susyW'
                sigPreDir=${sigPreStep}__
            fi
            if [[ $steps == 'all' || $steps == $stepType || $steps == $step ]] ; then

                if [[ $HOST == 'lxplus'* ]] ; then
                    queue=tomorrow
                else
                    queue=cms_med
                    if [[ $step == 'lep' || $step == 'sel' || $step == 'ssel' || $step == 'swgt' ]]; then
                        queue=cms_main
                    elif [[ $step == 'hadd' || $step == 'mt2' || $step == *'reco' || $step == *'ctrl' ]]; then
                        queue=cms_high
                    fi
                fi

                sample=''
                if [ $# -gt 2 ]; then
                    if [[ $3 == *' '* ]]; then
                        sample=$3
                    elif [[ $3 == 'main' || $3 == 'med' || $3 == 'high' ]]; then
                        queue=cms_$3
                    else
                        queue=$3
                    fi 
                    if [ $# -gt 3 ]; then
                        sample=$4
                    fi
                fi

                naod='nAODv9'
                corr=''

                if [ $prod == '16HIPM' ]; then
                    year='16'
                    naod='nAODv9_HIPM'
                    corr='HIPM'
                elif [ $prod == '16noHIPM' ]; then
                    year='16'
                    naod='nAODv9_noHIPM'
                    corr='noHIPM'
                else
                    year=$prod
                fi

                if [ $step == 'lep' ]; then

                    submitJobs $step Run20${year}_106X_${naod}_Full20${year}v8 DATASusy20${year}v8

                elif [ $step == 'hadd' ]; then

                    submitJobs $step Run20${year}_106X_${naod}_Full20${year}v8 DATASusy20${year}v8 hadd

                elif [ $step == 'mt2' ]; then

                    submitJobs $step Run20${year}_106X_${naod}_Full20${year}v8 DATASusy20${year}v8__hadd susyMT2recoNomin
                    submitJobs $step Run20${year}_106X_${naod}_Full20${year}v8 DATASusy20${year}v8__hadd susyMT2ctrlNomin

                elif [ $step == 'sel' ]; then

                    submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 MCSusy20${year}v8

                elif [ $step == 'sgen' ]; then

                    submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 susyGen

                elif [ $step == 'swgt' ]; then

                    submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 susyGen susyW

                elif [ $step == 'ssel' ]; then

                    submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 $sigPreStep MCSusy20${year}v8

                elif [[ $step == *'corr' ]]; then

                    submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 ${sigPreDir}MCSusy20${year}v8 MCSusyCorr20${year}v8$corr

                elif [[ $step == *'syst' ]]; then

                    for syst in Nomin JESUp JESDo JERUp JERDo ; do 
                        submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 ${sigPreDir}MCSusy20${year}v8__MCSusyCorr20${year}v8$corr MCSusy${syst}20${year}v8
                    done

                elif [[ $step == *'reco' ]] || [[ $step == *'ctrl' ]] ; then

                    sstep=$step
                    if [[ $step == 'sreco' ]] ; then
                        sstep=reco
                    elif [[ $step == 'sctrl' ]] ; then
                        sstep=ctrl
                    fi

                    for met in Nomin Smear SMTUp SMTDo ; do
                        submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 ${sigPreDir}MCSusy20${year}v8__MCSusyCorr20${year}v8${corr}__MCSusyNomin20${year}v8 susyMT2${sstep}$met
                    done

                    submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 ${sigPreDir}MCSusy20${year}v8__MCSusyCorr20${year}v8${corr}__MCSusyJESUp20${year}v8 susyMT2${sstep}SJSUp
                    submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 ${sigPreDir}MCSusy20${year}v8__MCSusyCorr20${year}v8${corr}__MCSusyJESDo20${year}v8 susyMT2${sstep}SJSDo

                    submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 ${sigPreDir}MCSusy20${year}v8__MCSusyCorr20${year}v8${corr}__MCSusyJERUp20${year}v8 susyMT2${sstep}JERUp
                    submitJobs $step Summer20UL${year}_106X_${naod}_Full20${year}v8 ${sigPreDir}MCSusy20${year}v8__MCSusyCorr20${year}v8${corr}__MCSusyJERDo20${year}v8 susyMT2${sstep}JERDo

                fi


            fi
        done

    fi
done


