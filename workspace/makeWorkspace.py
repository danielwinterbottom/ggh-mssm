#!/usr/bin/env python
import ROOT
import imp
import json
from array import array
from bisect import bisect_left
from math import pi
import argparse
import numpy as np

wsptools = imp.load_source('wsptools', 'workspaceTools.py')

parser = argparse.ArgumentParser()

parser.add_argument('--year', default='2018')

args = parser.parse_args()

def takeClosest(myList, myNumber):
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before

def GetFromTFile(str):
    f = ROOT.TFile(str.split(':')[0])
    obj = f.Get(str.split(':')[1]).Clone()
    f.Close()
    return obj


def GetNormed(str):
    h = GetFromTFile(str)
    h.Scale(1. / h.Integral(-1,-1))

    # add an extra bin at the end in place of the overflow bin
    bins =  h.GetXaxis().GetXbins()
    bins.Set(len(bins)+1)
    bins.AddAt(bins[len(bins)-2]*1.1,len(bins)-1)
    hout = ROOT.TH1D(h.GetName(),'',len(bins)-1,bins.GetArray())
    for i in range(1, h.GetNbinsX()+2):
      hout.SetBinContent(i,h.GetBinContent(i)) 
      hout.SetBinError(i,h.GetBinError(i)) 
    return hout

# Boilerplate
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.RooWorkspace.imp = getattr(ROOT.RooWorkspace, 'import')
ROOT.TH1.AddDirectory(0)

ROOT.gROOT.LoadMacro("RooSpline1D.cc+")

w = ROOT.RooWorkspace('w')


masses_pythia_2018 = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 400, 450, 600, 700, 800, 1200, 1400, 1500, 1600, 1800, 2000, 2600, 2900, 3200]

masses_pythia_2016 = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]

masses_pythia_2017 = [80, 90, 100, 110, 120, 130, 140, 180, 200, 250, 300, 350, 400, 450, 600, 700, 800, 900, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]

if args.year == '2016': masses_pythia = masses_pythia_2016
else: masses_pythia = list(set(masses_pythia_2018+masses_pythia_2017))

masses_ph = [60, 80, 100, 120, 125, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 2600, 2900, 3200, 3500]

masses_ph_alt  = [350, 400, 450, 500, 600, 700, 800, 900]

masses_f = [float(x) for x in masses_ph]

xsec = {}
with open("input/mssm_pt_weight_input_xs.txt") as f:
    for line in f:
       key = line.split()[0]
       val = line.split()[1]
       xsec[key] = float(val)

for P in ['h', 'A', 'H']:

  for u in ['','_scale_up','_scale_down']:

    w.factory('Yt_MSSM_%(P)s[1]' % vars())
    w.factory('Yb_MSSM_%(P)s[1]' % vars())
    w.factory('m%s[125,%g,%g]' % (P, min(masses_f), max(masses_f)))

    xsec_t_2HDM_ref = []
    xsec_b_2HDM_ref = []
    xsec_i_2HDM_ref = []

    for m in masses_ph:
        extra=''
        if m in masses_ph_alt and P == 'A': extra = '_alt'
        xsec_i_2HDM_ref.append(xsec['%(P)s_m%(m)s_i%(extra)s%(u)s' % vars()])
        xsec_t_2HDM_ref.append(xsec['%(P)s_m%(m)s_t%(u)s' % vars()])
        xsec_b_2HDM_ref.append(xsec['%(P)s_m%(m)s_b%(u)s' % vars()])

    spline_xsec_t_2HDM_ref = ROOT.RooSpline1D('gg%(P)s_t_2HDM_xsec%(u)s' % vars(), '', w.arg('m%s' % (P)), len(masses_f), array('d', masses_f), array('d', xsec_t_2HDM_ref), 'LINEAR')
    spline_xsec_b_2HDM_ref = ROOT.RooSpline1D('gg%(P)s_b_2HDM_xsec%(u)s' % vars(), '', w.arg('m%s' % (P)), len(masses_f), array('d', masses_f), array('d', xsec_b_2HDM_ref), 'LINEAR')
    spline_xsec_i_2HDM_ref = ROOT.RooSpline1D('gg%(P)s_i_2HDM_xsec%(u)s' % vars(), '', w.arg('m%s' % (P)), len(masses_f), array('d', masses_f), array('d', xsec_i_2HDM_ref), 'LINEAR')
    w.imp(spline_xsec_t_2HDM_ref)
    w.imp(spline_xsec_b_2HDM_ref)
    w.imp(spline_xsec_i_2HDM_ref)

    w.factory('expr::gg%(P)s_t_MSSM_xsec%(u)s("@0*(@1*@1)",gg%(P)s_t_2HDM_xsec%(u)s,Yt_MSSM_%(P)s)' % vars())
    w.factory('expr::gg%(P)s_b_MSSM_xsec%(u)s("@0*(@1*@1)",gg%(P)s_b_2HDM_xsec%(u)s,Yb_MSSM_%(P)s)' % vars())
    w.factory('expr::gg%(P)s_i_MSSM_xsec%(u)s("@0*(@1*@2)",gg%(P)s_i_2HDM_xsec%(u)s,Yt_MSSM_%(P)s,Yb_MSSM_%(P)s)' % vars())
    w.factory('expr::gg%(P)s_MSSM_xsec%(u)s("@0+@1+@2", gg%(P)s_t_MSSM_xsec%(u)s, gg%(P)s_b_MSSM_xsec%(u)s, gg%(P)s_i_MSSM_xsec%(u)s)' % vars())

    w.factory('expr::gg%(P)s_t_MSSM_frac%(u)s("@0/@1", gg%(P)s_t_MSSM_xsec%(u)s, gg%(P)s_MSSM_xsec%(u)s)' % vars())
    w.factory('expr::gg%(P)s_b_MSSM_frac%(u)s("@0/@1", gg%(P)s_b_MSSM_xsec%(u)s, gg%(P)s_MSSM_xsec%(u)s)' % vars())
    w.factory('expr::gg%(P)s_i_MSSM_frac%(u)s("@0/@1", gg%(P)s_i_MSSM_xsec%(u)s, gg%(P)s_MSSM_xsec%(u)s)' % vars())


  for u in ['','_scale_up','_scale_down','_hdamp_up','_hdamp_down']:

    for m in masses_ph:
        extra=''
        if m in masses_ph_alt and P == 'A': extra = '_alt'

        wsptools.SafeWrapHist(w, ['h_pt'],
            GetNormed('input/mssm_pt_weight_inputs.root:%(P)s_m%(m)s_i%(extra)s%(u)s' % vars()), name='%(P)s_%(m)s_i%(u)s' % vars())

        wsptools.SafeWrapHist(w, ['h_pt'],
            GetNormed('input/mssm_pt_weight_inputs.root:%(P)s_m%(m)s_t%(u)s' % vars()), name='%(P)s_%(m)s_t%(u)s' % vars())

        wsptools.SafeWrapHist(w, ['h_pt'],
            GetNormed('input/mssm_pt_weight_inputs.root:%(P)s_m%(m)s_b%(u)s' % vars()), name='%(P)s_%(m)s_b%(u)s' % vars())

for m in masses_pythia:

    extra=''
    if args.year == '2016': extra = '_2016'
    wsptools.SafeWrapHist(w, ['h_pt'],
        GetNormed('input/mssm_pt_weight_inputs.root:pythia_m%(m)s%(extra)s' % vars()), name='h_%(m)s_pythia' % vars())
  
    if m not in masses_ph: continue

    for P in ['h', 'A', 'H']:
      for u in ['','_scale_up','_scale_down','_hdamp_up','_hdamp_down']:

        # define binned weights here for mass points that exist for both pythia and powheg 
        w.factory('expr::%(P)s_%(m)s_t_ratio%(u)s("@0/@1", %(P)s_%(m)s_t%(u)s, h_%(m)s_pythia)' % vars())
        w.factory('expr::%(P)s_%(m)s_b_ratio%(u)s("@0/@1", %(P)s_%(m)s_b%(u)s, h_%(m)s_pythia)' % vars())
        w.factory('expr::%(P)s_%(m)s_i_ratio%(u)s("@0/@1", %(P)s_%(m)s_i%(u)s, h_%(m)s_pythia)' % vars())

# now use linear interpolation between mass points
masses_common = list(set(masses_pythia+masses_ph).intersection(masses_pythia).intersection(masses_ph))
masses_common.sort()
min_mass = masses_common[0]
max_mass = masses_common[-1]-1.

w.factory('expr::h_mass_round("TMath::Nint(min(max(@0,%(min_mass)s),%(max_mass)s))",h_mass[125])' % vars())

for P in ['h','H','A']:
  for u in ['','_scale_up','_scale_down','_hdamp_up','_hdamp_down']:
    for c in ['t','b','i']:

      functions = [] 

      for i in range(0,len(masses_common)-1):
        m0 = masses_common[i]
        m1 = masses_common[i+1]
     
        functions.append('%(P)s_%(m0)s_to_%(m1)s_%(c)s_ratio%(u)s' % vars())

        w.factory('expr::%(P)s_%(m0)s_to_%(m1)s_%(c)s_ratio%(u)s("(@0>=%(m0)s&&@0<%(m1)s)*((@2-@1)/(%(m1)s-%(m0)s)*(@0-%(m0)s) + @1)", h_mass_round, %(P)s_%(m0)s_%(c)s_ratio%(u)s, %(P)s_%(m1)s_%(c)s_ratio%(u)s)' % vars())
 
      func_str=''
      vars_str=''
      for i, f in enumerate(functions): 
        func_str+='@%(i)i+' % vars()
        vars_str+='%(f)s,' % vars()

      func_str=func_str[:-1]
      vars_str=vars_str[:-1]

      w.factory('expr::%(P)s_%(c)s_ratio%(u)s("%(func_str)s", %(vars_str)s)' % vars())
      

w.importClassCode('RooSpline1D')

w.Print()
if args.year == '2016':
  w.writeToFile('higgs_pt_2016_v0.root')
else:
  w.writeToFile('higgs_pt_v0.root')

w.Delete()

