import ROOT
import math
import os
import subprocess
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from LatinoAnalysis.NanoGardener.data.SusyISRCorrections import SUSYISRCorrections

class SusyWeightsProducer(Module):

    ###
    def __init__(self, cmssw, sourcedir):
        self.cmssw = cmssw
        self.sourcedir = sourcedir[:sourcedir.index('susyGen')] + 'susyGen'
        pass

    ###
    def beginJob(self):
        pass

    ###
    def endJob(self):
        pass

    ###
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("baseW",         "F")
        self.out.branch("isrW",          "F")

        inputFileName = inputFile.GetName()

        datasetName = inputFileName.split('nanoLatino_')[-1].split('__part')[0].replace('.root','')
        massPointDicName = self.sourcedir + '/' + datasetName + '.py'

        if os.path.isfile(massPointDicName): 

            exec(open(massPointDicName).read())
            self.massPointN    = massPointN
            self.isrObservable = isrObservable 
            self.isrEdge       = isrEdge 
            self.isrCorrection = isrCorrection
            self.isrBins       = isrBins

        else:

            chain = ROOT.TChain('Events')
              
            if '__part' in inputFileName :
                inputFileName = inputFileName[:inputFileName.index('__part')] + '__part*.root'
                nInputTrees = int(subprocess.check_output('ls ' + self.sourcedir + '/' + inputFileName + ' | grep -c root', shell=True).strip('\n'))
                for part in range(nInputTrees):
                    partFileName = self.sourcedir + '/' + inputFileName.replace('__part*.root', '__part' + str(part) + '.root')
                    if os.path.isfile(partFileName) :
                        chain.Add(partFileName)
                    else:
                        raise Exception('SusyWeightsProducer ERROR: input susyGen file', partFileName, 'does not exist')

            else:
                chain.Add(self.sourcedir + '/' + inputFileName)
                nInputTrees = 1

            print 'SusyWeightsProducer: read', nInputTrees, 'input susyGen files with', chain.GetEntries(), 'events'
   
            self.massPointN, self.isrObservable, self.isrEdge, self.isrCorrection, self.isrBins = {}, {}, {}, {}, {}
            idPromptList = [ ]

            if 'pMSSM' in inputFileName:
                idPromptList.append( 9999999 )

            else:
                inputTree.SetEstimate(inputTree.GetEntries())
                inputTree.Draw('susyIDprompt')
                idPromptArray = inputTree.GetV1()
                for i in range(inputTree.GetSelectedRows()):
                    if int(idPromptArray[i]) not in idPromptList:
                        idPromptList.append(int(idPromptArray[i]))

            for idPrompt in idPromptList:
                
                self.massPointN[idPrompt] = { }
  
                self.isrObservable[idPrompt] = ''

                for process in SUSYISRCorrections:
                    if str(idPrompt) in SUSYISRCorrections[process]['susyPromptParticles']:
                        for isrVer in SUSYISRCorrections[process]['version']:
                            if self.cmssw in SUSYISRCorrections[process]['version'][isrVer]['production']:

                                self.isrObservable[idPrompt] = SUSYISRCorrections[process]['version'][isrVer]['observable']
                        
                                self.isrEdge[idPrompt] = []
                                self.isrCorrection[idPrompt] = []

                                for edge in sorted(SUSYISRCorrections[process]['version'][isrVer]['correction'].keys()) :
                                    
                                    self.isrEdge[idPrompt].append( float(edge) )
                                    self.isrCorrection[idPrompt].append( float(SUSYISRCorrections[process]['version'][isrVer]['correction'][edge]) )

                                self.isrBins[idPrompt] = len(self.isrEdge[idPrompt]) - 1

                if self.isrObservable[idPrompt]=='' :
                    raise Exception('SusyWeightsProducer ERROR: SUSY model not found for', inputFile.GetName())

                modelPointList = []
                if idPrompt==9999999:
                    massScan = ROOT.TH2D("massScan", "", 600, 1., 601., 144855, 1., 144856.) # The first pMSSM ID takes on values between 1 and 600
                    inputTree.Project(massScan.GetName(), "pMSSMid2:pMSSMid1", "1.", "") # the second pMSSM ID takes on values between 1 and 144855
                    for key in inputTree.GetListOfBranches():
                        if 'GenModel_pMSSM_MCMC' in key.GetName():
                            xb = int(key.GetName().split('_')[3])
                            yb = int(key.GetName().split('_')[4].replace('.slha',''))
                            modelPointList.append([xb, yb])
                else:
                    massScan = ROOT.TH2D("massScan", "", 3000, 0., 3000., 3000, 0., 3000.)
                    inputTree.Project(massScan.GetName(), "susyMLSP:susyMprompt", "susyIDprompt=="+str(idPrompt), "") 
                    for xb in range(1, massScan.GetNbinsX()+1) :
                        for yb in range(1, massScan.GetNbinsY()+1) :
                            if massScan.GetBinContent(xb, yb)>0. :
                                modelPointList.append([xb, yb])

                for modelPoint in modelPointList:
                    xb = modelPoint[0]
                    yb = modelPoint[1]
                    if xb>=0: 
                        if yb>=0: 

                            histoISR = ROOT.TH1D("histoISR", "", self.isrBins[idPrompt], array('d',self.isrEdge[idPrompt]))
                            if idPrompt==9999999: massSel = "(pMSSMid1=="+str(xb)+" && pMSSMid2=="+str(yb)+")" 
                            else: massSel = "(susyMprompt=="+str(xb-1)+" && susyMLSP=="+str(yb-1)+" && susyIDprompt=="+str(idPrompt)+")"
                            chain.Project(histoISR.GetName(), self.isrObservable[idPrompt], massSel+"*genWeight", "")

                            reweightedNormalization = 0.
                            for ib in range(self.isrBins[idPrompt]+1) :
                                reweightedNormalization += histoISR.GetBinContent(ib+1)*self.isrCorrection[idPrompt][ib]

                            normFactor = histoISR.Integral(0, self.isrBins[idPrompt]+1)/reweightedNormalization

                            massPointName = str(xb)+"-"+str(yb) if idPrompt==9999999 else str(xb-1)+"-"+str(yb-1)
                            self.massPointN[idPrompt][massPointName] = {}
                            self.massPointN[idPrompt][massPointName]['events'] = histoISR.GetEntries()
                            self.massPointN[idPrompt][massPointName]['isrW'] = normFactor
                            if idPrompt==9999999:
                                print 'SusyWeightsProducer: overall ISR normalization factor for pMSSM point (',str(xb),',',str(yb),'):', normFactor
                            else:
                                print 'SusyWeightsProducer: overall ISR normalization factor for mass point (',str(idPrompt),',',str(xb-1),',',str(yb-1),'):', normFactor
                        
    ###    
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    ###
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if 9999999 in self.massPointN:
            idPromptSusy = 9999999
            massPointName = str(event.pMSSMid1)+"-"+str(event.pMSSMid2)

        else:
            idPromptSusy = int(event.susyIDprompt)
            massPointName = str(int(event.susyMprompt))+"-"+str(int(event.susyMLSP))

        Xsec  = event.Xsec
        nevents = self.massPointN[idPromptSusy][massPointName]['events']
         
        baseW = 1000.*Xsec/nevents

        isrW = self.massPointN[idPromptSusy][massPointName]['isrW']
        for ib in reversed(xrange(self.isrBins[idPromptSusy]+1)) :
            if getattr(event, self.isrObservable[idPromptSusy]) >= self.isrEdge[idPromptSusy][ib] :
                isrW *= self.isrCorrection[idPromptSusy][ib]
                break

        self.out.fillBranch("baseW",   baseW)
        self.out.fillBranch("isrW",    isrW)      
            
        return True
 
