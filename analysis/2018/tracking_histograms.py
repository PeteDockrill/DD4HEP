# Must initialise session before running!

from __future__ import division
import argparse
import copy
import math
import numpy as np
import pandas as pd
import pyLCIO
import ROOT
import extracttrack
import histwrap

#CMD Arguments
#TODO: add way to plot only MCParticle/SiTrack/CATrack
parser = argparse.ArgumentParser(description='Tracking Histogram Plotter')
parser.add_argument('filename', help='Name of SLCIO file')
parser.add_argument('-n', '--eventrange', nargs=2, type=int,
					help="Minimum and maximum of events to read (inclusive), "
							"default is all events")
parser.add_argument('-i', '--pdg', nargs='*', type=int,
					help="PDG of wanted particles")
parser.add_argument('-w', '--weight', type=float, default=1.0,
					help="Minimum weight of track wanted, currently only "
							"implemented for truth tracking")
momargs = parser.add_mutually_exclusive_group()
#momargs.add_argument('-p', '--momentum', type=float,
#					help="Momentum of particle")
momargs.add_argument('-pr', '--momentumrange', nargs=2, type=float, 
					help="Minimum and maximum of momentum")
phiargs = parser.add_mutually_exclusive_group()
#phiargs.add_argument('-f', '--phi', type=float,
#					help="Phi of particle")
phiargs.add_argument('-fr', '--phirange', nargs=2, type=float,
					help="Minimum and maximum of phi")
thetaargs = parser.add_mutually_exclusive_group()
#thetaargs.add_argument('-t', '--theta', type=float,
#						help="Theta of particle")
thetaargs.add_argument('-tr', '--thetarange', nargs=2, type=float,
						help="Minimum and maximum of theta")
args = parser.parse_args()

#Extracts data from file to dataframe
mcparticle_df, sitrack_df, catrack_df = (
		extracttrack.extract_mcparticle_and_track_to_dataframe(args.filename))

#Filter
#TODO: Add SD for momentum, phi, theta (no range)
#fdf for Filtered DataFrame
mcparticle_fdf = copy.copy(mcparticle_df)
sitrack_fdf = copy.copy(sitrack_df)
catrack_fdf = copy.copy(catrack_df)
if args.eventrange is not None:
	rangemin, rangemax = args.eventrange
	mcparticle_fdf = mcparticle_fdf.query("event >= %i"%rangemin).query("event < %i"%rangemax)
	sitrack_fdf = sitrack_fdf.query("event >= %i"%rangemin).query("event < %i"%rangemax)
	catrack_fdf = catrack_fdf.query("event >= %i"%rangemin).query("event < %i"%rangemax)
if args.pdg is not None:
	mcparticle_fdf = mcparticle_fdf.query("pdg in %s"%str(args.pdg))
if args.weight is not None:
	sitrack_fdf = sitrack_fdf.query("weight >= %f"%args.weight)
if args.momentumrange is not None:
	rangemin, rangemax = args.momentumrange
	mcparticle_fdf = mcparticle_fdf.query("momentum >= %f"%rangemin).query("momentum <= %f"%rangemax)
	sitrack_fdf = sitrack_fdf.query("momentum >= %f"%rangemin).query("momentum <= %f"%rangemax)
	catrack_fdf = catrack_fdf.query("momentum >= %f"%rangemin).query("momentum <= %f"%rangemax)
if args.phirange is not None:
	rangemin, rangemax = args.phirange
	mcparticle_fdf = mcparticle_fdf.query("phi >= %f"%rangemin).query("phi <= %f"%rangemax)
	sitrack_fdf = sitrack_fdf.query("phi >= %f"%rangemin).query("phi <= %f"%rangemax)
	catrack_fdf = catrack_fdf.query("phi >= %f"%rangemin).query("phi <= %f"%rangemax)
if args.thetarange is not None:
	rangemin, rangemax = args.thetarange
	mcparticle_fdf = mcparticle_fdf.query("theta >= %f"%rangemin).query("theta <= %f"%rangemax)
	sitrack_fdf = sitrack_fdf.query("theta >= %f"%rangemin).query("theta <= %f"%rangemax)
	catrack_fdf = catrack_fdf.query("theta >= %f"%rangemin).query("theta <= %f"%rangemax)

#TODO: temp only, move to a better place
if args.eventrange is not None:
	nevent = args.eventrange[1]-args.eventrange[0]
else:
	reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
	reader.open(args.filename)
	nevent = reader.getNumberOfEvents()
	reader.close()

"""
histwrap.plot_1d_double_histogram(
						mcparticle_fdf['momentum'], sitrack_fdf['momentum'],
						label1='MCParticle', label2='SiTracks',
						title='Tracking Momentum',
						nbins=int(nevent**0.5),)
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['momentum'], sitrack_fdf['momentum'],      
						labelref='MCParticle', labeltrk='SiTracks',
						title='SiTrack Momentum Efficiency',			           
						nbins=int(nevent**0.5))
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['momentum'], catrack_fdf['momentum'],      
						labelref='MCParticle', labeltrk='CATracks',
						title='CATrack Momentum Efficiency',			           
						nbins=int(nevent**0.5))
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['phi'], sitrack_fdf['phi'],
						labelref='MCParticle', labeltrk='SiTracks',
						title='SiTrack Phi Efficiency',     
						nbins=int(nevent**0.5), rangemin=0, rangemax=np.pi)
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['phi'], catrack_fdf['phi'],   
						labelref='MCParticle Efficiency', labeltrk='CATracks',
						title='CATrack Phi Efficiency', 
						nbins=int(nevent**0.5), rangemin=0, rangemax=np.pi)
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['theta'], sitrack_fdf['theta'],
						labelref='MCParticle', labeltrk='SiTracks',                   
						title='SiTrack Theta Efficiency',			    
						nbins=int(nevent**0.5), rangemin=-np.pi, rangemax=np.pi)
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['theta'], catrack_fdf['theta'],      
						labelref='MCParticle', labeltrk='CATracks',                   
						title='CATrack Theta Efficiency',			    
						nbins=int(nevent**0.5), rangemin=-np.pi, rangemax=np.pi)
"""

histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['momentum'], mcparticle_fdf['phi'], 'MCParticle'),
			(sitrack_fdf['momentum'], sitrack_fdf['phi'], 'SiTrack'),
			'Phi against Momentum', int(nevent**0.5), int(nevent**0.5))
histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['momentum'], mcparticle_fdf['theta'], 'MCParticle'),
			(sitrack_fdf['momentum'], sitrack_fdf['theta'], 'SiTrack'),
			'Theta against Momentum', int(nevent**0.5), int(nevent**0.5))
histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['phi'], mcparticle_fdf['theta'], 'MCParticle'),
			(sitrack_fdf['phi'], sitrack_fdf['theta'], 'SiTrack'),
			'Theta against Phi', int(nevent**0.5), int(nevent**0.5))
histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['momentum'], mcparticle_fdf['phi'], 'MCParticle'),
			(catrack_fdf['momentum'], catrack_fdf['phi'], 'CaTrack'),
			'Phi against Momentum', int(nevent**0.5), int(nevent**0.5))
histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['momentum'], mcparticle_fdf['theta'], 'MCParticle'),
			(catrack_fdf['momentum'], catrack_fdf['theta'], 'CaTrack'),
			'Theta against Momentum', int(nevent**0.5), int(nevent**0.5))
histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['phi'], mcparticle_fdf['theta'], 'MCParticle'),
			(catrack_fdf['phi'], catrack_fdf['theta'], 'CaTrack'),
			'Theta against Phi', int(nevent**0.5), int(nevent**0.5))
exit()

histwrap.plot_2d_single_histogram(mcparticle_fdf['momentum'], mcparticle_fdf['phi'], label='label', title='MC Phi v Mom', nbinsx=int(nevent**0.5), nbinsy=int(nevent**0.5))
histwrap.plot_2d_single_histogram(mcparticle_fdf['momentum'], mcparticle_fdf['theta'], label='label', title='MC Theta v Mom', nbinsx=int(nevent**0.5), nbinsy=int(nevent**0.5))
histwrap.plot_2d_single_histogram(mcparticle_fdf['phi'], mcparticle_fdf['theta'], label='label', title='MC Theta v Phi', nbinsx=int(nevent**0.5), nbinsy=int(nevent**0.5))
histwrap.plot_2d_single_histogram(sitrack_fdf['momentum'], sitrack_fdf['phi'], label='label', title='Si Phi v Mom', nbinsx=int(nevent**0.5), nbinsy=int(nevent**0.5))
histwrap.plot_2d_single_histogram(sitrack_fdf['momentum'], sitrack_fdf['theta'], label='label', title='Si Theta v Mom', nbinsx=int(nevent**0.5), nbinsy=int(nevent**0.5))
histwrap.plot_2d_single_histogram(sitrack_fdf['phi'], sitrack_fdf['theta'], label='label', title='Si Theta v Phi', nbinsx=int(nevent**0.5), nbinsy=int(nevent**0.5))
histwrap.plot_2d_single_histogram(catrack_fdf['momentum'], catrack_fdf['phi'], label='label', title='CA Phi v Mom', nbinsx=int(nevent**0.5), nbinsy=int(nevent**0.5))
histwrap.plot_2d_single_histogram(catrack_fdf['momentum'], catrack_fdf['theta'], label='label', title='CA Theta v Mom', nbinsx=int(nevent**0.5), nbinsy=int(nevent**0.5))
histwrap.plot_2d_single_histogram(catrack_fdf['phi'], catrack_fdf['theta'], label='label', title='CA Theta v Phi', nbinsx=int(nevent**0.5), nbinsy=int(nevent**0.5))

histwrap.plot_1d_double_histogram(mcparticle_fdf['momentum'], sitrack_fdf['momentum'],
						label1='MCParticle', label2='SiTracks',
						title='Tracking Momentum',
						nbins=int(nevent**0.5),)# rangemin=None, rangemax=110)
histwrap.plot_1d_double_histogram(mcparticle_fdf['momentum'], catrack_fdf['momentum'],      
						label1='MCParticle', label2='CATracks',
						title='Tracking Momentum',			           
						nbins=int(nevent**0.5),)# rangemin=None, rangemax=110)

histwrap.plot_1d_double_histogram(mcparticle_fdf['theta'], sitrack_fdf['theta'],
						label1='MCParticle', label2='SiTracks',
						title='Tracking Theta',     
						nbins=int(nevent**0.5),)# rangemin=1.4825, rangemax=1.4845)
histwrap.plot_1d_double_histogram(mcparticle_fdf['theta'], catrack_fdf['theta'],   
						label1='MCParticle', label2='CATracks',
						title='Tracking Theta', 
						nbins=int(nevent**0.5),)# rangemin=1.4825, rangemax=1.4845)

histwrap.plot_1d_double_histogram(mcparticle_fdf['phi'], sitrack_fdf['phi'],      
						label1='MCParticle', label2='SiTracks',                   
						title='Tracking Phi',			    
						nbins=int(nevent**0.5), rangemin=-np.pi, rangemax=np.pi)
histwrap.plot_1d_double_histogram(mcparticle_fdf['phi'], catrack_fdf['phi'],      
						label1='MCParticle', label2='CATracks',                   
						title='Tracking Phi',			    
						nbins=int(nevent**0.5), rangemin=-np.pi, rangemax=np.pi)

"""
qgraphmom = ROOT.TGraphQQ(nevent, sitrack_df['momentum'].values,
							nevent, catrack_df['momentum'].values,)
qgraphmom.Draw()
raw_input()
qgraphmomerr = ROOT.TGraphQQ(nevent, sitrack_df['momentumerr'].values,                
							nevent, catrack_df['momentumerr'].values,)                 
qgraphmomerr.Draw()                                                                
raw_input()                                                                     
qgraphtheta = ROOT.TGraphQQ(nevent, sitrack_df['theta'].values,             
	                        nevent, catrack_df['theta'].values,)          
qgraphtheta.Draw()                                                                
raw_input()                                                                     
qgraphphi = ROOT.TGraphQQ(nevent, sitrack_df['phi'].values,             
	                        nevent, catrack_df['phi'].values,)          
qgraphphi.Draw()                                                               
raw_input()                                                                     
"""        

