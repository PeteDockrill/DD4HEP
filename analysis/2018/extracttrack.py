"""Module for extracting track properties from MCParticles and tracks.
Main function for external use is extract_mcparticle_and_track_to_dataframe.
"""

import math
import numpy as np
import pandas as pd	
import pyLCIO


def extract_track_properties(track):                                            
	"""Extract properties (momentum, phi and theta) from track.          
	
	Arguments
	---------
	track : ROOT.IOIMPL.TrackIOImpl
		Track to extract properties from
	
	Returns
	------
	trackmom : float
		Momentum of track
	trackphi : float
		phi of track
	tracktheta : float
		theta of track
	"""
	c = 2.99792*10**11                                                          
                                                                                
	#Transverse momentum related to omega, momentum related to tan(lambda)
	tracktransmom = math.fabs(c*10**(-15)*5/track.getOmega())                  
	trackmom = tracktransmom*(1+track.getTanLambda()**2)**0.5
	trackphi = track.getPhi()
	#theta also related to tan(lambda)
	tracktheta = math.pi/2.-math.atan(track.getTanLambda())                     
	
	return (trackmom, trackphi, tracktheta)


def extract_mcparticle_properties(mcparticle):
	"""Extracts properties (momentum, phi and theta)  from mcparticle.
	
	Arguments
	--------
	mcparticle : ROOT.IOIMPL.MCParticleIOImpl
		MCParticle to extract properties from

	Returns
	-------
	mcparticlemom : float
		Momentum of mcparticle
	mcparticlephi : float
		phi of mcparticle
	mcparticletheta : float
		theta of mcparticle
	"""
	#Only first 3 elements of mcparticle.getMomentum() contain information;
	#can't get more than one element at once
	mcparticlemomx, mcparticlemomy, mcparticlemomz = (
			mcparticle.getMomentum()[0], mcparticle.getMomentum()[1],
			mcparticle.getMomentum()[2])
	mcparticlemom = (mcparticlemomx**2+mcparticlemomy**2+mcparticlemomz**2)**0.5                                              
	mcparticletransmom = (mcparticlemomx**2+mcparticlemomy**2)**0.5     
	mcparticlephi = math.atan2(mcparticlemomy, mcparticlemomx)
	mcparticletheta = math.atan2(mcparticletransmom,mcparticlemomz)     
	
	return (mcparticlemom, mcparticlephi, mcparticletheta)


def extract_mcparticle_and_track_to_dataframe(filename, flat=True):	
	"""Extracts MCParticle, SiTrack, and CATrack, and outputs properties as
	pandas DataFrames. flat==True returns a flat DataFrame, False returns
	a DataFrame containing lists for each event (very slow).
	
	Arguements
	---------
	filename : str
		Name of *.slcio file to extract data from
	
	Keyword Arguments
	----------------
	flat : bool
		True returns a flat pandas DataFrame, False returns a DataFrame
		containing Series with lists (much slower)
	
	Returns
	------
	mcparticle_df : pandas DataFrame
		DataFrame containing event no, PDG, momentum, phi, and theta of 
		MCParticles
	sitrack_df : pandas DataFrame
		DataFrame containing event no, weight, momentum, momentum error,
		phi, and theta of Truth Tracks
	catrack_df : pandas DataFrame
		DataFrame containing event no, momentum, momentum error, phi, and
		theta of Conformal Tracks (weight is currently not implemented in
		Marlin)		
	"""
	#Interface for reading *.slcio files
	reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
	reader.open(filename)
	
	if not flat:
		nevent = reader.getNumberOfEvents()
		mcparticle_df = pd.DataFrame({
								'event':[[]]*nevent, 'pdg':[[]]*nevent,
								'momentum':[[]]*nevent, 'phi':[[]]*nevent, 
								'theta':[[]]*nevent})
		sitrack_df = pd.DataFrame({
							'event':[[]]*nevent, 'weight':[[]]*nevent,
							'momentum':[[]]*nevent, 'momentumerr':[[]]*nevent,
							'phi':[[]]*nevent, 'theta':[[]]*nevent})
		catrack_df = pd.DataFrame({
							'event':[[]]*nevent, #'weight':[[]]*nevent,
							'momentum':[[]]*nevent,
							'momentumerr':[[]]*nevent,
							'phi':[[]]*nevent, 'theta':[[]]*nevent})
		#In each event, iterates over each mcparticle to find corresponding track
		for i, event in enumerate(reader):
			#Iterables
			mcparticle_iter = event.getCollection("MCParticle")
			#sitracks_iter = event.getCollection("SiTracks")
			sitrackrelations_iter = event.getCollection("SiTrackRelations")
			catracks_iter = event.getCollection("CATracks")
			#catrackrelations_iter = event.getCollection("CATrackRelation")

			#Lists containing properties particles/tracks of event i
			mcparticlepdg_list = []
			mcparticlemom_list = []
			mcparticlephi_list = []
			mcparticletheta_list = []

			sitrackweight_list = []
			sitrackmom_list = []
			sitrackmomerr_list = []
			sitrackphi_list = []
			sitracktheta_list = []

			#Iterates over each MCParticle to find corresponding track
			for mcparticle in mcparticle_iter:
				#Extract properties for mcparticle and add to list
				mcparticlemom, mcparticlephi, mcparticletheta = (
											extract_mcparticle_properties())
				mcparticlepdg_list.append(mcparticle.getPDG())
				mcparticlemom_list.append(mcparticlemom)
				mcparticlephi_list.append(mcparticlephi)
				mcparticletheta_list.append(mcparticletheta)
					
				#Find sitrack corresponding to mcparticle
				for relation in sitrackrelations_iter:
					weight = relation.getWeight()
					if (relation.getTo().id() == mcparticle.id()):
						sitrack = relation.getFrom()
						
						#Extract properties for sitrack and add to list
						sitrackmom, sitrackphi, sitracktheta = (
											extract_track_properties(sitrack))
					
						sitrackweight_list.append(weight)
						sitrackmom_list.append(sitrackmom)
						sitrackmomerr_list.append(sitrackmom-mcparticlemom)
						sitrackphi_list.append(sitrackphi)
						sitracktheta_list.append(sitracktheta)
			
			#Add list containing properties to dataframe
			sitrack_df['event'].loc[i] = [i]*len(sitrackweight_list)
			sitrack_df['weight'].loc[i] = sitrackweight_list
			sitrack_df['momentum'].loc[i] = sitrackmom_list
			sitrack_df['momentumerr'].loc[i] = sitrackmomerr_list
			sitrack_df['phi'].loc[i] = sitrackphi_list
			sitrack_df['theta'].loc[i] = sitracktheta_list 

			mcparticle_df['event'].loc[i] = np.array([i]*len(mcparticlepdg_list))
			mcparticle_df['pdg'].loc[i] = np.array(mcparticlepdg_list)
			mcparticle_df['momentum'].loc[i] = np.array(mcparticlemom_list)
			mcparticle_df['phi'].loc[i] = np.array(mcparticlephi_list)
			mcparticle_df['theta'].loc[i] = np.array(mcparticletheta_list)

			#catrackweight_list = []
			catrackmom_list = []
			catrackmomerr_list = []
			catrackphi_list = []
			catracktheta_list = []
			
			#Finds all catracks and corresponding properties
			#currently no relation present
			for catrack in catracks_iter:
				#TODO: Add weight calculation
				catrackmom, catrackphi, catracktheta = extract_track_properties(catrack)
				catrackmom_list.append(catrackmom)                                                        
				catrackmomerr_list.append(catrackmom-mcparticlemom)                                      
				catrackphi_list.append(catrackphi)
				catracktheta_list.append(catracktheta)
			catrack_df['event'].loc[i] = [i]*len(catrackmom_list)
			#catrack_df['weight'].loc[i] = catrackweight_list
			catrack_df['momentum'].loc[i] = catrackmom_list
			catrack_df['momentumerr'].loc[i] = catrackmomerr_list
			catrack_df['phi'].loc[i] = catrackphi_list
			catrack_df['theta'].loc[i] = catracktheta_list
			
	else:
		#Lists containing properties particles/tracks of all events
		mcparticleevent_alllist = []
		mcparticlepdg_alllist = []
		mcparticlemom_alllist = []
		mcparticlephi_alllist = []
		mcparticletheta_alllist = []
		
		sitrackevent_alllist = []
		sitrackweight_alllist = []
		sitrackmom_alllist = []
		sitrackmomerr_alllist = []
		sitrackphi_alllist = []
		sitracktheta_alllist = []
		
		catrackevent_alllist = []
		#catrackweight_alllist = []
		catrackmom_alllist = []
		catrackmomerr_alllist = []
		catrackphi_alllist = []
		catracktheta_alllist = []

		#In each event, iterates over each mcparticle to find corresponding track
		for i, event in enumerate(reader):
			#Iterables
			mcparticle_iter = event.getCollection("MCParticle")
			#sitracks_iter = event.getCollection("SiTracks")
			sitrackrelations_iter = event.getCollection("SiTrackRelations")
			catracks_iter = event.getCollection("CATracks")
			#catrackrelations_iter = event.getCollection("CATrackRelation")

			#Iterates over each MCParticle to find corresponding track
			for mcparticle in mcparticle_iter:
				#Extract properties for mcparticle and add to (all)list
				mcparticlemom, mcparticlephi, mcparticletheta = (
									extract_mcparticle_properties(mcparticle))
				
				mcparticleevent_alllist.append(i)
				mcparticlepdg_alllist.append(mcparticle.getPDG())
				mcparticlemom_alllist.append(mcparticlemom)
				mcparticlephi_alllist.append(mcparticlephi)
				mcparticletheta_alllist.append(mcparticletheta)
					
				#Find sitrack corresponding to mcparticle
				for relation in sitrackrelations_iter:
					weight = relation.getWeight()
					if (relation.getTo().id() == mcparticle.id()):
						sitrack = relation.getFrom()

						#Extract properties for sitrack and add to list
						sitrackmom, sitrackphi, sitracktheta = (
											extract_track_properties(sitrack))
					
						sitrackevent_alllist.append(i)
						sitrackweight_alllist.append(weight)
						sitrackmom_alllist.append(sitrackmom)
						sitrackmomerr_alllist.append(sitrackmom-mcparticlemom)
						sitrackphi_alllist.append(sitrackphi)
						sitracktheta_alllist.append(sitracktheta)
			
			#Finds all catracks, currently no relation present
			for catrack in catracks_iter:
				#TODO: Add weight calculation
				catrackmom, catrackphi, catracktheta = extract_track_properties(catrack)
				
				catrackevent_alllist.append(i)
				#catrackweight_alllist.append(1.0) #Dummy for now
				catrackmom_alllist.append(catrackmom)                                                        
				catrackmomerr_alllist.append(catrackmom-mcparticlemom)                                      
				catrackphi_alllist.append(catrackphi)
				catracktheta_alllist.append(catracktheta)
		
		#Convert lists for each mcparticle/track to dataframe
		mcparticle_df = pd.DataFrame({'event':mcparticleevent_alllist,
									'pdg':mcparticlepdg_alllist,
									'momentum':mcparticlemom_alllist,
									'phi':mcparticlephi_alllist,
									'theta':mcparticletheta_alllist})
		
		sitrack_df = pd.DataFrame({'event':sitrackevent_alllist,
									'weight':sitrackweight_alllist,
									'momentum':sitrackmom_alllist,
									'momentumerr':sitrackmom_alllist,
									'phi':sitrackphi_alllist,
									'theta':sitracktheta_alllist})
		
		catrack_df = pd.DataFrame({'event':catrackevent_alllist,
									#'weight':catrackweight_alllist,
									'momentum':catrackmom_alllist,
									'momentumerr':catrackmom_alllist,
									'phi':catrackphi_alllist,
									'theta':catracktheta_alllist})

	return mcparticle_df, sitrack_df, catrack_df
