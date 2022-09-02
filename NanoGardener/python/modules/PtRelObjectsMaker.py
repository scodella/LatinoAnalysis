import ROOT
import math
import os.path
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class PtRelObjectsMaker(Module):

    ###
    def __init__(self):
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

        self.out.branch('muJet_idx',    'I')
        self.out.branch('muJet_pt',     'F')
        self.out.branch('muJet_eta',    'F')
        self.out.branch('muJet_phi',    'F')
        self.out.branch('muJet_ptrel',  'F')
        self.out.branch('muJet_muon',   'I')
        self.out.branch('nSoftMuon',    'I')

    ###    
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def getPtRel(self, muon, jet):

        muonvec = ROOT.TVector3()
        muonvec.SetPtEtaPhi(muon.pt, muon.eta, muon.phi)

        jetvec = ROOT.TVector3()
        jetvec.SetPtEtaPhi(jet.pt, jet.eta, jet.phi)
  
        return muonvec.Perp(jetvec)

    ###
    def analyze(self, event):
        '''process event, return True (go to next module) or False (fail, go to next event)'''

        if event.nMuon==0: return False
        
        muons = Collection(event, 'Muon')
        jets  = Collection(event, 'Jet')

        nSoftMuon, softMuonPt = 0, 5.
        muJet_idx, muJet_muon = -1, -1
        muJet_pt, muJet_eta, muJet_phi, muJet_ptrel = -1., -1., -1., -1.

        for mu in range(event.nMuon):
            if muons[mu].pt>=5. and abs(muons[mu].eta)<=2.4 and muons[mu].jetIdx>=0:
                if muons[mu].mediumId:

                  if muons[mu].pt>softMuonPt and jets[muons[mu].jetIdx].pt>=20. and abs(jets[muons[mu].jetIdx].eta)<2.5:

                      muJet_idx   = muons[mu].jetIdx
                      muJet_pt    = jets[muons[mu].jetIdx].pt
                      muJet_eta   = jets[muons[mu].jetIdx].eta
                      muJet_phi   = jets[muons[mu].jetIdx].phi
                      muJet_ptrel = self.getPtRel(muons[mu], jets[muons[mu].jetIdx])
                      muJet_muon  = mu
                   
                  nSoftMuon += 1

        if nSoftMuon==0 or muJet_idx==-1: return False

        self.out.fillBranch('muJet_idx',   muJet_idx)
        self.out.fillBranch('muJet_pt',    muJet_pt)
        self.out.fillBranch('muJet_eta',   muJet_eta)
        self.out.fillBranch('muJet_phi',   muJet_phi)
        self.out.fillBranch('muJet_ptrel', muJet_ptrel)
        self.out.fillBranch('muJet_muon',  muJet_muon)
        self.out.fillBranch('nSoftMuon',   nSoftMuon)

        return True
 
