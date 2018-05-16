from __future__ import division
from ROOT import ROOT, TDirectory, TFile, gFile, TBranch, TLeaf, TTree, TH1, TH1F, TH2F, TChain, TCanvas, TLegend, gROOT, gStyle
import math
#####################Settings#####################################################################################
gStyle.SetOptStat(0)
#path0 = "/afs/desy.de/user/h/hezhiyua/public/sec_data/"
#path1 = "/afs/desy.de/user/h/hezhiyua/public/qcd_vs_ctau0_vs_ctau1_v2/"
#path0 = "D:\\py_tests\\sec_data\\RecoStudies_ntuples_v2\\"
#path1 = "D:\\py_tests\\plots\\"
#path0 = "/mnt/d/py_tests/sec_data/RecoStudies_ntuples_v2/"
#path1 = "/mnt/d/py_tests/plots/"

path0 = "/afs/desy.de/user/h/hezhiyua/private/sec_data/60GeV/"
path1 = "/afs/desy.de/user/h/hezhiyua/public/qcd_vs_ctau0_vs_ctau100_ms60/"

channel = {
           #'qcd':'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
           #'ttt':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root',
           'vbf':'VBFHToBB_M-125_13TeV_powheg_pythia8.root',
           'vbfct0p60g':'VBFH_HToSSTobbbb_MH-125_MS-60_ctauS-0_TuneCUETP8M1_13TeV-powheg-pythia8_PRIVATE-MC.root'
           #'vbfct100p60g':'VBFH_HToSSTobbbb_MH-125_MS-60_ctauS-100_TuneCUETP8M1_13TeV-powheg-pythia8_PRIVATE-MC.root'	   
          }

twoD = 0 # 2D plot option: 0 --> 1D
CHS = 0 # CHS jet option: 0 --> off

number_of_bin = 100
#attr = ['pt', 'eta', 'phi', 'CSV', 'chf', 'nhf', 'phf', 'elf', 'muf', 'chm', 'cm', 'nm']
#attr = ['pt', 'nhf', 'phf', 'elf', 'muf']
#attr = ['CSV', 'chf']
#attr = ['pt']
attr = ['chm','cm']
#attr = ['chf','chm','cm','pt']
#attr = ['dR_q1','dR_q2','dR_q3','dR_q4']
#####################Settings#####################################################################################

file_dict = {}
####################
for cc in channel:
     file_dict[cc] = TFile(path0 + channel[cc],"r")
####################
#n = tree.GetEntries()
#file_dict['qcd'].Close()
hist = {}
tree = {}
##############################
for cc in channel:
    hist[cc] = {}
    tree[cc] = {}
##############################

#####################################################################################
def findbin(sample):
    nn = number_of_bin+1
    ll = 0
    edge = 0.009
    while ll < nn:
        if (hist[sample]['pt'][ll] >= edge) and (hist[sample]['pt'][ll] <= edge+0.002):
            print(ll * (300/number_of_bin))
        ll+=1
#####################################################################################
"""
###########################################################
def findDirName() 
    #file_dict['qcd']
    TIter next(file_dict['qcd'].GetListOfKeys())
    key = TKey
    while key = next():
        cl = TClass
        cl = gROOT.GetClass(key.GetClassName())
        if (cl.InheritsFrom("TDirectory")):
            dir = TDirectory
            dir = (TDirectory*)key.ReadObj()
            print( "Directory name: " + dir.GetName() )
###########################################################
"""

def write_1(var,sample):
    for s in enumerate(attr):
        if sample == 'qcd':
            color1 = 4
        elif sample == 'ttt':
            color1 = 880+1 #400+3	
        elif sample == 'ct0':
            color1 = 8 #634
        elif sample == 'ct0p05':
            color1 = 3
        elif sample == 'ct1':
            color1 = 2
        elif sample == 'ct100':
            color1 = 6	
     
        elif sample == 'vbf':
            color1 = 800+10
        elif sample == 'vbfct0p':
            color1 = 3
        elif sample == 'vbfct1p':
            color1 = 860
        elif sample == 'vbfct100p':
            color1 = 1	

        elif sample == 'vbfct0p60g':
            color1 = 3
        elif sample == 'vbfct100p60g':
            color1 = 3



        if s[1] == 'pt':
            h_par = [number_of_bin,0,300]
        elif s[1] == 'eta':
            h_par = [number_of_bin,-2.5,2.5]
        elif s[1] == 'phi':
            h_par = [number_of_bin,-math.pi,math.pi]
        elif s[1] == 'CSV':
            h_par = [number_of_bin,0,1]
        elif s[1] == 'chf':
            h_par = [number_of_bin,0,1]
        elif s[1] == 'nhf':
            h_par = [number_of_bin,0,1]
        elif s[1] == 'phf':
            h_par = [number_of_bin,0,1]
        elif s[1] == 'elf':
            h_par = [number_of_bin,0,1]
        elif s[1] == 'muf':
            h_par = [number_of_bin,0,1]
        elif s[1] == 'chm':
            h_par = [number_of_bin,0,100]
        elif s[1] == 'chm':
            h_par = [number_of_bin,0,100]
        elif s[1] == 'cm':
            h_par = [number_of_bin,0,100]
        elif s[1] == 'nm':
            h_par = [number_of_bin,0,100]

        elif s[1] == 'dR_q1':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s[1] == 'dR_q2':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s[1] == 'dR_q3':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s[1] == 'dR_q4':
            h_par = [number_of_bin,-1.1,3*math.pi]

        tree[sample][s[1]] = file_dict[sample].Get('reconstruction;1').Get('tree') #.Get('ntuple;1').Get('tree;1')

        if twoD == 0:
            hist[sample][s[1]] = TH1F(sample + s[1], '; %s; events' %s[1] , h_par[0], h_par[1], h_par[2])
        elif twoD == 1:
            hist[sample][s[1]] = TH2F(sample + s[1], '; %s; events' %s[1] , h_par[0], h_par[1], h_par[2] , number_of_bin, 0, 300)
        print( tree[sample][s[1]] )
        hist[sample][s[1]].Sumw2()

        if twoD == 0:
            tree[sample][s[1]].Project(sample+s[1], var + '.' + s[1], cutting ) #cut )
        elif twoD == 1:
            tree[sample][s[1]].Project(sample+s[1], var + '.' + s[1] + ':' + var + '.' + 'pt', cutting ) #cut )

        if hist[sample][s[1]].Integral() != 0:
            hist[sample][s[1]].Scale(1/float(hist[sample][s[1]].Integral()))
        else:
            print("denominator zero!")
        entr = tree[sample][s[1]].GetEntries(cutting)
        hist[sample][s[1]].SetLineColor(color1)
        hist[sample][s[1]].SetLineWidth(3)
        hist[sample][s[1]].SetTitle('cut: ' + cutting + '[entries after cut:' + '%s]' %entr)
        #hist[sample][s[1]].SetTitleSize(0.4,'t')
        #hist[sample][s[1]].GetYaxis().SetTitleOffset(1.6)		
        if s[1] == 'elf':
            hist[sample][s[1]].SetAxisRange(0., 0.02,"Y")
        elif s[1] == 'muf':
            hist[sample][s[1]].SetAxisRange(0., 0.02,"Y")        			
        print( hist[sample][s[1]].GetEntries() )
        #xx = gROOT.FindObject( "%s" %(sample + s[1]) ) #to find the histogram
        #xx.Delete()    #to delete the histogram

##########################################################
def plot_2(var):
    for s in enumerate(attr):
        c1 = TCanvas("c1", "Signals", 800, 800)
        c1.cd()
        c1.SetGrid()
        #gStyle.SetTitleFontSize(8.1)
        if s[1] in ('elf', 'muf', 'chm', 'cm', 'nm'):
            c1.SetLogx()
        for cc in channel:
            hist[cc][s[1]].Draw('colz same')
        #hist['qcd'][s[1]].Draw()
        #hist['ctau0'][s[1]].Draw('same')
        #hist['ttt'][s[1]].Draw('same')
        legend = TLegend(0.91, 0.91, 0.99, 0.99)
        legend.SetHeader('samples')
        for cc in channel:
            legend.AddEntry(hist[cc][s[1]],cc)
        #legend.AddEntry(hist['qcd'][s[1]],'qcd')
        #legend.AddEntry(hist['ctau0'][s[1]],'ctau0')
        #legend.AddEntry(hist['ttt'][s[1]],'ttt')
        legend.Draw()
        c1.Print(path1 + s[1] + var + cutting.replace('(','_').replace(')','_').replace('&&','A').replace('>','LG').replace('<','LS').replace('=','EQ').replace('.','P').replace('-','N').replace('Jet','J').replace('GenBquark','GBQ') + ".pdf")
        c1.Update()
##########################################################

########################################################################
def clear(sample):
    for s in enumerate(attr):
        xx = gROOT.FindObject( "%s" %(sample + s[1]) ) #to find the histogram
        xx.Delete()    #to delete the histogram
########################################################################

####################################generating list with 10 Jets
jet = []
ii = 0
num_of_jets = 1
while ii < num_of_jets:
    ii+=1
    if CHS == 0:
        jet.append('Jet' + "%s" %ii)
    elif CHS == 1:
        jet.append('CHSJet' + "%s" %ii)
####################################generating list with 10 Jets

###########################################
cut_GenBquark = [ '(GenBquark1.pt>15)&&(GenBquark1.eta<2.4)&&(GenBquark1.eta>-2.4)' ]
for i in enumerate(jet):
    cut_name = i[1] + '.'
    cut_dR = [ '(' + cut_name + 'dR_q1' + '<' + '0.4' + ')' + '&&' + '(' + cut_name + 'dR_q1'+ '>=' + '0' + ')' + '&&' + '(' + cut_name + 'dR_q2'+ '>=' + '0.4' + ')' + '&&' + '(' + cut_name + 'dR_q3'+ '>=' + '0.4' + ')' + '&&' + '(' + cut_name + 'dR_q4'+ '>=' + '0.4' + ')' ]
    #cut_dR = [ '(' + cut_name + 'dR_q1' + '<' + '0.4' + ')' ]
    cut_eta = [ "(" + cut_name + 'eta' + '<' + '2.4' + ')' + '&&' + '(' + cut_name + 'eta' + '>' + '-2.4' + ')' ]	
    cut_chf = [ "(" + cut_name + 'chf' + '<' + '0.2' + ')' ]
    #cut_pt = [ "(" + cut_name + 'pt' + '>' + '15' + ')' + '&&' + '(' + cut_name + 'pt'+ '>' + '68' + ')' + '&&' + '(' + cut_name + 'pt'+ '<' + '75' + ')' ]
    cut_pt = [ "(" + cut_name + 'pt' + '>' + '15' + ')' ]
    #cutting = cut_dR[0] + '&&' + cut_chf[0] + '&&' + cut_GenBquark[0]
    cutting = cut_pt[0] + '&&' + cut_dR[0] + '&&' + cut_eta[0] + '&&' + cut_GenBquark[0]
    for cc in channel:
        write_1(i[1],cc)
    plot_2(i[1])
    for cc in channel:
        clear(cc)
        hist[cc].clear()
        tree[cc].clear()
############################################

