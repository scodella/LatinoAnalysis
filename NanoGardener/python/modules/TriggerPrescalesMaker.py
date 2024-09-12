import ROOT
import math
import os.path
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TriggerPrescalesMaker(Module):

    ###
    def __init__(self, TriggerPrescalesPath = 'LatinoAnalysis/NanoGardener/python/data/trigger/TriggerPrescales.py'):

        cmssw_base = os.getenv('CMSSW_BASE')
        exec(open(cmssw_base+'/src/'+TriggerPrescalesPath).read())
        self.TriggerPrescales = TriggerPrescales
        self.missingRuns = {}
        self.badLumiBlocks = {}

    ###                                                                                                                    
    def beginJob(self):
        pass

    ###
    def endJob(self):
        for trigger in self.missingRuns:
            for run in self.missingRuns[trigger]:
                print(('TriggerPrescalesMaker: run', run, 'not found in prescale dictionary for trigger path', trigger))
        for trigger in self.badLumiBlocks:
            for run in self.badLumiBlocks[trigger]:
                print(('TriggerPrescalesMaker: run', run, 'has not prescale information for trigger path', trigger))

    ###
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        for trigger in list(self.TriggerPrescales.keys()):
            self.out.branch('prescale_'+trigger.replace('HLT_',''), 'F')

    ###    
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    ###
    def analyze(self, event):
        '''process event, return True (go to next module) or False (fail, go to next event)'''

        run = str(event.run)

        for trigger in list(self.TriggerPrescales.keys()):

            prescale = -1.

            if run in self.TriggerPrescales[trigger]:
                if not getattr(event, trigger): prescale = 0.
                else:     
                    for lumiblock in self.TriggerPrescales[trigger][run]:
                        if lumiblock=='None':
                            if trigger not in self.badLumiBlocks:
                                self.badLumiBlocks[trigger] = []
                            if run not in self.badLumiBlocks[trigger]:
                                self.badLumiBlocks[trigger].append(run) 
                            prescale = 0.999
                        else:   
                            if event.luminosityBlock>=int(lumiblock) and event.luminosityBlock<=int(self.TriggerPrescales[trigger][run][lumiblock]['lastblock']):
                                prescale = float(self.TriggerPrescales[trigger][run][lumiblock]['prescale'])
            else: 
                 if trigger not in self.missingRuns:
                     self.missingRuns[trigger] = []
                 if run not in self.missingRuns[trigger]:
                     self.missingRuns[trigger].append(run)

            self.out.fillBranch('prescale_'+trigger.replace('HLT_',''), prescale)

        return True
 

