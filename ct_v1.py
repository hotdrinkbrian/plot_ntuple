from __future__ import division
from ROOT import ROOT, TDirectory, TFile, gFile, TBranch, TLeaf, TTree, TH1, TH1F, TH2F, TChain, TCanvas, TLegend, gROOT, gStyle, TGraphErrors
from array import array
import math
from timeit import default_timer as timer

start= timer()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Settings~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gStyle.SetOptStat(0)
path0 = "/nfs/dust/cms/user/lbenato/RecoStudies_ntuples_v4/"
#path1 = "/afs/desy.de/user/h/hezhiyua/private/qcd_vs_ctau0p60g_v3/"
path1 = "/afs/desy.de/user/h/hezhiyua/private/qcd_vs_vbf40g_v4/"
#path0 = "D:\\py_tests\\sec_data\\RecoStudies_ntuples_v2\\"
#path1 = "D:\\py_tests\\plots\\"
#path0 = "/afs/desy.de/user/h/hezhiyua/private/sec_data/60GeV/"
#path1 = "/afs/desy.de/user/h/hezhiyua/public/qcd_vs_ctau0_vs_ctau100_ms60/"
#CHS_comparison = 0 #1 for non_CHS and CHS comparison
ct_dep = 1 #1 for ct dependence comparison
life_time = ['0','0p1','1','10','100']
life_time_float = [0.001,0.1,1,10,100]
#life_time = ['0','0p05','1','10','100','1000','10000']
#life_time_float = [0.001,0.05,1,10,100,1000,10000]
len_of_lt = len(life_time)

if ct_dep == 0:
    channel = {
               #'vbfHToBB':'VBFHToBB_M-125_13TeV_powheg_pythia8.root',
               #'vbfct0p60g':'VBFH_HToSSTobbbb_MH-125_MS-60_ctauS-0_TuneCUETP8M1_13TeV-powheg-pythia8.root'
               'zhct0p40g':'ZH_HToSSTobbbb_ZToLL_MH-125_MS-40_ctauS-0_TuneCUETP8M1_13TeV-powheg-pythia8.root',
   	       'vbfHToBB':'VBFHToBB_M-125_13TeV_powheg_pythia8.root'
              }
elif ct_dep == 1:
    channel = {}
    for lt in life_time:
        channel['ct' + lt] = '/VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-' + lt + '_TuneCUETP8M1_13TeV-powheg-pythia8.root'
    channel['qcd'] = '/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
    #channel['qcd'] = 'VBFHToBB_M-125_13TeV_powheg_pythia8.root'


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
attr = ['pt', 'eta', 'phi', 'CSV', 'chf', 'nhf', 'phf', 'elf', 'muf', 'chm', 'cm', 'nm']
#attr = ['pt','chf','nm','phf']
#attr = ['cm']

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

legends = 'vbf'
legendb = 'qcd_200-300GeV'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Settings~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

####################
def file_dict_gen(path,chann):
    fd = {}
    for cc in channel:
         fd[cc] = TFile(path + chann[cc],"r")
    return fd
####################
file_dict = file_dict_gen(path0,channel)


tree = {} #dictionary to hold all trees
hist = {}
hist_CHS = {}  # to be opt
if ct_dep == 0:    
    ##############################
    for cc in channel:
        hist[cc] = {}
        hist_CHS[cc] = {}
    ##############################
elif ct_dep == 1:     
    mean ={}        #dictionary to hold all mean values
    errors ={}      #dictionary to hold all errors
    entries_after_cut = {}
    yy ={}          #dictionary to hold all arrays of y values for TGraph
    ey ={}          #dictionary to hold all arrays of errors for TGraph
    ##############################
    for cc in channel:
        hist[cc] = {}
        hist_CHS[cc] = {} # to be opt
        mean[cc] ={}
        errors[cc] ={}
        entries_after_cut[cc] ={}
    ##############################
    entries_after_cut['qcd'] = {}
    entries_after_cut['sgn'] = {}
    yy['qcd'] ={} 
    yy['sgn'] ={}       
    ey['qcd'] ={} 
    ey['sgn'] ={} 
    #######################################
    x = array( 'd' )        # array to plot for TGraph
    ex = array( 'd' )
    for ll in life_time_float:
        x.append( ll )
        ex.append( 0.0  )
    #######################################

####################################################################################################################
def write_1(var,sample,cuts):
    for s in attr:
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
        elif sample == 'vbfHToBB':
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

        elif sample == 'zhct0p40g':
            color1 = 3

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
            #if CHS_comparison == 1:
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

        if ct_dep == 0:
            entr = tree[sample].GetEntries(cuts)
            hist[sample][s].SetLineColor(color1)
            hist[sample][s].SetLineWidth(3)
            hist[sample][s].SetTitle('cut: ' + cuts.replace('(','_').replace(')','_').replace('&&',',').replace('Jet','J').replace('GenBquark','GBQ') + '[entries:' + str(entr) + ']')
            hist_CHS[sample][s].SetLineColor(color1+44)
            hist_CHS[sample][s].SetLineWidth(3)
            #hist[sample][s].SetTitleSize(0.4,'t')
            #hist[sample][s].GetYaxis().SetTitleOffset(1.6)		
            if s == 'elf':
                hist[sample][s].SetAxisRange(0., 0.02,"Y")
                hist_CHS[sample][s].SetAxisRange(0., 0.02,"Y")
            elif s == 'muf':
                hist[sample][s].SetAxisRange(0., 0.02,"Y")  
                hist_CHS[sample][s].SetAxisRange(0., 0.02,"Y")      			
            print( hist[sample][s].GetEntries() )
        elif ct_dep == 1:
            entries_after_cut[sample][s] = tree[sample].GetEntries( cuts ) # to be optimized
            errors[sample][s] = hist[sample][s].GetStdDev() #saving errors of the histogram
            #errors[sample][s] = hist[sample][s].GetRMS()
            mean[sample][s] = hist[sample][s].GetMean()     #saving means of the histogram
####################################################################################################################

###########################################################################
def write_2(sample):
    #for cc in channel:
    for s in attr:
        yy[sample][s] = array( 'd' )     #declaring the yy array
        ey[sample][s] = array( 'd' )     #declaring the ey array    
        for ll in enumerate(life_time):
            if sample == 'qcd':
                yy[sample][s].append( mean['qcd'][s] )
                ey[sample][s].append( errors['qcd'][s] )
            else:
                yy[sample][s].append( mean['ct'+ll[1]][s] )
                ey[sample][s].append( errors['ct'+ll[1]][s] )
###########################################################################

##########################################################
def plot_2(var,cuts):
    for s in attr:
        if ct_dep == 0:
            c1 = TCanvas("c1", "Signals", 800, 800)
            c1.cd()
            c1.SetGrid()
            #gStyle.SetTitleFontSize(8.1)
            if s in ('elf', 'muf', 'chm', 'cm', 'nm'):
                c1.SetLogx()
            for cc in channel:
                hist[cc][s].Draw('colz same')
                hist_CHS[cc][s].Draw('colz same')
            legend = TLegend(0.90, 0.90, 0.99, 0.99)
            #legend.SetHeader('Samples')
            for cc in channel:
                legend.AddEntry(hist[cc][s],cc)
                legend.AddEntry(hist_CHS[cc][s],cc + 'CHS')
            legend.Draw()
            c1.Print(path1 + s + var + cuts.replace('(','_').replace(')','_').replace('&&','A').replace('>','LG').replace('<','LS').replace('=','EQ').replace('.','P').replace('-','N').replace('Jet','J').replace('GenBquark','GBQ') + ".pdf")
            c1.Update()
            c1.Close() 
            print('|||||||||||||||||||||||||||||||||||||||||||||||||||')
        elif ct_dep == 1:
            eac0 = str( entries_after_cut['ct0'][s] )
            c1 = TCanvas("c1", "Signals", 800, 800)
            c1.SetGrid()
            c1.cd()
            c1.SetLogx()
            #gr = TGraph( len_of_lt , x , yy['sgn'][s] )
            gr = TGraphErrors( len_of_lt , x , yy['sgn'][s] , ex , ey['sgn'][s] )
            gr.SetMarkerSize(1.5)
            gr.SetMarkerStyle(21)
            gr.SetLineColor(4)
            gr.SetLineWidth(4)
            gr.SetTitle('averaged ' + s + ' cut: ' + cuts.replace('(','_').replace(')','_').replace('&&',',').replace('Jet','J').replace('GenBquark','GBQ') + '[entries:' + eac0 + ']')
            gr.GetXaxis().SetTitle('decaying length (mm)')
            gr.GetYaxis().SetTitle('mean frequency')
            gr.SetName('sgn')
            gr.Draw('ACP')  # '' sets up the scattering style
            gr1 = TGraphErrors( len_of_lt , x , yy['qcd'][s] , ex , ey['qcd'][s] )
            gr1.SetMarkerSize(1.0)
            gr1.SetMarkerStyle(2)
            gr1.SetLineColor(2)
            gr1.SetLineWidth(2)
            gr1.SetName('qcd')
            #gr1.SetTitle('averaged ' + s)
            #gr1.GetXaxis().SetTitle('decaying length (mm)')
            #gr1.GetYaxis().SetTitle('mean frequency')
            gr1.Draw('CP')  # '' sets up the scattering style
            legend = TLegend(0.89, 0.89, 0.99, 0.99)
            legend.AddEntry('qcd',legendb)
            legend.AddEntry('sgn',legends)
            legend.Draw()
            c1.Print(path1 + 'mean_' + s + var + cuts.replace('(','_').replace(')','_').replace('&&','A').replace('>','LG').replace('<','LS').replace('=','EQ').replace('.','P').replace('-','N').replace('Jet','J').replace('GenBquark','GBQ') + ".pdf")
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

#===========================================================================================
#===========================================================================================
if ct_dep == 0:
    for i in jet:
        for cc in channel:
            write_1(i,cc,cutting)
        plot_2(i,cutting)
        for cc in channel:
            clear_hist(cc) 
            hist[cc].clear()
            tree.clear()   
elif ct_dep == 1:
    for i in jet:
        for cc in channel:
            write_1(i,cc,cutting)
        write_2('qcd')
        write_2('sgn')
        plot_2(i,cutting)
        for cc in channel:
            clear_hist(cc) 
            hist[cc].clear()
            tree.clear()   

for cc in channel:
    file_dict[cc].Close()
#===========================================================================================
#===========================================================================================










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
