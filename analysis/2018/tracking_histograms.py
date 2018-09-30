"""Program for extracting properties of MC particles, truth tracks, and
conformal tracks from slcio and plotting histograms with extracted data.
Usage is: python tracking_histograms.py $slciofilename. 

Possible arguments are:
-n/--eventrange     : Minimum and maximum event number to plot
-i/--pdg            : PDG(s) of MC Particles to plot
-w/--weight         : Minimum weight of track to plot
-pr/--momentumrange : Minimum and maximum of momentum to plot
-fr/--phirange      : Minimum and maximum of phi to plot
-tr/--thetarange    : Minimum and maximum of theta to plot

"""
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
#TODO: Add way to plot only MCParticle/SiTrack/CATrack
#TODO: Add choice for histogram type
parser = argparse.ArgumentParser(description='Tracking Histogram Plotter')
parser.add_argument('filename', help='Name of SLCIO file')
parser.add_argument('-n', '--eventrange', nargs=2, type=int,
					help="Range of event number to read, min and max (inclusive);"
							" default is all events")
parser.add_argument('-i', '--pdg', nargs='*', type=int,
					help="PDG(s) of wanted particles")
parser.add_argument('-w', '--weight', type=float, default=1.0,
					help="Minimum weight of track wanted, currently only "
							"implemented for truth tracking")
#TODO: Change momentum, phi, theta to respective bin number
#Filters for graphs
momargs = parser.add_mutually_exclusive_group()
#momargs.add_argument('-p', '--momentum', type=float,
#					help="Momentum of particle")
momargs.add_argument('-pr', '--momentumrange', nargs=2, type=float,
					default=[None, None],
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
#fdf stands for Filtered DataFrame
mcparticle_fdf = copy.copy(mcparticle_df)
sitrack_fdf = copy.copy(sitrack_df)
catrack_fdf = copy.copy(catrack_df)
if args.eventrange is not None:
	rangemin, rangemax = args.eventrange
	mcparticle_fdf = mcparticle_fdf.query("event >= %i"%rangemin).query(
														"event < %i"%rangemax)
	sitrack_fdf = sitrack_fdf.query("event >= %i"%rangemin).query(
														"event < %i"%rangemax)
	catrack_fdf = catrack_fdf.query("event >= %i"%rangemin).query(
														"event < %i"%rangemax)
if args.pdg is not None:
	mcparticle_fdf = mcparticle_fdf.query("pdg in %s"%str(args.pdg))
if args.weight is not None:
	sitrack_fdf = sitrack_fdf.query("weight >= %f"%args.weight)
#Momentum, phi, theta filtering is now done by ROOT graph
"""#if first value is None, then argument has not been specified
if args.momentumrange[0] is not None:
	rangemin, rangemax = args.momentumrange
	mcparticle_fdf = mcparticle_fdf.query("momentum >= %f"%rangemin).query(
													"momentum <= %f"%rangemax)
	sitrack_fdf = sitrack_fdf.query("momentum >= %f"%rangemin).query(
													"momentum <= %f"%rangemax)
	catrack_fdf = catrack_fdf.query("momentum >= %f"%rangemin).query(
													"momentum <= %f"%rangemax)
if args.phirange is not None:
	rangemin, rangemax = args.phirange
	mcparticle_fdf = mcparticle_fdf.query("phi >= %f"%rangemin).query(
													"phi <= %f"%rangemax)
	sitrack_fdf = sitrack_fdf.query("phi >= %f"%rangemin).query(
													"phi <= %f"%rangemax)
	catrack_fdf = catrack_fdf.query("phi >= %f"%rangemin).query(
													"phi <= %f"%rangemax)
if args.thetarange is not None:
	rangemin, rangemax = args.thetarange
	mcparticle_fdf = mcparticle_fdf.query("theta >= %f"%rangemin).query(
													"theta <= %f"%rangemax)
	sitrack_fdf = sitrack_fdf.query("theta >= %f"%rangemin).query(
													"theta <= %f"%rangemax)
	catrack_fdf = catrack_fdf.query("theta >= %f"%rangemin).query(
													"theta <= %f"%rangemax)
"""
mommin, mommax = args.momentumrange
if args.phirange is not None:
	phimin, phimax = args.phirange
else:
	phimin, phimax = -np.pi, np.pi
if args.thetarange is not None:
	thetamin, thetamax = args.thetarange
else:
	thetamin, thetamax = 0, np.pi

#TODO: move reading of event no, add bin number for args
if args.eventrange is not None:
	nevent = args.eventrange[1]-args.eventrange[0]
else:
	reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
	reader.open(args.filename)
	nevent = reader.getNumberOfEvents()
	reader.close()
nbins = int(nevent**0.5)

#Plot histograms

histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['momentum'], sitrack_fdf['momentum'],      
						labelref='MCParticle', labeltrk='SiTracks',
						title='Momentum',			           
						nbins=nbins,
						rangemin=mommin, rangemax=mommax)
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['momentum'], catrack_fdf['momentum'],      
						labelref='MCParticle', labeltrk='CATracks',
						title='Momentum',			           
						nbins=nbins,
						rangemin=mommin, rangemax=mommax)
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['phi'], sitrack_fdf['phi'],
						labelref='MCParticle', labeltrk='SiTracks',
						title='Phi',     
						nbins=nbins, 
						rangemin=phimin, rangemax=phimax)
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['phi'], catrack_fdf['phi'],   
						labelref='MCParticle Efficiency', labeltrk='CATracks',
						title='Phi', 
						nbins=nbins,
						rangemin=phimin, rangemax=phimax)
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['theta'], sitrack_fdf['theta'],
						labelref='MCParticle', labeltrk='SiTracks',                   
						title='Theta',			    
						nbins=nbins,
						rangemin=thetamin, rangemax=thetamax)
histwrap.plot_1d_double_histogram_efficiency(
						mcparticle_fdf['theta'], catrack_fdf['theta'],      
						labelref='MCParticle', labeltrk='CATracks',                   
						title='Theta',			    
						nbins=nbins,
						rangemin=thetamin, rangemax=thetamax)

histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['momentum'], mcparticle_fdf['phi'], 'MCParticle'),
			(sitrack_fdf['momentum'], sitrack_fdf['phi'], 'SiTrack'),
			'Phi against Momentum', nbins, int(nevent**0.5),
			mommin, mommax, phimin, phimax)
histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['momentum'], mcparticle_fdf['theta'], 'MCParticle'),
			(sitrack_fdf['momentum'], sitrack_fdf['theta'], 'SiTrack'),
			'Theta against Momentum', nbins, int(nevent**0.5),
			mommin, mommax, thetamin, thetamax)
histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['phi'], mcparticle_fdf['theta'], 'MCParticle'),
			(sitrack_fdf['phi'], sitrack_fdf['theta'], 'SiTrack'),
			'Theta against Phi', nbins, int(nevent**0.5),
			phimin, phimax, thetamin, thetamax)
histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['momentum'], mcparticle_fdf['phi'], 'MCParticle'),
			(catrack_fdf['momentum'], catrack_fdf['phi'], 'CATrack'),
			'Phi against Momentum', nbins, int(nevent**0.5),
			mommin, mommax, phimin, phimax)
histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['momentum'], mcparticle_fdf['theta'], 'MCParticle'),
			(catrack_fdf['momentum'], catrack_fdf['theta'], 'CATrack'),
			'Theta against Momentum', nbins, int(nevent**0.5),
			mommin, mommax, thetamin, thetamax)
histwrap.plot_2d_single_histogram_efficiency(
			(mcparticle_fdf['phi'], mcparticle_fdf['theta'], 'MCParticle'),
			(catrack_fdf['phi'], catrack_fdf['theta'], 'CATrack'),
			'Theta against Phi', nbins, int(nevent**0.5),
			phimin, phimax, thetamin, thetamax)

histwrap.plot_2d_single_histogram(
		mcparticle_fdf['momentum'], mcparticle_fdf['phi'], label='label',
		title='MC Phi v Mom', nbinsx=nbins, nbinsy=int(nevent**0.5),
		rangexmin=mommin, rangexmax=mommax, rangeymin=phimin, rangeymax=phimax)
histwrap.plot_2d_single_histogram(
		mcparticle_fdf['momentum'], mcparticle_fdf['theta'], label='label', 
		title='MC Theta v Mom', nbinsx=nbins,
		nbinsy=nbins, rangexmin=mommin, rangexmax=mommax, 
		rangeymin=thetamin, rangeymax=thetamax)
histwrap.plot_2d_single_histogram(
		mcparticle_fdf['phi'], mcparticle_fdf['theta'], label='label',
		title='MC Theta v Phi', nbinsx=nbins,
		nbinsy=nbins, rangexmin=phimin, rangexmax=phimax,
		rangeymin=thetamin, rangeymax=thetamax)
histwrap.plot_2d_single_histogram(
		sitrack_fdf['momentum'], sitrack_fdf['phi'], label='label',
		title='Si Phi v Mom', nbinsx=nbins, nbinsy=int(nevent**0.5),
		rangexmin=mommin, rangexmax=mommax, rangeymin=phimin, rangeymax=phimax)
histwrap.plot_2d_single_histogram(
		sitrack_fdf['momentum'], sitrack_fdf['theta'], label='label',
		title='Si Theta v Mom', nbinsx=nbins,
		nbinsy=nbins, rangexmin=mommin, rangexmax=mommax,
		rangeymin=thetamin, rangeymax=thetamax)
histwrap.plot_2d_single_histogram(
		sitrack_fdf['phi'], sitrack_fdf['theta'], label='label',
		title='Si Theta v Phi', nbinsx=nbins,
		nbinsy=nbins, rangexmin=phimin, rangexmax=phimax,
		rangeymin=thetamin, rangeymax=thetamax)
histwrap.plot_2d_single_histogram(
		catrack_fdf['momentum'], catrack_fdf['phi'], label='label',
		title='CA Phi v Mom', nbinsx=nbins, nbinsy=int(nevent**0.5),
		rangexmin=mommin, rangexmax=mommax, rangeymin=phimin, rangeymax=phimax)
histwrap.plot_2d_single_histogram(
		catrack_fdf['momentum'], catrack_fdf['theta'], label='label',
		title='CA Theta v Mom', nbinsx=nbins,
		nbinsy=nbins, rangexmin=mommin, rangexmax=mommax, 
		rangeymin=thetamin, rangeymax=thetamax)
histwrap.plot_2d_single_histogram(
		catrack_fdf['phi'], catrack_fdf['theta'], label='label',
		title='CA Theta v Phi', nbinsx=nbins,
		nbinsy=nbins, rangexmin=phimin, rangexmax=phimax,
		rangeymin=thetamin, rangeymax=thetamax)

histwrap.plot_1d_double_histogram(mcparticle_fdf['momentum'], 
								sitrack_fdf['momentum'],
								label1='MCParticle', label2='SiTracks',
								title='Tracking Momentum',
								nbins=nbins, 
								rangemin=mommin, rangemax=mommax)
histwrap.plot_1d_double_histogram(mcparticle_fdf['momentum'], 
								catrack_fdf['momentum'],      
								label1='MCParticle', label2='CATracks',
								title='Tracking Momentum',			           
								nbins=nbins,
								rangemin=mommin, rangemax=mommax)
histwrap.plot_1d_double_histogram(mcparticle_fdf['phi'], sitrack_fdf['phi'],      
								label1='MCParticle', label2='SiTracks',                   
								title='Tracking Phi',			    
								nbins=nbins,
								rangemin=phimin, rangemax=phimax)
histwrap.plot_1d_double_histogram(mcparticle_fdf['phi'], catrack_fdf['phi'],      
								label1='MCParticle', label2='CATracks',                   
								title='Tracking Phi',			    
								nbins=nbins,
								rangemin=phimin, rangemax=phimax)
histwrap.plot_1d_double_histogram(mcparticle_fdf['theta'], sitrack_fdf['theta'],
								label1='MCParticle', label2='SiTracks',
								title='Tracking Theta',     
								nbins=nbins,
								rangemin=thetamin, rangemax=thetamax)
histwrap.plot_1d_double_histogram(mcparticle_fdf['theta'], catrack_fdf['theta'],   
								label1='MCParticle', label2='CATracks',
								title='Tracking Theta', 
								nbins=nbins,
								rangemin=thetamin, rangemax=thetamax)

