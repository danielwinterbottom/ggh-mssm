import ROOT
import imp
from array import array

wsptools = imp.load_source('wsptools', 'workspaceTools.py')

# Boilerplate
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.RooWorkspace.imp = getattr(ROOT.RooWorkspace, 'import')
ROOT.TH1.AddDirectory(0)

ROOT.gROOT.LoadMacro("RooSpline1D.cc+")

w = ROOT.RooWorkspace('w')

map_to_add = {}

map_to_add['MH_bbH'] = []
map_to_add['xs_bbH_ybyb'] = []
map_to_add['xs_bbH_ybyb_up'] = []
map_to_add['xs_bbH_ybyb_down'] = []

map_to_add['xs_bbH_ybyt'] = []
map_to_add['xs_bbH_ybyt_up'] = []
map_to_add['xs_bbH_ybyt_down'] = []

map_to_add['MH_ggH'] = []
map_to_add['xs_ggH'] = []
map_to_add['xs_ggH_up'] = []
map_to_add['xs_ggH_t'] = []
map_to_add['xs_ggH_t_up'] = []
map_to_add['xs_ggH_b'] = []
map_to_add['xs_ggH_b_up'] = []
map_to_add['xs_ggH_i'] = []
map_to_add['xs_ggH_i_up'] = []

map_to_add['xs_ggA'] = []
map_to_add['xs_ggA_up'] = []
map_to_add['xs_ggA_t'] = []
map_to_add['xs_ggA_t_up'] = []
map_to_add['xs_ggA_b'] = []
map_to_add['xs_ggA_b_up'] = []
map_to_add['xs_ggA_i'] = []
map_to_add['xs_ggA_i_up'] = []

g1 = ROOT.TGraph()
g2 = ROOT.TGraph()
g3 = ROOT.TGraph()
g4 = ROOT.TGraph()
g5 = ROOT.TGraph()
g6 = ROOT.TGraph()

def ReadbbHFile(filename):
  datContent = [i.strip().split() for i in open(filename).readlines()][3:]
  out=[]
  for d in datContent:
    val = (float(d[0]), float(d[3]), float(d[4]), float(d[5]), float(d[6]), float(d[7]), float(d[8]), float(d[9]), float(d[10]))
    #print val
    out.append(val)
  return out

bbhfull = ReadbbHFile('BPT_summary4_NLO+NNLLpart+ybyt.dat')
bbh_yb = ReadbbHFile('BPT_summary4_NLO+NNLLpart.dat')

def GetInteference(x,y):
  # x = full, y = y_b only 
  m=x[0]
  xs=x[1]-y[1]
  u1 = x[2]-y[2]
  u2 = x[3]-y[3]
  u3 = x[4]-y[4]
  u4 = x[5]-y[5]
  u5 = x[6]-y[6]
  u6 = x[7]-y[7]
  u7 = x[8]-y[8]
  out=(m,xs,u1,u2,u3,u4,u5,u6,u7)
  return out


def GetUncert(x):

 tot_up=0
 tot_down=0
 if x[1]==0.: return (0.,0.)
 for i in range(2,9):
   if i<5 or x[i]/x[1]>0.:
     tot_up+=(x[i]/x[1])**2
   if i<5 or x[i]/x[1]<0.:
     tot_down+=(x[i]/x[1])**2
 tot_up=tot_up**.5
 tot_down=tot_down**.5
 return (tot_up,-tot_down)

for i, x in enumerate(bbhfull):
  y = bbh_yb[i]

  if y[0] == x[0]:
 
    m = y[0]

    #if m<60. or m>250.: continue

    (up,down) = GetUncert(y)
    (up_x,down_x) = GetUncert(x)

    xs_yb = y[1]

    map_to_add['MH_bbH'].append(m)
    map_to_add['xs_bbH_ybyb'].append(y[1])  
    map_to_add['xs_bbH_ybyb_up'].append((1.+up)*y[1]) 
    map_to_add['xs_bbH_ybyb_down'].append((1.+down)*y[1]) 

    map_to_add['xs_bbH_ybyt'].append(x[1])
    map_to_add['xs_bbH_ybyt_up'].append((1.+up_x)*x[1])
    map_to_add['xs_bbH_ybyt_down'].append((1.+down_x)*x[1])

fout = ROOT.TFile('xs_lowmass_yb_yt.root', 'RECREATE')

g13 = ROOT.TGraph(); g13.SetName('xs_ggA_t')
g14 = ROOT.TGraph(); g14.SetName('xs_ggA_t_up')
g15 = ROOT.TGraph(); g15.SetName('xs_ggA_b')
g16 = ROOT.TGraph(); g16.SetName('xs_ggA_b_up')
g17 = ROOT.TGraph(); g17.SetName('xs_ggA_i')
g18 = ROOT.TGraph(); g18.SetName('xs_ggA_i_up')

from pandas import read_excel

xl_file = 'Higgs_XSBR_YR4_update.xlsx'
sheet = 'YR4 BSM 13TeV'
df = read_excel(xl_file, sheet_name = sheet)

f_ws = ROOT.TFile('higgs_pt_v2.root')
ws = f_ws.Get('w')

for i in range(4,118):
  m=df.iloc[i,0]
  xs=df.iloc[i,1]
  u1=df.iloc[i,4]
  u2=df.iloc[i,5]
  xs_u = ((u1/100.)**2+(u2/100.)**2)**.5
  #g7.SetPoint(g7.GetN(), m, xs)
  #g8.SetPoint(g8.GetN(), m, 1.+u)

  ws.var("mh").setVal(m)
  ws.var("mH").setVal(m)
  ws.var("mA").setVal(m)

  xs_map = {}

  for u in ['','_scale_up','_scale_down']:

    sm_nlo = ws.function("ggH_t_2HDM_xsec%(u)s" % vars()).getVal()+ ws.function("ggH_b_2HDM_xsec%(u)s" % vars()).getVal() + ws.function("ggH_i_2HDM_xsec%(u)s" % vars()).getVal()  
    sm_A_nlo = ws.function("ggA_t_2HDM_xsec%(u)s" % vars()).getVal()+ ws.function("ggA_b_2HDM_xsec%(u)s" % vars()).getVal() + ws.function("ggA_i_2HDM_xsec%(u)s" % vars()).getVal()  
    xs_H_t = (ws.function("ggH_t_2HDM_xsec%(u)s" % vars()).getVal())/sm_nlo*xs
    xs_A_t = (ws.function("ggA_t_2HDM_xsec%(u)s" % vars()).getVal())/sm_nlo*xs
  
    xs_H_b = (ws.function("ggH_b_2HDM_xsec%(u)s" % vars()).getVal())/sm_nlo*xs
    xs_A_b = (ws.function("ggA_b_2HDM_xsec%(u)s" % vars()).getVal())/sm_nlo*xs
  
    xs_H_i = (ws.function("ggH_i_2HDM_xsec%(u)s" % vars()).getVal())/sm_nlo*xs
    xs_A_i = (ws.function("ggA_i_2HDM_xsec%(u)s" % vars()).getVal())/sm_nlo*xs
    xs_map['A_t%(u)s' % vars()] = xs_A_t
    xs_map['A_b%(u)s' % vars()] = xs_A_b
    xs_map['A_i%(u)s' % vars()] = xs_A_i

    xs_map['H_t%(u)s' % vars()] = xs_H_t
    xs_map['H_b%(u)s' % vars()] = xs_H_b
    xs_map['H_i%(u)s' % vars()] = xs_H_i

  #print '------'
  #print xs_map['H_t_scale_down']/xs_map['H_t']
  #print xs_map['H_t_scale_up']/xs_map['H_t']

  #print xs_map['H_b_scale_down']/xs_map['H_b']
  #print xs_map['H_b_scale_up']/xs_map['H_b']

  #print xs_map['H_i_scale_down']/xs_map['H_i']
  #print xs_map['H_i_scale_up']/xs_map['H_i']

  map_to_add['MH_ggH'].append(m)

  val = xs_map['H_t']
  val_u = xs_map['H_t_scale_up']
  val_d = xs_map['H_t_scale_down']
  u_nlo = ((max(val,val_u,val_d) - min(val,val_u,val_d))/2)/val
  u_tot = (u_nlo**2 +xs_u**2)**.5
#  g7.SetPoint(g7.GetN(), m, val)
#  g8.SetPoint(g8.GetN(), m, 1.+u_tot)

  map_to_add['xs_ggH'].append(xs)
  map_to_add['xs_ggH_up'].append((1.+xs_u)*xs)
  
  map_to_add['xs_ggH_t'].append(val)
  map_to_add['xs_ggH_t_up'].append((1.+u_tot)*val)

  val = xs_map['H_b']
  val_u = xs_map['H_b_scale_up']
  val_d = xs_map['H_b_scale_down']
  u_nlo = ((max(val,val_u,val_d) - min(val,val_u,val_d))/2)/val
  u_tot = (u_nlo**2 +xs_u**2)**.5

  map_to_add['xs_ggH_b'].append(val)
  map_to_add['xs_ggH_b_up'].append((1.+u_tot)*val)

  val = xs_map['H_i']
  val_u = xs_map['H_i_scale_up']
  val_d = xs_map['H_i_scale_down']
  u_nlo = ((max(val,val_u,val_d) - min(val,val_u,val_d))/2)/val
  u_tot = (u_nlo**2 +xs_u**2)**.5

  map_to_add['xs_ggH_i'].append(val)
  map_to_add['xs_ggH_i_up'].append((1.+u_tot)*val)

  map_to_add['xs_ggA'].append(xs*sm_A_nlo/sm_nlo)
  map_to_add['xs_ggA_up'].append((1.+xs_u)*xs*sm_A_nlo/sm_nlo)

  val = xs_map['A_t']
  val_u = xs_map['A_t_scale_up']
  val_d = xs_map['A_t_scale_down']
  u_nlo = ((max(val,val_u,val_d) - min(val,val_u,val_d))/2)/val
  u_tot = (u_nlo**2 +xs_u**2)**.5

  map_to_add['xs_ggA_t'].append(val)
  map_to_add['xs_ggA_t_up'].append((1.+u_tot)*val)

  val = xs_map['A_b']
  val_u = xs_map['A_b_scale_up']
  val_d = xs_map['A_b_scale_down']
  u_nlo = ((max(val,val_u,val_d) - min(val,val_u,val_d))/2)/val
  u_tot = (u_nlo**2 +xs_u**2)**.5

  map_to_add['xs_ggA_b'].append(val)
  map_to_add['xs_ggA_b_up'].append((1.+u_tot)*val)

  val = xs_map['A_i']
  val_u = xs_map['A_i_scale_up']
  val_d = xs_map['A_i_scale_down']
  u_nlo = ((max(val,val_u,val_d) - min(val,val_u,val_d))/2)/val
  u_tot = (u_nlo**2 +xs_u**2)**.5

  map_to_add['xs_ggA_i'].append(val)
  map_to_add['xs_ggA_i_up'].append((1.+u_tot)*val)

w.factory('Yt_h[1]' % vars())
w.factory('Yb_h[1]' % vars())
w.factory('Yt_H[1]' % vars())
w.factory('Yb_H[1]' % vars())
w.factory('Yt_A[1]' % vars())
w.factory('Yb_A[1]' % vars())
w.factory('mA[100,50,3000]') 
w.factory('mH[100,50,3000]')
w.factory('mh[100,50,3000]')

for P in ['A','H','h']:
  
  P_=P.upper()

  spline_gg_xsec = ROOT.RooSpline1D('gg%(P)s_xsec' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_ggH']), array('d', map_to_add['MH_ggH']), array('d', map_to_add['xs_gg%(P_)s' % vars()]), 'LINEAR')
  spline_gg_xsec_up = ROOT.RooSpline1D('gg%(P)s_xsec_up' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_ggH']), array('d', map_to_add['MH_ggH']), array('d', map_to_add['xs_gg%(P_)s_up' % vars()]), 'LINEAR')

  spline_gg_xsec_t = ROOT.RooSpline1D('gg%(P)s_t_xsec' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_ggH']), array('d', map_to_add['MH_ggH']), array('d', map_to_add['xs_gg%(P_)s_t' % vars()]), 'LINEAR')
  spline_gg_xsec_t_up = ROOT.RooSpline1D('gg%(P)s_t_xsec_up' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_ggH']), array('d', map_to_add['MH_ggH']), array('d', map_to_add['xs_gg%(P_)s_t_up' % vars()]), 'LINEAR')

  spline_gg_xsec_b = ROOT.RooSpline1D('gg%(P)s_b_xsec' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_ggH']), array('d', map_to_add['MH_ggH']), array('d', map_to_add['xs_gg%(P_)s_b' % vars()]), 'LINEAR')
  spline_gg_xsec_b_up = ROOT.RooSpline1D('gg%(P)s_b_xsec_up' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_ggH']), array('d', map_to_add['MH_ggH']), array('d', map_to_add['xs_gg%(P_)s_b_up' % vars()]), 'LINEAR')

  spline_gg_xsec_i = ROOT.RooSpline1D('gg%(P)s_i_xsec' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_ggH']), array('d', map_to_add['MH_ggH']), array('d', map_to_add['xs_gg%(P_)s_i' % vars()]), 'LINEAR')
  spline_gg_xsec_i_up = ROOT.RooSpline1D('gg%(P)s_i_xsec_up' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_ggH']), array('d', map_to_add['MH_ggH']), array('d', map_to_add['xs_gg%(P_)s_i_up' % vars()]), 'LINEAR')

  spline_bb_ybyb_xsec = ROOT.RooSpline1D('bb%(P)s_ybyb_xsec' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_bbH']), array('d', map_to_add['MH_bbH']), array('d', map_to_add['xs_bbH_ybyb' % vars()]), 'LINEAR')
  spline_bb_ybyb_xsec_up = ROOT.RooSpline1D('bb%(P)s_ybyb_xsec_up' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_bbH']), array('d', map_to_add['MH_bbH']), array('d', map_to_add['xs_bbH_ybyb_up' % vars()]), 'LINEAR')
  spline_bb_ybyb_xsec_down = ROOT.RooSpline1D('bb%(P)s_ybyb_xsec_down' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_bbH']), array('d', map_to_add['MH_bbH']), array('d', map_to_add['xs_bbH_ybyb_down' % vars()]), 'LINEAR')

  spline_bb_ybyt_xsec = ROOT.RooSpline1D('bb%(P)s_ybyt_xsec' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_bbH']), array('d', map_to_add['MH_bbH']), array('d', map_to_add['xs_bbH_ybyt' % vars()]), 'LINEAR')
  spline_bb_ybyt_xsec_up = ROOT.RooSpline1D('bb%(P)s_ybyt_xsec_up' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_bbH']), array('d', map_to_add['MH_bbH']), array('d', map_to_add['xs_bbH_ybyt_up' % vars()]), 'LINEAR')
  spline_bb_ybyt_xsec_down = ROOT.RooSpline1D('bb%(P)s_ybyt_xsec_down' % vars(), '', w.arg('m%s' % (P)), len(map_to_add['MH_bbH']), array('d', map_to_add['MH_bbH']), array('d', map_to_add['xs_bbH_ybyt_down' % vars()]), 'LINEAR')

  w.imp(spline_gg_xsec)
  w.imp(spline_gg_xsec_up)

  w.imp(spline_gg_xsec_t)
  w.imp(spline_gg_xsec_t_up)

  w.imp(spline_gg_xsec_b)
  w.imp(spline_gg_xsec_b_up)

  w.imp(spline_gg_xsec_i)
  w.imp(spline_gg_xsec_i_up)

  w.imp(spline_bb_ybyb_xsec)
  w.imp(spline_bb_ybyb_xsec_up)
  w.imp(spline_bb_ybyb_xsec_down)

  w.imp(spline_bb_ybyt_xsec)
  w.imp(spline_bb_ybyt_xsec_up)
  w.imp(spline_bb_ybyt_xsec_down)


  w.factory('expr::xs_bb%(P)s("@0*@2*@2 + (@1-@0)*@2*@3", bb%(P)s_ybyb_xsec, bb%(P)s_ybyt_xsec, Yb_%(P)s, Yt_%(P)s)' % vars())
  w.factory('expr::xs_gg%(P)s("@0", gg%(P)s_xsec)' % vars())
  w.factory('expr::xs_gg%(P)s_t("@0*@1*@1", gg%(P)s_t_xsec, Yt_%(P)s)' % vars())
  w.factory('expr::xs_gg%(P)s_b("@0*@1*@1", gg%(P)s_b_xsec, Yb_%(P)s)' % vars())
  w.factory('expr::xs_gg%(P)s_i("@0*@1*@2", gg%(P)s_i_xsec, Yt_%(P)s, Yb_%(P)s)' % vars())
  for u in ['_up','_down']:
    w.factory('expr::xs_bb%(P)s%(u)s("(@0*@2*@2 + (@1-@0)*@2*@3)/@4", bb%(P)s_ybyb_xsec%(u)s, bb%(P)s_ybyt_xsec%(u)s, Yb_%(P)s, Yt_%(P)s, xs_bb%(P)s)' % vars())
  for u in ['_up','_down']:
    w.factory('expr::xs_gg%(P)s%(u)s("@0/@1", gg%(P)s_xsec%(u)s, gg%(P)s_xsec)' % vars())
    w.factory('expr::xs_gg%(P)s_t%(u)s("@0*@1*@1/@2", gg%(P)s_t_xsec%(u)s, Yt_%(P)s, xs_gg%(P)s_t)' % vars())
    w.factory('expr::xs_gg%(P)s_b%(u)s("@0*@1*@1/@2", gg%(P)s_b_xsec%(u)s, Yb_%(P)s, xs_gg%(P)s_b)' % vars())
    w.factory('expr::xs_gg%(P)s_i%(u)s("@0*@1*@2/@3", gg%(P)s_i_xsec%(u)s, Yt_%(P)s, Yb_%(P)s, xs_gg%(P)s_i)' % vars())
  w.factory('expr::xs_gg%(P)s_down("(2-@0)", xs_gg%(P)s_up)' % vars())
  w.factory('expr::xs_gg%(P)s_t_down("(2-@0)", xs_gg%(P)s_t_up)' % vars())
  w.factory('expr::xs_gg%(P)s_b_down("(2-@0)", xs_gg%(P)s_b_up)' % vars())
  w.factory('expr::xs_gg%(P)s_i_down("(2-@0)", xs_gg%(P)s_i_up)' % vars())


w.importClassCode('RooSpline1D')

w.Print()
w.writeToFile('xs_lowmass_yb_yt.root')

w.Delete()
