#!/usr/bin/env python
#// Small dumb code to play with trees
#// O.Bondu, F. Bojarski (May 2014)
# Various python imports
from os import path
from math import log10, pow
import collections
# ROOT setup
import ROOT
from ROOT import TFile, TTree, TLine, TChain, TCanvas, TH1D, TLatex, TLegend, TLorentzVector
ROOT.gROOT.Reset()
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine(".x setTDRStyle.C")
#ROOT.gROOT.ForceStyle(1)
ROOT.TGaxis.SetMaxDigits(3)

c1 = TCanvas()
treedir = "/storage/data/cms/store/user/obondu/"
cmsswdir = "/home/fynu/obondu/Higgs/CMSSW_7_4_5/src/cp3_llbb/HHAnalysis"

intL = 5.590
samples = []
# samples.append([ name, typ, dirpath, subdir, file, tree, sample_cut, color, style, label , sigma , N])
#samples.append(["data", 0, treedir, "DoubleMuon/DoubleMuon_Run2015B-PromptReco-v1_2015-07-15/150715_183741/0000", "output_mc_*root", "t", "1.", ROOT.kBlack, 1, "data", 1, 84874])
#samples.append(["ggX0HH_M260", -2600, treedir, "GluGluToRadionToHHTo2B2VTo2L2Nu_M-260_narrow_13TeV-madgraph/GluGluToRadionToHHTo2B2VTo2L2Nu_M-260_narrow_Asympt25ns/150715_121230/0000", "output_mc_*.root", "t", "1.", ROOT.kRed+2, 0, "mR 260 GeV" , 1000., 300000])
#samples.append(["ggX0HH_M270", -2700, treedir, "GluGluToRadionToHHTo2B2VTo2L2Nu_M-270_narrow_13TeV-madgraph/GluGluToRadionToHHTo2B2VTo2L2Nu_M-270_narrow_Asympt25ns/150715_121450/0000/", "output_mc_*.root", "t", "1.", ROOT.kMagenta+2, 0, "mR 270 GeV" , 1000., 298400])
#samples.append(["ggX0HH_M300", -3000, treedir, "GluGluToRadionToHHTo2B2VTo2L2Nu_M-300_narrow_13TeV-madgraph/GluGluToRadionToHHTo2B2VTo2L2Nu_M-300_narrow_Asympt25ns/150715_123323/0000/", "output_mc_*.root", "t", "1.", ROOT.kBlue+2, 0, "mR 300 GeV" , 1000., 299200])
samples.append(["ggX0HH_M300", -3000, cmsswdir, "", "output_mc.root", "t", "1.", ROOT.kBlue+2, 0, "mR 300 GeV" , 1000., 2000])
#samples.append(["ggX0HH_M350", -3500, treedir, "GluGluToRadionToHHTo2B2VTo2L2Nu_M-350_narrow_13TeV-madgraph/GluGluToRadionToHHTo2B2VTo2L2Nu_M-350_narrow_Asympt25ns/150715_124549/0000/", "output_mc_*.root", "t", "1.", ROOT.kCyan+2, 0, "mR 350 GeV" , 1000., 299200])
#samples.append(["ggX0HH_M400", -4000, treedir, "GluGluToRadionToHHTo2B2VTo2L2Nu_M-400_narrow_13TeV-madgraph/GluGluToRadionToHHTo2B2VTo2L2Nu_M-400_narrow_Asympt25ns/150715_125012/0000/", "output_mc_*.root", "t", "1.", ROOT.kGreen+2, 0, "mR 400 GeV" , 1000., 300000])
#samples.append(["ggX0HH_M450", -4500, treedir, "GluGluToRadionToHHTo2B2VTo2L2Nu_M-450_narrow_13TeV-madgraph/GluGluToRadionToHHTo2B2VTo2L2Nu_M-450_narrow_Asympt25ns/150715_125720/0000/", "output_mc_*.root", "t", "1.", ROOT.kYellow+2, 0, "mR 450 GeV" , 1000., 300000])
#samples.append(["ggX0HH_M500", -5000, treedir, "GluGluToRadionToHHTo2B2VTo2L2Nu_M-500_narrow_13TeV-madgraph/GluGluToRadionToHHTo2B2VTo2L2Nu_M-500_narrow_Asympt25ns/150709_161544/0000/", "output_mc_*.root", "t", "1.", ROOT.kBlue+2, 0, "mR 500 GeV" , 1., 295600])
#samples.append(["TTbar", 1, '/home/fynu/obondu/Higgs/CMSSW_7_4_5/src/cp3_llbb/HHAnalysis', '', 'output_mc_TTbar.root', 't', '1.', ROOT.kSpring-6, 1001, "t#bar{t}", 831.76, 49483])
#samples.append(["DY", 2, '/home/fynu/obondu/Higgs/CMSSW_7_4_5/src/cp3_llbb/HHAnalysis', '', 'output_mc_DY.root', 't', '1.', ROOT.kOrange-6, 1001, "DY", 6025.2, 4537])

#####plots.append([ name2, variable, plot_cut, norm, binning, title, additional_info, cutline, cutline2 ])
plots = []
# get on with matching
plots.append(["mumu_muon1_has_matched_gen_particle", "muon_has_matched_gen_particle[0]", "mumu_category", 1, "(2, 0, 2)", "#mu1 has matched gen", "#mu#mu cat.", "", ""])
plots.append(["mumu_muon2_has_matched_gen_particle", "muon_has_matched_gen_particle[1]", "mumu_category", 1, "(2, 0, 2)", "#mu2 has matched gen", "#mu#mu cat.", "", ""])
plots.append(["mumu_gen_iL1", "(hh_gen_iL1 != -1)", "mumu_category", 1, "(2, 0, 2)", "genL1 found", "#mu#mu cat.", "", ""])
plots.append(["mumu_gen_iL2", "(hh_gen_iL2 != -1)", "mumu_category", 1, "(2, 0, 2)", "genL2 found", "#mu#mu cat.", "", ""])
plots.append(["mumu_gen_deltaR_muon1_L1", "hh_gen_deltaR_muon_L1[0]", "mumu_category && muon_has_matched_gen_particle[0] && (hh_gen_iL1 != -1)", 1, "(50, 0, 5)", "#Delta R(#mu1, genL1)", "#mu#mu cat.", "", ""])
plots.append(["mumu_gen_deltaR_muon1_L2", "hh_gen_deltaR_muon_L2[0]", "mumu_category && muon_has_matched_gen_particle[0] && (hh_gen_iL2 != -1)", 1, "(50, 0, 5)", "#Delta R(#mu1, genL2)", "#mu#mu cat.", "", ""])
plots.append(["mumu_gen_deltaR_muon2_L1", "hh_gen_deltaR_muon_L1[1]", "mumu_category && muon_has_matched_gen_particle[1] && (hh_gen_iL1 != -1)", 1, "(50, 0, 5)", "#Delta R(#mu2, genL1)", "#mu#mu cat.", "", ""])
plots.append(["mumu_gen_deltaR_muon2_L2", "hh_gen_deltaR_muon_L2[1]", "mumu_category && muon_has_matched_gen_particle[1] && (hh_gen_iL2 != -1)", 1, "(50, 0, 5)", "#Delta R(#mu2, genL2)", "#mu#mu cat.", "", ""])

# basic kinematics, no cut
#plots.append(["mumu_jet1_pt", "jet_p4[0].Pt()", "mumu_category", 1, "(300, 0, 300)", "p_{T}^{jet1} (GeV)", "#mu#mu cat.", "", ""])
#plots.append(["mumu_jet2_pt", "jet_p4[1].Pt()", "mumu_category", 1, "(300, 0, 300)", "p_{T}^{jet2} (GeV)", "#mu#mu cat.", "", ""])
#plots.append(["mumu_muon1_pt", "muon_p4[0].Pt()", "mumu_category", 1, "(100, 0, 100)", "p_{T}^{muon1} (GeV)", "#mu#mu cat.", "", ""])
#plots.append(["mumu_muon2_pt", "muon_p4[1].Pt()", "mumu_category", 1, "(100, 0, 100)", "p_{T}^{muon2} (GeV)", "#mu#mu cat.", "", ""])
#plots.append(["mumu_met_pt", "met_p4[0].Pt()", "mumu_category", 1, "(100, 0, 500)", "p_{T}^{met} (GeV)", "#mu#mu cat.", "", ""])
#
#plots.append(["elel_jet1_pt", "jet_p4[0].Pt()", "elel_category", 1, "(300, 0, 300)", "p_{T}^{jet1} (GeV)", "ee cat.", "", ""])
#plots.append(["elel_jet2_pt", "jet_p4[1].Pt()", "elel_category", 1, "(300, 0, 300)", "p_{T}^{jet2} (GeV)", "ee cat.", "", ""])
#plots.append(["elel_electron1_pt", "electron_p4[0].Pt()", "elel_category", 1, "(100, 0, 100)", "p_{T}^{electron1} (GeV)", "ee cat.", "", ""])
#plots.append(["elel_electron2_pt", "electron_p4[1].Pt()", "elel_category", 1, "(100, 0, 100)", "p_{T}^{electron2} (GeV)", "ee cat.", "", ""])
#plots.append(["elel_met_pt", "met_p4[0].Pt()", "elel_category", 1, "(100, 0, 500)", "p_{T}^{met} (GeV)", "ee cat.", "", ""])
#
#plots.append(["muel_jet1_pt", "jet_p4[0].Pt()", "muel_category", 1, "(300, 0, 300)", "p_{T}^{jet1} (GeV)", "#mu e cat.", "", ""])
#plots.append(["muel_jet2_pt", "jet_p4[1].Pt()", "muel_category", 1, "(300, 0, 300)", "p_{T}^{jet2} (GeV)", "#mu e cat.", "", ""])
#plots.append(["muel_muon1_pt", "muon_p4[0].Pt()", "muel_category", 1, "(100, 0, 100)", "p_{T}^{muon1} (GeV)", "#mu e cat.", "", ""])
#plots.append(["muel_electron2_pt", "electron_p4[1].Pt()", "muel_category", 1, "(100, 0, 100)", "p_{T}^{electron2} (GeV)", "#mu e cat.", "", ""])
#plots.append(["muel_met_pt", "met_p4[0].Pt()", "muel_category", 1, "(100, 0, 500)", "p_{T}^{met} (GeV)", "#mu e cat.", "", ""])
#
#plots.append(["elmu_jet1_pt", "jet_p4[0].Pt()", "elmu_category", 1, "(300, 0, 300)", "p_{T}^{jet1} (GeV)", "e#mu cat.", "", ""])
#plots.append(["elmu_jet2_pt", "jet_p4[1].Pt()", "elmu_category", 1, "(300, 0, 300)", "p_{T}^{jet2} (GeV)", "e#mu cat.", "", ""])
#plots.append(["elmu_electron1_pt", "electron_p4[0].Pt()", "elmu_category", 1, "(100, 0, 100)", "p_{T}^{electron1} (GeV)", "e#mu cat.", "", ""])
#plots.append(["elmu_muon2_pt", "muon_p4[1].Pt()", "elmu_category", 1, "(100, 0, 100)", "p_{T}^{muon2} (GeV)", "e#mu cat.", "", ""])
#plots.append(["elmu_met_pt", "met_p4[0].Pt()", "elmu_category", 1, "(100, 0, 500)", "p_{T}^{met} (GeV)", "e#mu cat.", "", ""])

for name2, variable, plot_cut, norm, binning, title, additional_info, cutline, cutline2 in plots:
    c1 = TCanvas()
    legend = TLegend(0.45, 0.82, 0.90, 0.93, "")
    legend.SetTextSize(0.015)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetLineColor(ROOT.kWhite)
    legend.SetShadowColor(ROOT.kWhite)
    xnbin, xlow, xhigh = map(float, binning.strip().strip("()").split(","))
    ymax = -1
    ymin = 10000000
    firsthistname = ""
    if plot_cut == "": plot_cut = "1"
    hist_signal = {}
    hist_data = {}
    hist_bkg = {}
    label_signal = {}
    label_data = {}
    label_bkg = {}

    for ifile, [ name, typ, dirpath, subdir, file, tree, sample_cut, color, style, label , sigma , N] in enumerate(samples):
#        print ""
#        print ifile, file, color, style, label, typ
        chain = TChain(tree)
        chain.Add( path.join(dirpath, subdir, file) )
        total_cut = plot_cut
        if sample_cut == "": sample_cut = "1"
        if typ < 0:
            total_cut = "(" + plot_cut + ") * (" + str(sigma) + " * " + str(intL) + ")/" + str(N)
        elif typ == 0:
           total_cut = "(" + plot_cut + ") * (" + sample_cut + ")"
        elif typ > 0:
           total_cut = "(" + plot_cut + ") * (" + sample_cut + ")"
        option = ""
        if ifile != 0:
            option = "same"
        if typ == 0:
            option += "e1"
        chain.Draw(variable + ">>h_tmp" + binning, total_cut, option)
        # Cosmetics
        h = ROOT.gDirectory.Get("h_tmp")
#        h.UseCurrentStyle()
#        print h.GetEntries()
        try:
            h.SetName(name + "_" + name2 + "_" + str(ifile))
        except AttributeError:
            print "#INFO: Empty histogram for contribution ", name + "_" + name2 + "_" + str(ifile)
            continue
        if ifile == 0:
            firsthistname = name + "_" + name2 + "_" + str(ifile)
        h.SetLineWidth(2)
        h.SetLineColor(color)
        h.SetFillColor(color)
        h.SetFillStyle(style)
        h.SetMarkerColor(color)
        h.SetMarkerSize(1)
        h.SetMarkerStyle(1)
        h.GetXaxis().SetTitle( title )
        unit = ""
        if title.find("[") != -1:
            unit = title[title.find("[")+1:title.find("]")]
        if norm == 1. or norm == 1:
            h.GetYaxis().SetTitle( "Norm. to unity / ( " + str(((xhigh - xlow) / xnbin)) + " " + unit + " )")
        elif norm == "data" or norm == "Data":
            h.GetYaxis().SetTitle( "Norm. to data / ( " + str(((xhigh - xlow) / xnbin)) + " " + unit + " )")
        else:
            h.GetYaxis().SetTitle( "# events / ( " + str(((xhigh - xlow) / xnbin)) + " " + unit + " )")
        # store histo for redraw in the correct order later
        if typ > 0:
            label_bkg[typ] = label
            if typ not in hist_bkg:
                hist_bkg[typ] = h
            else:
                hist_bkg[typ].Add(h)
        elif typ == 0:
            label_data[typ] = label
            hist_data[typ] = h
        elif typ < 0:
            label_signal[typ] = label
            hist_signal[typ] = h
        del chain, h

#        print "hist_bkg=", hist_bkg
#        print "hist_signal=", hist_signal
#        print "hist_data=", hist_data

    # Sum the backgrounds
#    print ""
#    print "1: ", hist_bkg.items()
#    print "2: ", sorted(hist_bkg.items())
#    print "3: ", collections.OrderedDict(sorted(hist_bkg.items()))
    for key in collections.OrderedDict(sorted(hist_bkg.items())):
#        print "hist_bkg[key].GetEntries()= ", hist_bkg[key].GetEntries()
        for jkey in collections.OrderedDict(sorted(hist_bkg.items())):
            if jkey <= key: continue
            hist_bkg[key].Add(hist_bkg[jkey])
#            print "hist_bkg[key].GetEntries()= ", hist_bkg[key].GetEntries()
    # Adjust norm if case happens
    if norm == 1. or norm == 1:
        bkg_integral = 1.
        for ikey, key in enumerate(collections.OrderedDict(sorted(hist_bkg.items()))):
            if ikey == 0:
                bkg_integral = hist_bkg[key].Integral(0, hist_bkg[key].GetNbinsX() + 1)
            hist_bkg[key].Scale( 1. / bkg_integral )
        data_integral = 1.
        for ikey, key in enumerate(collections.OrderedDict(sorted(hist_data.items()))):
            if ikey == 0:
                data_integral = hist_data[key].Integral(0, hist_data[key].GetNbinsX() +1)
            hist_data[key].Scale( 1. / data_integral )
        signal_integral = 1.
        for ikey, key in enumerate(collections.OrderedDict(sorted(hist_signal.items()))):
            if ikey == 0:
                signal_integral = hist_signal[key].Integral(0, hist_signal[key].GetNbinsX() +1)
            hist_signal[key].Scale( 1. / signal_integral )
    elif norm == "data" or norm == "Data":
        data_integral = 1.
        for ikey, key in enumerate(collections.OrderedDict(sorted(hist_data.items()))):
            if ikey == 0:
                data_integral = hist_data[key].Integral(0, hist_data[key].GetNbinsX() +1)
            else:
                continue
#        print "data_integral= ", data_integral
        bkg_integral = 1.
        for ikey, key in enumerate(collections.OrderedDict(sorted(hist_bkg.items()))):
#            print ikey, key, hist_bkg[key].GetEntries(), hist_bkg[key].Integral(0, hist_bkg[key].GetNbinsX() + 1)
            if ikey == 0:
                bkg_integral = hist_bkg[key].Integral(0, hist_bkg[key].GetNbinsX() + 1)
            hist_bkg[key].Scale( data_integral / bkg_integral )
        signal_integral = 1.
        for ikey, key in enumerate(collections.OrderedDict(sorted(hist_signal.items()))):
            if ikey == 0:
                signal_integral = hist_signal[key].Integral(0, hist_signal[key].GetNbinsX() +1)
            hist_signal[key].Scale( data_integral / signal_integral )
    # redraw in order : background, data, signal, axis
    if len(hist_bkg) + len(hist_data) + len(hist_signal) > 1:
        legend.SetNColumns(2)
    if len(hist_bkg) + len(hist_data) + len(hist_signal) > 6:
        legend.SetNColumns(3)
    for ikey, key in enumerate(collections.OrderedDict(sorted(hist_bkg.items()))):
        if ikey == 0:
            hist_bkg[key].Draw("")
            firsthistname = hist_bkg[key].GetName()
        else:
            hist_bkg[key].Draw("same")
        legend.AddEntry(hist_bkg[key].GetName(), label_bkg[key], "lf")
        ymax = max(ymax, hist_bkg[key].GetMaximum())
        ymin = min(ymin, hist_bkg[key].GetMinimum(0.0))
    for key in hist_data:
        hist_data[key].Draw("e1same")
        legend.AddEntry(hist_data[key].GetName(), label_data[key], "lpe")
        ymax = max(ymax, hist_data[key].GetMaximum())
        ymin = min(ymin, hist_data[key].GetMinimum(0.0))
    for key in collections.OrderedDict(sorted(hist_signal.items())):
        hist_signal[key].Draw("histsame")
        ROOT.gPad.Modified()
        c1.Update()
        legend.AddEntry(hist_signal[key].GetName(), label_signal[key], "lf")
        ymax = max(ymax, hist_signal[key].GetMaximum())
        ymin = min(ymin, hist_signal[key].GetMinimum(0.0))
    ymin_lin = ymin / 10.
    yrange_lin = ymax - ymin_lin
    ymax_lin = .25 * yrange_lin + ymax
    yrange_log = (log10(ymax) - log10(ymin)) / .77
    ymax_log = pow(10., .25*yrange_log + log10(ymax))
    ymin_log = pow(10., log10(ymin) - .03*yrange_log)

    latexLabel = TLatex()
    latexLabel.SetTextSize(0.75 * c1.GetTopMargin())
    latexLabel.SetNDC()
    latexLabel.SetTextFont(42) # helvetica
    if norm == 1.:
        latexLabel.DrawLatex(0.80, 0.96, "(13 TeV)")
    else:
        if intL > 1000.:
            latexLabel.DrawLatex(0.70, 0.96, str(intL) + "/fb (13 TeV)")
        else:
            latexLabel.DrawLatex(0.70, 0.96, str(intL) + "/pb (13 TeV)")
    latexLabel.SetTextFont(61) # helvetica bold face
    latexLabel.DrawLatex(0.17, 0.89, "CMS")
    latexLabel.SetTextFont(52) # helvetica italics
    latexLabel.DrawLatex(0.17, 0.85, "Internal")
    latexLabel.SetTextSize(.04)
    latexLabel.DrawLatex(.30, .85, additional_info)
    ROOT.gPad.RedrawAxis()
    legend.Draw()
    c1.Update()

    line = TLine()
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line2 = TLine()
    line2.SetLineStyle(2)
    line2.SetLineWidth(2)

    h = ROOT.gDirectory.Get(firsthistname)
    h.SetMaximum(ymax_lin)
    h.SetMinimum(ymin_lin)
    if cutline != "":
        line.SetX1(cutline); line.SetY1(ymin_lin); line.SetX2(cutline); line.SetY2(ymax)
        line.Draw("same")
    if cutline2 != "":
        line2.SetX1(cutline2); line2.SetY1(ymin_lin); line2.SetX2(cutline2); line2.SetY2(ymax)
        line2.Draw("same")
    c1.Update()
    c1.Print("png/" + name2 + ".png")
    c1.Print("pdf/" + name2 + ".pdf")
    c1.Print("gif/" + name2 + ".gif")
    c1.Print("root/" + name2 + ".root")


    c1.SetLogy(1)
    h.SetMaximum(ymax_log)
    h.SetMinimum(ymin_log)
    h.GetYaxis().SetRangeUser(ymin_log, ymax_log)
    if cutline != "":
        line.SetX1(cutline); line.SetY1(ymin_log); line.SetX2(cutline); line.SetY2(ymax)
        line.Draw("same")
    if cutline2 != "":
        line2.SetX1(cutline2); line2.SetY1(ymin_log); line2.SetX2(cutline2); line2.SetY2(ymax)
        line2.Draw("same")
    c1.Update()
    c1.Print("png/" + name2 + "_log.png")
    c1.Print("pdf/" + name2 + "_log.pdf")
    c1.Print("gif/" + name2 + "_log.gif")
    c1.Print("root/" + name2 + "_log.root")
    c1.SetLogy(0)

    del c1
