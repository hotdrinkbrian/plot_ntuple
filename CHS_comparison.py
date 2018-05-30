from __future__ import division
from ROOT import ROOT, TDirectory, TFile, gFile, TBranch, TLeaf, TTree, TH1, TH1F, TH2F, TChain, TCanvas, TLegend, gROOT, gStyle
import math
from timeit import default_timer as timer

start= timer()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Settings~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gStyle.SetOptStat(0)
path0 = "/nfs/dust/cms/user/lbenato/RecoStudies_ntuples_v4/"
#path1 = "/afs/desy.de/user/h/hezhiyua/private/qcd_vs_ctau0p60g_v3/"
path1 = "/afs/desy.de/user/h/hezhiyua/private/vbf_vs_zh40g0mm_v1/"
#path0 = "D:\\py_tests\\sec_data\\RecoStudies_ntuples_v2\\"
#path1 = "D:\\py_tests\\plots\\"
#path0 = "/afs/desy.de/user/h/hezhiyua/private/sec_data/60GeV/"
#path1 = "/afs/desy.de/user/h/hezhiyua/public/qcd_vs_ctau0_vs_ctau100_ms60/"
"""
channel = {
           #'qcd':'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
           #'ttt':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root',
           'vbfHToBB':'VBFHToBB_M-125_13TeV_powheg_pythia8.root',
           'vbfct0p60g':'VBFH_HToSSTobbbb_MH-125_MS-60_ctauS-0_TuneCUETP8M1_13TeV-powheg-pythia8_PRIVATE-MC.root'
           #'vbfct100p60g':'VBFH_HToSSTobbbb_MH-125_MS-60_ctauS-100_TuneCUETP8M1_13TeV-powheg-pythia8_PRIVATE-MC.root'	   
          }
"""

channel = {
           'ttt':'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root',
           'qcd':'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
           #'vbfct0p60g':'VBFH_HToSSTobbbb_MH-125_MS-60_ctauS-0_TuneCUETP8M1_13TeV-powheg-pythia8.root',
           'vbfct0p40g':'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-0_TuneCUETP8M1_13TeV-powheg-pythia8.root',
           #'zhct0p40g':'ZH_HToSSTobbbb_ZToLL_MH-125_MS-40_ctauS-0_TuneCUETP8M1_13TeV-powheg-pythia8.root',
   	   'vbfHToBB':'VBFHToBB_M-125_13TeV_powheg_pythia8.root'
          }

twoD = 0 # 2D plot option: 0 --> 1D
CHS = 0 # CHS jet option: 0 --> off
number_of_bin = 100
num_of_jets = 1
#attr = ['pt']
#attr = ['chm','cm']
#attr = ['CSV', 'chf']
#attr = ['chf','chm','cm','pt']
#attr = ['dR_q1','dR_q2','dR_q3','dR_q4']
#attr = ['pt', 'nhf', 'phf', 'elf', 'muf']
#attr = ['pt', 'eta', 'phi', 'CSV', 'chf', 'nhf', 'phf', 'elf', 'muf', 'chm', 'cm', 'nm']
attr = ['pt', 'CSV', 'chf', 'nhf', 'phf', 'chm', 'cm', 'nm']
#attr = ['pt','chf','nm','phf']
#attr = ['nhf']

####################################generating list with 10 Jets
def jet_list_gen(n):
    jl = []
    for ii in range(1,n+1): 
        if CHS == 0:
            jl.append('Jet' + "%s" %ii)
        elif CHS == 1:
            jl.append('CHSJet' + "%s" %ii)
    return jl
####################################generating list with 10 Jets
jet = jet_list_gen(num_of_jets)

#++++++++++++++++++++++++++++cuts+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
########################################################################
def cut_dict_gen(cut_name):
    cut_dict = {}
    cut_dict['pt'] =  '(' + cut_name + 'pt' + '>' + '15' + ')' # + '&&' + '(' + cut_name + 'pt' + '>' + '70' + ')' + '&&' + '(' + cut_name + 'pt' + '<' + '75' + ')'  
       
    cut_dict['eta'] = '(' + cut_name + 'eta' + '<' + '2.4' + ')' + '&&' + '(' + cut_name + 'eta' + '>' + '-2.4' + ')'
    cut_dict['dR'] = '(' + cut_name + 'dR_q1' + '<' + '0.4' + ')' + '&&' + '(' + cut_name + 'dR_q2'+ '>=' + '0.4' + ')' + '&&' + '(' + cut_name + 'dR_q3'+ '>=' + '0.4' + ')' + '&&' + '(' + cut_name + 'dR_q4'+ '>=' + '0.4' + ')'
    cut_dict['chf'] = ''
    #cut_dict['GenBquark'] = '(GenBquark1.pt>15)&&(GenBquark1.eta<2.4)&&(GenBquark1.eta>-2.4)' 
    return cut_dict
########################################################################
###################################################################################################
def cutting_gen(pref):
    for i in jet:
        cuts = cut_dict_gen( pref + i + '.'  )
    cuttings = cuts['pt'] + '&&' + cuts['eta'] + '&&' + cuts['dR']  #+ '&&' + cut_dict['GenBquark']
    return cuttings
###################################################################################################
cutting = cutting_gen('')
print('---------cut:')
print(cutting)
cutting_CHS = cutting_gen('CHS')
print('---------cut_CHS:')
print(cutting_CHS)
#++++++++++++++++++++++++++++cuts+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Settings~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

####################
def file_dict_gen(path,chann):
    fd = {}
    for cc in channel:
         fd[cc] = TFile(path + chann[cc],"r")
    return fd
####################
file_dict = file_dict_gen(path0,channel)

plotrange = {}
tree = {}
hist = {}
hist_CHS = {}
##############################
for cc in channel:
    hist[cc] = {}
    hist_CHS[cc] = {}
##############################


####################################################################################################################
def write_1(var,sample,cuts):
    for s in attr:
        if sample == 'qcd':
            color1 = 3
        elif sample == 'ttt':
            color1 = 2  #880+1 #400+3	
        elif sample == 'ct0':
            color1 = 8  #634
        elif sample == 'ct0p05':
            color1 = 3
        elif sample == 'ct1':
            color1 = 2
        elif sample == 'ct100':
            color1 = 6	
        elif sample == 'vbfHToBB':
            color1 = 7  #800+10
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

        elif sample == 'zhct0p40g':
            color1 = 3
        elif sample == 'vbfct0p40g':
            color1 = 4 


        if s == 'pt':
            h_par = [number_of_bin,0,300]
        elif s == 'eta':
            h_par = [number_of_bin,-2.5,2.5]
        elif s == 'phi':
            h_par = [number_of_bin,-math.pi,math.pi]
        elif s == 'CSV':
            h_par = [number_of_bin,0,1]
        elif s == 'chf':
            h_par = [number_of_bin,0,1]
        elif s == 'nhf':
            h_par = [number_of_bin,0,1]
        elif s == 'phf':
            h_par = [number_of_bin,0,1]
        elif s == 'elf':
            h_par = [number_of_bin,0,1]
        elif s == 'muf':
            h_par = [number_of_bin,0,1]
        elif s == 'chm':
            h_par = [number_of_bin,0,100]
        elif s == 'chm':
            h_par = [number_of_bin,0,100]
        elif s == 'cm':
            h_par = [number_of_bin,0,100]
        elif s == 'nm':
            h_par = [number_of_bin,0,100]
        elif s == 'dR_q1':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s == 'dR_q2':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s == 'dR_q3':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s == 'dR_q4':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s == 'nPV':
            h_par = [number_of_bin,0,80]

        tree[sample] = file_dict[sample].Get('reconstruction;1').Get('tree') #.Get('ntuple;1').Get('tree')
        if twoD == 0:
            hist[sample][s] = TH1F(sample+s, '; %s; events' %s , h_par[0], h_par[1], h_par[2])
            hist_CHS[sample][s] = TH1F(sample+s + 'CHS', '; %s; events' %s , h_par[0], h_par[1], h_par[2])
        elif twoD == 1:
            hist[sample][s] = TH2F(sample+s, '; %s; events' %s , h_par[0], h_par[1], h_par[2] , number_of_bin, 0, 300)
            hist_CHS[sample][s] = TH2F(sample+s +'CHS', '; %s; events' %s , h_par[0], h_par[1], h_par[2] , number_of_bin, 0, 300)
        print( tree[sample] )
        hist[sample][s].Sumw2()
        hist_CHS[sample][s].Sumw2()

        if twoD == 0:
            tree[sample].Project(sample+s, var + '.' + s, cuts ) 
            tree[sample].Project(sample+s+'CHS', 'CHS' + var + '.' + s, cuts + '_CHS' )
        elif twoD == 1:
            tree[sample].Project(sample+s, var + '.' + s + ':' + var + '.' + 'pt', cuts ) 
            tree[sample].Project(sample+s+'CHS', 'CHS' + var + '.' + s + ':' + var + '.' + 'pt', cuts + '_CHS' )              

        if hist[sample][s].Integral() != 0 and hist_CHS[sample][s].Integral() != 0:
            hist[sample][s].Scale(1/float(hist[sample][s].Integral()))
            hist_CHS[sample][s].Scale(1/float(hist_CHS[sample][s].Integral()))   
        else:
            print("zero denominator!")
        entr = tree[sample].GetEntries(cuts)
        hist[sample][s].SetLineColor(color1)
        hist[sample][s].SetLineWidth(3)
        hist[sample][s].SetTitle('cut: ' + cuts.replace('(','_').replace(')','_').replace('&&',',').replace('Jet','J').replace('GenBquark','GBQ') + '[entries:' + str(entr) + ']')
        hist_CHS[sample][s].SetLineColor(color1+44)
        hist_CHS[sample][s].SetLineWidth(3)
        #hist[sample][s].SetTitleSize(0.4,'t')
        #hist[sample][s].GetYaxis().SetTitleOffset(1.6)	
        	
        plotrange[s] =  max( plotrange[s] , hist[sample][s].GetMaximum() )
        print( 'Entries:' )  			
        print( hist[sample][s].GetEntries() )
####################################################################################################################

##########################################################
def plot_2(var,cuts):
    for s in attr:
        c1 = TCanvas("c1", "Signals", 800, 800)
        c1.cd()
        c1.SetGrid()
        #gStyle.SetTitleFontSize(8.1)
        if s in ('elf', 'muf', 'chm', 'cm', 'nm'):
            c1.SetLogx()
        for cc in channel:
            #hist[cc][s].SetMaximum(0.44)
            hist[cc][s].Draw('colz same')
            if CHS == 1:
                hist_CHS[cc][s].Draw('colz same')
        legend = TLegend(0.90, 0.90, 0.99, 0.99)
        #legend.SetHeader('Samples')
        for cc in channel:
            legend.AddEntry(hist[cc][s],cc)
            if CHS == 1:
                legend.AddEntry(hist_CHS[cc][s],cc + 'CHS')
        legend.Draw()
        c1.Print(path1 + s + var + cuts.replace('(','_').replace(')','_').replace('&&','A').replace('>','LG').replace('<','LS').replace('=','EQ').replace('.','P').replace('-','N').replace('Jet','J').replace('GenBquark','GBQ') + ".pdf")
        c1.Update()
        c1.Close() 
        print('|||||||||||||||||||||||||||||||||||||||||||||||||||')
##########################################################

########################################################################
def clear_hist(sample):
    for s in attr:
        if gROOT.FindObject( sample+s ) != None:
            hh = gROOT.FindObject( sample+s ) #to find the histogram
            hh.Delete()    #to delete the histogram
        if gROOT.FindObject( sample+s+'CHS' ) != None:
            hhchs = gROOT.FindObject( sample+s+'CHS' ) #to find the histogram
            hhchs.Delete()    #to delete the histogram
########################################################################

########################################################################
def set_hist_yrange():
    os = 1.14
    for cc in channel:
        for s in attr:
            hist[cc][s].SetMaximum( plotrange[s] * os )
            hist_CHS[cc][s].SetMaximum( plotrange[s] *os )
            if s == 'elf':
                hist[cc][s].SetAxisRange(0., 0.02,"Y")
                hist_CHS[cc][s].SetAxisRange(0., 0.02,"Y")
            elif s == 'muf':
                hist[cc][s].SetAxisRange(0., 0.02,"Y")  
                hist_CHS[cc][s].SetAxisRange(0., 0.02,"Y")        
########################################################################

########################################################################
def init_plotrange():
    for s in attr:
        plotrange[s] = 0           
########################################################################

#===========================================================================================
#===========================================================================================
for i in jet:

    init_plotrange()       

    for cc in channel:
        write_1(i,cc,cutting)

    set_hist_yrange()
    plot_2(i,cutting)

    plotrange.clear()
    for cc in channel:
        clear_hist(cc) 
        hist[cc].clear()
        tree.clear() 
          
for cc in channel:
        file_dict[cc].Close()
#===========================================================================================
#===========================================================================================

"""
if ct_dep == 1:
    life_time = []
    life_time_float = []
    len_of_lt = len(life_time)
    x = array( 'd' )        # array to plot for TGraph
    ex = array( 'd' )

    #######################################
    for ll in enumerate( life_time_float ):
        x.append( ll[1] )
        ex.append( 0.0  )
    #######################################
    file_dict['qcd_200'] = TFile(path0 + "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root","r")

    for cc in enumerate(life_time):
        file_dict['sgn_' + cc[1]] = TFile(path0 + "ZH_HToSSTobbbb_ZToLL_MH-125_MS-40_ctauS-" + cc[1] + "_TuneCUETP8M1_13TeV-powheg-pythia8.root","r")

"""









end = timer() 
print("Time taken:", end-start) 
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
