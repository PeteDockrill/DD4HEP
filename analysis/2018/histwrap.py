"""Module containing wrapper functions for plotting ROOT histograms.

Functions
--------
plot_1d_single_histograms
plot_1d_doublehistograms
plot_2d_single_histogram
"""


import ROOT


def _create_1d_histogram(array, label, title, nbins, rangemin, rangemax):
	"""Returns 1D ROOT histogram object (TH1F; one float per channel).
		
	Arguments
	---------
	array : np.ndarray
		Array containing data
	label : str
		Label for data in array
	title : str
		Title of histogram
	nbins : int
		Number of bins
	rangemin : float
		Minimum value on x-axis (minimum value in array if None)
	rangemax : float
		Maximum value on x-axis (maximum value in array if None)
	
	Returns
	-------
	histogram : ROOT.TH1F
		1D ROOT histogram object (one float per channel)
	"""
	#Label, Title, Number of Bins, Range Min, Range Max
	histogram = ROOT.TH1F(label, title, nbins,
							array.min() if rangemin is None else rangemin,
							array.max() if rangemax is None else rangemax)
	#Adds values to histogram
	for value in array:
		histogram.Fill(value)
	
	return histogram


def plot_1d_single_histogram(array, label='', title='', nbins=10,
						rangemin=None, rangemax=None):
	"""Wrapper for plotting 1D ROOT Histogram (TH1F; one float per channel).
	
	Arguments
	---------
	array : np.ndarray
		Array containing data
	
	Keyword Arguments
	----------------
	label : str
		Label for data in array
	title : str
		Title of histogram
	nbins : int
		Number of bins
	rangemin : float
		Minimum value on x-axis (minimum value in array if None)
	rangemax : float
		Maximum value on x-axis (maximum value in array if None)
	
	Methods Used
	------------
	_create_1d_histogram
	"""
	histogram = _create_1d_histogram(array, label, title, nbins, rangemin,
									rangemax)
	#histogram name, no of entries, mean, rms, no of underflow, no of upperflow,    
	#skewness
	ROOT.gStyle.SetOptStat('nemruos')
	histogram.Draw()
	#raw_input line needed or else ROOT will automatically close graph)
	raw_input()


def plot_1d_double_histogram(array1, array2, label1='', label2='', title='',
							nbins=10, rangemin=None, rangemax=None):
	"""Wrapper for double 1D ROOT Histograms (TH1F; one float per channel).
	
	Arguments
	---------
	array1 : np.ndarray
		Array containing first set of data (plotted in red)
	array2 : np.ndarray
		Array containing second set of data (plotted in blue)
	
	Keyword Arguments
	----------------
	label1 : str
		Label for data in array1
	label2 : str
		Label for data in array2 
	title : str
		Title of histogram
	nbins : int
		Number of bins
	rangemin : float
		Minimum value on x-axis (minimum value in array1 and array2 if None)
	rangemax : float
		Maximum value on x-axis (maximum value in array1 and array2 if None)
	
	Methods Used
	------------
	_create_1d_histogram
	"""
	#TODO: Add separation of statistics box
	if rangemin is None:
		rangemin1 = array1.min()
		rangemin2 = array2.min()
		rangemin = min(rangemin1, rangemin2)
	else:
		rangemin = rangemin
	if rangemax is None:
		rangemax1 = max(array1)    
		rangemax2 = max(array2)
		rangemax = max(rangemax1, rangemax2)
	else:
		rangemax = rangemax
	
	histogram1 = _create_1d_histogram(array1, label1, title, nbins, rangemin,
										rangemax)
	histogram1.SetLineColor(ROOT.kRed)
	histogram1.SetLineWidth(3)
	
	histogram2 = _create_1d_histogram(array2, label2, title, nbins, rangemin,
										rangemax)
	histogram2.SetLineColor(ROOT.kBlue)
	histogram2.SetLineWidth(3)
	
	#histogram name, no of entries, mean, rms, no of underflow, no of upperflow,    
	#skewness
	ROOT.gStyle.SetOptStat('nemruos')
 
	histogram1.Draw()                                              
	histogram2.Draw("sames")
	#raw_input line needed or else ROOT will automatically close graph
	raw_input()


def plot_1d_double_histogram_efficiency(arrayref, arraytrk, labelref='',
										labeltrk='', title='', nbins=10,
										rangemin=None, rangemax=None):
	"""Plots effiency using 1D ROOT histogram object (TH1F; one float per 
	channel). Same input as plot_1d_double_histogram.
	
	Arguments
	---------
	arrayref: np.ndarray
		Array containing particle data (plotted in red)
	arraytrk : np.ndarray
		Array containing track/reconstructed data (plotted in blue)
	
	Keyword Arguments
	----------------
	labelref : str
		Label for data in arrayref
	labeltrk : str
		Label for data in arraytrk
	title : str
		Title of histogram
	nbins : int
		Number of bins
	rangemin : float
		Minimum value on x-axis (minimum value in arrayref and arraytrk if None)
	rangemax : float
		Maximum value on x-axis (maximum value in arrayref and arraytrk if None)
	
	Methods Used
	------------
	_create_1d_histogram
	"""
	rangeminref = arrayref.min() if rangemin is None else rangemin
	rangemintrk = arraytrk.min() if rangemin is None else rangemin
	rangemin = min(rangeminref, rangemintrk) 
	rangemaxref = arrayref.max() if rangemax is None else rangemax    
	rangemaxtrk = arraytrk.max() if rangemax is None else rangemax
	rangemax = max(rangemaxref, rangemaxtrk)
	
	#Histograms have to have same range and no of bins
	#Plots have to drawn on separate canvases and drawn before another          
	#canvas is created
	c1 = ROOT.TCanvas('c1', 'MCParticleCanvas', 1)
	histogram_ref = _create_1d_histogram(arrayref, labelref, title, nbins,
											rangemin, rangemax) 
	#histogram name, no of entries, mean, rms, no of underflow, no of upperflow, 
	#skewness                                                                   
	ROOT.gStyle.SetOptStat('nemruos')
	histogram_ref.Draw()
	
	c2 = ROOT.TCanvas('c2', 'TrackCanvas', 1)
	histogram_track = _create_1d_histogram(arraytrk, labeltrk, title, nbins,
											rangemin, rangemax)
	ROOT.gStyle.SetOptStat('nemruos')
	histogram_track.Draw()
	
	c3 = ROOT.TCanvas('c3', 'EfficiencyCanvas', 1)
	histogram_efficiency = _create_1d_histogram(arraytrk, 'Efficiency', title+' Efficiency', nbins,    
											rangemin, rangemax)
	#Gives efficiency
	histogram_efficiency.Divide(histogram_ref)
	ROOT.gStyle.SetOptStat('nemruos')
	histogram_efficiency.Draw()
	
	#raw_input line needed or else ROOT will automatically close graph)
	raw_input()


def _create_2d_histogram(arrayx, arrayy, label, title, nbinsx, nbinsy,
						rangexmin, rangexmax, rangeymin, rangeymax):
	"""Returns 2D ROOT histogram object (TH2F; one float per channel).
	
	Arguments
	---------
	arrayx : np.ndarray
		Array containing data for x-axis
	arrayy : np.ndarray
		Array containing data for y-axis
	label : str
		Label for data in arrays
	title : str
		Title of histogram
	nbinsx : int
		Number of bins on x-axis
	nbinsy : int
		Number of bins on y-axis
	rangexmin : float
		Minimum value on x-axis (minimum value in arrayx if None)
	rangexmax : float
		Maximum value on x-axis (maximum value in arrayx if None)
	rangeymin : float
		Minimum value on y-axis (minimum value in arrayy if None)
	rangeymax : float
		Maximum value on y-axis (maximum value in arrayy if None)

	Returns
	-------
	histogram : ROOT.TH2F
		2D ROOT histogram object (one float per channel)
	"""
	assert len(arrayx) == len(arrayy)
	
	#min/max of axis
	rangexmin = arrayx.min() if rangexmin is None else rangexmin    
	rangexmax = arrayx.max() if rangexmax is None else rangexmax
	rangeymin = arrayy.min() if rangeymin is None else rangeymin                   
	rangeymax = arrayy.min() if rangeymax is None else rangeymax
	
	#label, title, no of bins on x-axis, min x, max x, 
	#no of bins on y-axis, min y, max y
	histogram = ROOT.TH2F(label, title, nbinsx, rangexmin, rangexmax,
							nbinsy, rangeymin, rangeymax)
	#Add values to histogram
	for valuex, valuey in zip(arrayx, arrayy):
		histogram.Fill(valuex, valuey)
	
	return histogram


def plot_2d_single_histogram(arrayx, arrayy, label='', title='',     
							nbinsx=10, nbinsy=10, rangexmin=None, rangexmax=None,
							rangeymin=None, rangeymax=None):
	"""Wrapper for plotting 2D ROOT histograms (TH2F; one float per channel).
	
	Arguments
	---------
	arrayx : np.ndarray
		Array containing data for x-axis
	arrayy : np.ndarray
		Array containing data for y-axis
	
	Keyword Arguments
	-----------------
	label : str
		Label for data in arrays
	title : str
		Title of histogram
	nbinsx : int
		Number of bins on x-axis
	nbinsy : int
		Number of bins on y-axis
	rangexmin : float
		Minimum value on x-axis (minimum value in arrayx if None)
	rangexmax : float
		Maximum value on x-axis (maximum value in arrayx if None)
	rangeymin : float
		Minimum value on y-axis (minimum value in arrayy if None)
	rangeymax : float
		Maximum value on y-axis (maximum value in arrayy if None)
	
	Methods Used
	------------
	_create_2d_histogram
	"""
	#TODO: Add separation of statistics box
	histogram = _create_2d_histogram(arrayx, arrayy, label, title, nbinsx,
									nbinsy, rangexmin, rangexmax,
									rangeymin, rangeymax)
	
	#histogram name, no of entries, mean, rms, no of underflow, no of upperflow,    
	#skewness
	ROOT.gStyle.SetOptStat('nemruos')

	#Shows legend for colour
	histogram.Draw('COLZ')
	#raw_input line needed or else ROOT will automatically close graph)
	raw_input()


def plot_2d_single_histogram_efficiency(tupleref, tupletrk, title='', nbinsx=10,
										nbinsy=10, rangexmin=None,
										rangexmax=None, rangeymin=None,
										rangeymax=None):
	"""Plots effiency using 2D ROOT histogram object (TH2F; one float per
	channel). Each tuple contains the input for a 2d_single_histogram apart
	from range (arrayx, arrayy, label, title, nbinx, nbinsy), but all
	arguments must be given unlike plot_2d_single_histogram.
	
	Arguments
	---------
	tupleref : tuple
		tuple containing arrayx, arrayy, and label for reference histogram
	tupletrk : tuple
		tuple containing arrayx, arrayy, and label for track histogram 
	
	Keyword Arguments
	-----------------
	title : str
		Title of histogram
	nbinsx : int
		Number of bins on x-axis
	nbinsy : int
		Number of bins on y-axis
	rangexmin : float
		Minimum value on x-axis (minimum value in arrayx if None)
	rangexmax : float
		Maximum value on x-axis (maximum value in arrayx if None)
	rangeymin : float
		Minimum value on y-axis (minimum value in arrayy if None)
	rangeymax : float
		Maximum value on y-axis (maximum value in arrayy if None)

	Methods Used
	------------
	_create_2d_histogram
	""" 
	#TODO: Currently plots very slow, find faster way
	(arrayxref, arrayyref, labelref) = tupleref
	(arrayxtrk, arrayytrk, labeltrk) = tupletrk

	rangexminref = arrayxref.min() if rangexmin is None else rangexmin 
	rangexmintrk = arrayxtrk.min() if rangexmin is None else rangexmin
	rangexmin = min(rangexminref, rangexmintrk)
	rangexmaxref = arrayxref.max() if rangexmax is None else rangexmax 
	rangexmaxtrk = arrayxtrk.max() if rangexmax is None else rangexmax
	rangexmax = max(rangexmaxref, rangexmaxtrk)
	rangeyminref = arrayyref.min() if rangeymin is None else rangeymin 
	rangeymintrk = arrayytrk.min() if rangeymin is None else rangeymin
	rangeymin = min(rangeyminref, rangeymintrk)
	rangeymaxref = arrayyref.max() if rangeymax is None else rangeymax 
	rangeymaxtrk = arrayytrk.max() if rangeymax is None else rangeymax
	rangeymax = max(rangeymaxref, rangeymaxtrk)
	
	#Plots have to drawn on separate canvases and drawn before another
	#canvas is created
	c1 = ROOT.TCanvas('c1', 'MCParticleCanvas', 1)
	histogram_ref = _create_2d_histogram(*tupleref, title=title, nbinsx=nbinsx,
										nbinsy=nbinsy,
										rangexmin=rangexmin, rangexmax=rangexmax,
										rangeymin=rangeymin, rangeymax=rangeymax) 
	
	#histogram name, no of entries, mean, rms, no of underflow, no of upperflow,    
	#skewness
	ROOT.gStyle.SetOptStat('nemruos')
	histogram_ref.Draw('COLZ')
		
	c2 = ROOT.TCanvas('c2', 'TrackCanvas', 1)
	histogram_track = _create_2d_histogram(*tupletrk, title=title,
											nbinsx=nbinsx, nbinsy=nbinsy,
											rangexmin=rangexmin,
											rangexmax=rangexmax,
											rangeymin=rangeymin,
											rangeymax=rangeymax)
	ROOT.gStyle.SetOptStat('nemruos')
	histogram_track.Draw('COLZ')
	
	c3 = ROOT.TCanvas('c3', 'EfficiencyCanvas', 1)
	histogram_efficiency = _create_2d_histogram(arrayxtrk, arrayytrk, 'Efficiency',
											title=title+' Efficiency',
											nbinsx=nbinsx, nbinsy=nbinsy,
											rangexmin=rangexmin,
											rangexmax=rangexmax,
											rangeymin=rangeymin,
											rangeymax=rangeymax)
	#Gives efficiency
	histogram_efficiency.Divide(histogram_ref)
	ROOT.gStyle.SetOptStat('nemruos')
	histogram_efficiency.Draw('COLZ')
	
	#raw_input line needed or else ROOT will automatically close graph)
	raw_input()	
