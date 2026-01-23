#!/bin/sh 

if [[ $1 == "all" ]]; then
    if [[ $2 == "c"* ]] || [[ $2 == "j"* ]] || [[ $2 == "m"* ]] ; then
        prods=UL16HIPM,UL16noHIPM,UL17,UL18
    else
        prods=UL16,UL17,UL18
    fi
else
    prods=$1
fi
step=$2
if [ $# -ne 3 ]; then
    samples=pMSSM_set1prompt1_ext1,pMSSM_set1prompt2_ext1,pMSSM_set1prompt3_ext1,pMSSM_set2prompt1_ext1,pMSSM_set2prompt2_ext1,pMSSM_set1LL_ext1,pMSSM_set2LL1_ext1,pMSSM_set2LL2_ext1
elif [[ $3 == "p" ]]; then
    samples=pMSSM_set1prompt1_ext1,pMSSM_set1prompt2_ext1,pMSSM_set1prompt3_ext1,pMSSM_set2prompt1_ext1,pMSSM_set2prompt2_ext1
elif [[ $3 == "p1" ]]; then
    samples=pMSSM_set1prompt1_ext1,pMSSM_set1prompt2_ext1,pMSSM_set1prompt3_ext1
elif [[ $3 == "p11" ]]; then
    samples=pMSSM_set1prompt1_ext1
elif [[ $3 == "p12" ]]; then
    samples=pMSSM_set1prompt2_ext1
elif [[ $3 == "p13" ]]; then
    samples=pMSSM_set1prompt3_ext1
elif [[ $3 == "p2" ]]; then
    samples=pMSSM_set2prompt1_ext1,pMSSM_set2prompt2_ext1
elif [[ $3 == "p21" ]]; then
    samples=pMSSM_set2prompt1_ext1
elif [[ $3 == "p22" ]]; then
    samples=pMSSM_set2prompt2_ext1
elif [[ $3 == "l" ]]; then
    samples=pMSSM_set1LL_ext1,pMSSM_set2LL1_ext1,pMSSM_set2LL2_ext1
elif [[ $3 == "l1" ]]; then
    samples=pMSSM_set1LL_ext1
elif [[ $3 == "l2" ]]; then
    samples=pMSSM_set2LL1_ext1,pMSSM_set2LL2_ext1	
elif [[ $3 == "l21" ]]; then
    samples=pMSSM_set2LL1_ext1
elif [[ $3 == "l22" ]]; then
    samples=pMSSM_set2LL2_ext1
else
    samples=$3
fi

prodlist=$(echo $prods | tr "," "\n")
for prod in $prodlist ; do

    echo $prod $step $samples

    if [[ $prod == "UL18" ]]; then
        period=""
        year=2018
        shyear=18
	ulprod=UL18
    elif [[ $prod == "UL17" ]]; then
        period=""
        year=2017
        shyear=17
        ulprod=UL17
    elif [[ $prod == "UL16HIPM" ]]; then
        period="HIPM"
        year=2016
        shyear=16
        ulprod=UL16
    elif [[ $prod == "UL16noHIPM" ]]; then
        period="noHIPM"
        year=2016
        shyear=16
        ulprod=UL16
    elif [[ $prod == "UL16" ]]; then
        period=""
        year=2016
        shyear=16
        ulprod=UL16
    fi

    production=Spring21UL${shyear}FS_106X_nAODv9_Full${year}v8

    if [[ $step == "g"* ]]; then

	./mkPostProc.py -p $production -s susyGen -T $samples -b -Q nextweek 

    elif [[ $step == "h"* ]]; then

	./mkPostProc.py -p $production -i susyGen -s hadd -T $samples -b

    elif [[ $step == "l"* ]]; then

        ./mkPostProc.py -p $production -i susyGen -s FSSusy${year}v8 -T $samples -b

    elif [[ $step == "c"* ]]; then

        ./mkPostProc.py -p $production -i susyGen__FSSusy${year}v8 -s FSSusyCorr${year}v8${period} -T $samples -b

    elif [[ $step == "j"* ]]; then

        ./mkPostProc.py -p $production -i susyGen__FSSusy${year}v8__FSSusyCorr${year}v8${period} -s FSSusyNomin${year}v8$period -T $samples -b

    elif [[ $step == "m"* ]]; then

        ./mkPostProc.py -p $production -i susyGen__FSSusy${year}v8__FSSusyCorr${year}v8${period}__FSSusyNomin${year}v8$period -s susyMT2fastSmear -T $samples -b

    elif [[ $step == "r"* ]]; then

        ./mkPostProc.py -p $production -i susyGen__FSSusy${year}v8__FSSusyCorr${year}v8${period}__FSSusyNomin${year}v8$period -s susyMT2crfsSmear -T $samples -b
    fi

done


