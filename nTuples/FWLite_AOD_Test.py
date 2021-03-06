import time
import ROOT
import os
import psutil


process = psutil.Process(os.getpid())
print process.__dict__
print process.memory_info().__dict__
from DataFormats.FWLite import Handle, Events
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()



makeitleak = True
altCall = True

events = Events(["testoutAOD100.root"])
offEle_source, offEle_label                         = Handle("vector<reco::GsfElectron>"), ("gedGsfElectrons")
offMu_source, offMu_label                           = Handle("vector<reco::Muon>"), ("muons")
MuGlobalTracks_source, MuGlobalTracks_label         = Handle("vector<reco::Track>"), ("globalTracks")
if makeitleak:
    eleLooseID_source, eleLooseID_label                 = Handle("<edm::ValueMap<bool>>"), ("egmGsfElectronIDs:cutBasedElectronID_Fall17_94X_V1_loose")
    eleTightID_source, eleTightID_label                 = Handle("<edm::ValueMap<bool>>"), ("egmGsfElectronIDs:cutBasedElectronID_Fall17_94X_V1_tight")
offJets_source, offJets_label =                       Handle("vector<reco::PFJet>"), ("ak4PFJetsCHS")
offbTags_source, offbTags_label =  Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>>"), ("pfCombinedInclusiveSecondaryVertexV2BJetTags")

for i,event in enumerate(events):
    if i%10000==0:
        print "Processing event {0:10} ------ Memory: RES {1:3.2f} MB - VIRT {2:3.2f} MB ".format(i, process.memory_info().rss/1000000.0, process.memory_info().vms/1000000.0)
        #time.sleep(1)
    event.getByLabel(offEle_label, offEle_source)
    event.getByLabel(offMu_label, offMu_source)
    event.getByLabel(MuGlobalTracks_label, MuGlobalTracks_source)
    if makeitleak:
        event.getByLabel(eleLooseID_label , eleLooseID_source)
        event.getByLabel(eleTightID_label , eleTightID_source)
    event.getByLabel(offJets_label, offJets_source)
    event.getByLabel(offbTags_label, offbTags_source)
    print "-",offEle_source.isValid(), eleTightID_source.isValid()
    if offEle_source.isValid() and eleTightID_source.isValid():
        for iele, ele in  offEle_source.product():
            print ele, ele.pt(), eleTightID_source.product().get(iele)

    """
    print  "+",offbTags_source.isValid(),offJets_source.isValid()
    if offbTags_source.isValid() and offJets_source.isValid():
        for jet in offJets_source.product():
            offbtags = offbTags_source.product()
            for ibjet in range(len(offbtags)):
                 jobj = offbtags.key(ibjet).get()
                 print jobj,jobj.pt(),offbtags.value(ibjet)
    """

print "Processing event {0:10} ------ Memory: RES {1:3.2f} MB - VIRT {2:3.2f} MB ".format(i, process.memory_info().rss/1000000.0, process.memory_info().vms/1000000.0)

    
