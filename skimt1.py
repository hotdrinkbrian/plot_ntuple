import os
import multiprocessing as mp
import copy
import math
from array import array
from ROOT import gROOT, TFile, TTree, TObject, TH1, TH1F, AddressOf
# Import objects (structs)
#similar to root[0] bash: .L means load
gROOT.ProcessLine('.L /afs/desy.de/user/h/hezhiyua/private/git1/skim/Objects.h+')
#gROOT.ProcessLine('.L /home/brian/skimtest/Objects_m1.h+')
from ROOT import JetType, JetTypeSmall

#args = '/home/brian/skimtest/'
args = '/afs/desy.de/user/h/hezhiyua/private/git1/skim/'
#jobs = []
# Struct
Jet1o = JetType()
Jet2o = JetType()
Jet3o = JetType()
Jet4o = JetType()
Jets1 = JetTypeSmall()
Jets2 = JetTypeSmall()
Jets3 = JetTypeSmall()
Jets4 = JetTypeSmall()

"""
#------------------------------------------------------------------------------------------------------
a = ['pt','eta','phi','chf','nhf','phf','elf','muf','chm','cm','nm','dR_q1','dR_q2','dR_q3','dR_q4']
aa =''
for s in a:
    #aa = aa + s+'/f:'
    aa = '        Jets4.'+s+' = Jet4o.'+s
    print aa
#------------------------------------------------------------------------------------------------------
"""
#-----------------------------------------------------------------------------------------------------------
def skim(name):
    print 'filename:', name

    oldFile = TFile(name, "READ")
    oldTree = oldFile.Get("reconstruction/tree") 
    # locate and register the Jet branches of the old ttree
    oldTree.SetBranchAddress("Jet1", AddressOf(Jet1o, 'pt') ); 
    oldTree.SetBranchAddress("Jet2", AddressOf(Jet2o, 'pt') );
    oldTree.SetBranchAddress("Jet3", AddressOf(Jet3o, 'pt') );
    oldTree.SetBranchAddress("Jet4", AddressOf(Jet4o, 'pt') );
    
    print 'skimming file',oldFile.GetName(),'\tevents =',oldTree.GetEntries(),'\tweight =',oldTree.GetWeight()

    newFile = TFile("Skim/"+name, "RECREATE")
    newFile.cd()
    newTree = TTree("tree44", "tree44")
    newTree.Branch( 'Jet1s', Jets1, 'pt/F:eta/F:chf/F:nhf/F:phf/F:elf/F:muf/F:chm/I:cm/I:nm/I:dR_q1/F:dR_q2/F:dR_q3/F:dR_q4/F' )
    newTree.Branch( 'Jet2s', Jets2, 'pt/F:eta/F:chf/F:nhf/F:phf/F:elf/F:muf/F:chm/I:cm/I:nm/I:dR_q1/F:dR_q2/F:dR_q3/F:dR_q4/F' )
    newTree.Branch( 'Jet3s', Jets3, 'pt/F:eta/F:chf/F:nhf/F:phf/F:elf/F:muf/F:chm/I:cm/I:nm/I:dR_q1/F:dR_q2/F:dR_q3/F:dR_q4/F' )
    newTree.Branch( 'Jet4s', Jets4, 'pt/F:eta/F:chf/F:nhf/F:phf/F:elf/F:muf/F:chm/I:cm/I:nm/I:dR_q1/F:dR_q2/F:dR_q3/F:dR_q4/F' )
    # this attribute list must exactly match (the order of) the features in the header file!!!! 

    #theweight = oldTree.GetWeight() 
    for i in range(  0 , oldTree.GetEntries()  ):    # why -1?
        oldTree.GetEntry(i) 
        # selections
        # Trigger
        if  Jet1o.pt>15 \
            and \
            (Jet1o.eta>-2.4 or Jet1o.eta<2.4) \
            and \
            ( \
            (Jet1o.dR_q1<0.4 and Jet1o.dR_q2>0.4 and Jet1o.dR_q3>0.4 and Jet1o.dR_q4>0.4) \
            or \
            (Jet1o.dR_q2<0.4 and Jet1o.dR_q1>0.4 and Jet1o.dR_q3>0.4 and Jet1o.dR_q4>0.4) \
            or \
            (Jet1o.dR_q3<0.4 and Jet1o.dR_q2>0.4 and Jet1o.dR_q1>0.4 and Jet1o.dR_q4>0.4) \
            or \
            (Jet1o.dR_q4<0.4 and Jet1o.dR_q2>0.4 and Jet1o.dR_q3>0.4 and Jet1o.dR_q1>0.4) \
            ) \
            : 
            # set new leaf values to old ones  
            # this attribute list must exactly match (the order of) the features in the header file!!!!    
            Jets1.pt    = Jet1o.pt
            Jets1.eta   = Jet1o.eta
            Jets1.phi   = Jet1o.phi
            Jets1.chf   = Jet1o.chf
            Jets1.nhf   = Jet1o.nhf
            Jets1.phf   = Jet1o.phf
            Jets1.elf   = Jet1o.elf
            Jets1.muf   = Jet1o.muf     
            Jets1.chm   = Jet1o.chm
            Jets1.cm    = Jet1o.cm
            Jets1.nm    = Jet1o.nm
            Jets1.dR_q1 = Jet1o.dR_q1
            Jets1.dR_q2 = Jet1o.dR_q2
            Jets1.dR_q3 = Jet1o.dR_q3
            Jets1.dR_q4 = Jet1o.dR_q4

        if  Jet2o.pt>15 \
            and \
            (Jet2o.eta>-2.4 or Jet2o.eta<2.4) \
            and \
            ( \
            (Jet2o.dR_q1<0.4 and Jet2o.dR_q2>0.4 and Jet2o.dR_q3>0.4 and Jet2o.dR_q4>0.4) \
            or \
            (Jet2o.dR_q2<0.4 and Jet2o.dR_q1>0.4 and Jet2o.dR_q3>0.4 and Jet2o.dR_q4>0.4) \
            or \
            (Jet2o.dR_q3<0.4 and Jet2o.dR_q2>0.4 and Jet2o.dR_q1>0.4 and Jet2o.dR_q4>0.4) \
            or \
            (Jet2o.dR_q4<0.4 and Jet2o.dR_q2>0.4 and Jet2o.dR_q3>0.4 and Jet2o.dR_q1>0.4) \
            ) \
            : 
            Jets2.pt    = Jet2o.pt
            Jets2.eta   = Jet2o.eta
            Jets2.phi   = Jet2o.phi
            Jets2.chf   = Jet2o.chf
            Jets2.nhf   = Jet2o.nhf
            Jets2.phf   = Jet2o.phf
            Jets2.elf   = Jet2o.elf
            Jets2.muf   = Jet2o.muf
            Jets2.chm   = Jet2o.chm
            Jets2.cm    = Jet2o.cm
            Jets2.nm    = Jet2o.nm
            Jets2.dR_q1 = Jet2o.dR_q1
            Jets2.dR_q2 = Jet2o.dR_q2
            Jets2.dR_q3 = Jet2o.dR_q3
            Jets2.dR_q4 = Jet2o.dR_q4
             
        if  Jet3o.pt>15 \
            and \
            (Jet3o.eta>-2.4 or Jet3o.eta<2.4) \
            and \
            ( \
            (Jet3o.dR_q1<0.4 and Jet3o.dR_q2>0.4 and Jet3o.dR_q3>0.4 and Jet3o.dR_q4>0.4) \
            or \
            (Jet3o.dR_q2<0.4 and Jet3o.dR_q1>0.4 and Jet3o.dR_q3>0.4 and Jet3o.dR_q4>0.4) \
            or \
            (Jet3o.dR_q3<0.4 and Jet3o.dR_q2>0.4 and Jet3o.dR_q1>0.4 and Jet3o.dR_q4>0.4) \
            or \
            (Jet3o.dR_q4<0.4 and Jet3o.dR_q2>0.4 and Jet3o.dR_q3>0.4 and Jet3o.dR_q1>0.4) \
            ) \
            :           
            Jets3.pt    = Jet3o.pt
            Jets3.eta   = Jet3o.eta
            Jets3.phi   = Jet3o.phi
            Jets3.chf   = Jet3o.chf
            Jets3.nhf   = Jet3o.nhf
            Jets3.phf   = Jet3o.phf
            Jets3.elf   = Jet3o.elf
            Jets3.muf   = Jet3o.muf
            Jets3.chm   = Jet3o.chm
            Jets3.cm    = Jet3o.cm
            Jets3.nm    = Jet3o.nm
            Jets3.dR_q1 = Jet3o.dR_q1
            Jets3.dR_q2 = Jet3o.dR_q2
            Jets3.dR_q3 = Jet3o.dR_q3
            Jets3.dR_q4 = Jet3o.dR_q4

        if  Jet4o.pt>15 \
            and \
            (Jet4o.eta>-2.4 or Jet4o.eta<2.4) \
            and \
            ( \
            (Jet4o.dR_q1<0.4 and Jet4o.dR_q2>0.4 and Jet4o.dR_q3>0.4 and Jet4o.dR_q4>0.4) \
            or \
            (Jet4o.dR_q2<0.4 and Jet4o.dR_q1>0.4 and Jet4o.dR_q3>0.4 and Jet4o.dR_q4>0.4) \
            or \
            (Jet4o.dR_q3<0.4 and Jet4o.dR_q2>0.4 and Jet4o.dR_q1>0.4 and Jet4o.dR_q4>0.4) \
            or \
            (Jet4o.dR_q4<0.4 and Jet4o.dR_q2>0.4 and Jet4o.dR_q3>0.4 and Jet4o.dR_q1>0.4) \
            ) \
            :      
            Jets4.pt    = Jet4o.pt
            Jets4.eta   = Jet4o.eta
            Jets4.phi   = Jet4o.phi
            Jets4.chf   = Jet4o.chf
            Jets4.nhf   = Jet4o.nhf
            Jets4.phf   = Jet4o.phf
            Jets4.elf   = Jet4o.elf
            Jets4.muf   = Jet4o.muf
            Jets4.chm   = Jet4o.chm
            Jets4.cm    = Jet4o.cm
            Jets4.nm    = Jet4o.nm
            Jets4.dR_q1 = Jet4o.dR_q1
            Jets4.dR_q2 = Jet4o.dR_q2
            Jets4.dR_q3 = Jet4o.dR_q3
            Jets4.dR_q4 = Jet4o.dR_q4 
            
        newTree.Fill()

    print 'produced skimmed file',newFile.GetName(),'\tevents =',newTree.GetEntries(),'\tweight =',newTree.GetWeight()
    newFile.cd()
    newFile.Write()
    newFile.Close() 
    oldFile.Close()
#-----------------------------------------------------------------------------------------------------------

#=====================================================================================================
subfiles = [i for i in os.listdir(args) if os.path.isfile(os.path.join(args, i)) and '.root' in i] 
os.chdir(args)
if not os.path.isdir('Skim'): os.mkdir('Skim')

for s in subfiles:
    p = mp.Process(target=skim, args=(s,))
    #jobs.append(p)                              
    p.start()
#=====================================================================================================
















