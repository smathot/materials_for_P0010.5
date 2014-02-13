#-*- coding:utf-8 -*-

"""
This file is part of P0010.5.

P0010.5 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

P0010.5 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with P0010.5.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import warnings
import numpy as np
from exparser.CsvReader import CsvReader
from exparser.PivotMatrix import PivotMatrix
from exparser.TangoPalette import *
from matplotlib import pyplot as plt
from analysis import plot, stats
# Direct import so that we can invoke it from the command line
from analysis.stats import modelBuild

# The maximum saccade number to include in masterplot (production value=20)
maxSacc = 20

def _exp1(dm):
	
	"""Performs the full analysis for experiment 1."""
	
	# Generic
	masterPlot(dm)
	pupilSizePlot(dm)
	salFromPlot(dm)
	windowPlot(dm)

def _exp2(dm):
	
	"""Performs the full analysis for experiment 2."""
	
	# Generic
	masterPlot(dm)
	pupilSizePlot(dm)
	salFromPlot(dm)
	windowPlot(dm)
	# Experiment specific 
	instructionPlot(dm)
	instructionPlotPupilSize(dm)
	instructionPlotSalFrom(dm)

def _exp3(dm):
	
	"""Performs the full analysis for experiment 3."""
	
	# Generic
	masterPlot(dm)
	pupilSizePlot(dm)
	salFromPlot(dm)
	windowPlot(dm)
	# Experiment specific
	loadPlot(dm)
	loadPlotPupilSize(dm)
	loadPlotSalFrom(dm)	

def dvPlot(dm, dv, standalone=True, color=blue[1], label=None):
	
	"""
	Plots a dependent measure as a function of saccade number.
	
	Arguments:
	dm		--	A DataMatrix.
	dv		--	The dependent variable.
	
	Keyword arguments:
	standalone	--	Indicates whether this is a standalone plot, in which case
					it will create and save the plot, or not. (default=True)
	color		--	Plot color. (default=blue[1])
	label		--	Line label. (default=None)
	"""
	
	assert(dv in dm.columns())
	if standalone:
		plot.new()
	xData = []
	yData = []
	eData = []
	for saccNr in [None] + range(1, maxSacc+1):
		if saccNr == None:
			_dm = dm
		else:
			_dm = dm.select('saccNr == %d' % saccNr)
		y = _dm[dv].mean()
		e = _dm[dv].std() / np.sqrt(len(_dm))
		if saccNr == None:
			plt.errorbar(-2, y, yerr=[e], fmt='o-', color=color)
		else:
			xData.append(saccNr)
			yData.append(y)
			eData.append(e)
	xData = np.array(xData)
	yData = np.array(yData)
	eData = np.array(eData)
	plt.fill_between(xData, yData-eData, yData+eData, color=color, alpha=.25)
	plt.plot(xData, yData, 'o-', color=color, label=label)
	plt.axhline(0, linestyle='--', color='black')
	plt.xlabel('Saccade number')
	plt.ylabel(dv)
	plt.xlim(-2.5, maxSacc+.5)
	if standalone:
		plot.save('dvPlot.%s' % dv, show=True)

def filter(dm):
	
	"""
	Filters the DataMatrix.
	
	Returns:
	A DataMatrix.
	"""
	
	# Remove practice trials for exp 3
	if exp == 'exp3':
		dm = dm.select('trialId > 3')
	return dm

def getDataMatrix():
	
	"""
	Reads the data for the current experiment.
	
	Returns:
	A DataMatrix.
	"""
	
	print 'Reading ...'
	dm = CsvReader('data/%s.csv' % exp).dataMatrix()
	print 'Done'
	return dm

def instructionPlot(dm):
	
	"""
	Plots the effect of pupil size on saliency for different task instructions.
	Also builds optimal models for all instrunctions.
	
	Note: This is only applicable for experiment 2.
	
	Arguments:
	dm		--	A DataMatrix.
	"""
	
	assert(exp == 'exp2')
	modelBuild(dm.select('inst == "free"'), suffix='.free')
	modelBuild(dm.select('inst == "search"'), suffix='.search')
	modelBuild(dm.select('inst == "memory"'), suffix='.memory')
	plot.new()
	_dm = dm.select('inst == "free"')
	masterPlot(_dm, standalone=False, color=green[1], label='Free viewing')
	_dm = dm.select('inst == "search"')
	masterPlot(_dm, standalone=False, color=orange[1], label='Visual search')
	_dm = dm.select('inst == "memory"')
	masterPlot(_dm, standalone=False, color=blue[1], label='Memory')
	plt.legend()
	plot.save('instructionPlot', show=True)
	
def loadPlot(dm):
	
	"""
	Plots the effect of pupil size on saliency for different memory-load
	conditions, where lines correspond to load conditions. Also builds optimal
	models for the two conditions.
	
	Note: This is only applicable to experiment 3.
	
	Arguments:
	dm		--	A DataMatrix.
	"""
	
	assert(exp == 'exp3')
	modelBuild(dm.select('cond == "single"'), suffix='.single')
	modelBuild(dm.select('cond == "dual"'), suffix='.dual')
	plot.new()
	_dm = dm.select('cond == "single"')
	masterPlot(_dm, standalone=False, color=green[1], label='Single')
	_dm = dm.select('cond == "dual"')
	masterPlot(_dm, standalone=False, color=orange[1], label='Dual')
	plt.legend()
	plot.save('loadPlot', show=True)
	
def loadPlotPupilSize(dm):
	
	"""
	Creates pupil-size plots for the two load conditions, and performs an LME.
	
	Arguments:
	dm		--	A DataMatrix.
	"""
	
	assert(exp == 'exp3')
	# LME
	R.load(dm)
	_dm = R.lmer('pupilSize ~ cond + (1|file) + (1|scene)', nsim=nsim)
	_dm.save('output/exp3/pupilSize.cond.csv')
	print _dm
	# Plot
	plot.new()
	_dm = dm.select('cond == "single"')
	pupilSizePlot(_dm, standalone=False, color=green[1], label='Single')
	_dm = dm.select('cond == "dual"')
	pupilSizePlot(_dm, standalone=False, color=orange[1], label='Dual')
	plt.legend()
	plot.save('loadPlotPupilSize', show=True)
	
def loadPlotSalFrom(dm):
	
	"""
	Creates saliency plots for the two load conditions, and performs an LME.
	
	Arguments:
	dm		--	A DataMatrix.
	"""
	
	assert(exp == 'exp3')
	# LME
	R.load(dm)
	_dm = R.lmer('salFrom ~ cond + (1|file) + (1|scene)', nsim=nsim)
	_dm.save('output/exp3/salFrom.cond.csv')
	print _dm
	# Plot
	plot.new()
	_dm = dm.select('cond == "single"')
	salFromPlot(_dm, standalone=False, color=green[1], label='Single')
	_dm = dm.select('cond == "dual"')
	salFromPlot(_dm, standalone=False, color=orange[1], label='Dual')
	plt.legend()
	plot.save('loadPlotSalFrom', show=True)
	
def loadPlotWindow(dm):
	
	"""
	Creates a two-line window plot for each load condition
	
	Arguments:
	dm		--	A DataMatrix.
	"""
	
	assert(exp == 'exp3')
	plot.new()
	_dm = dm.select('cond == "single"')
	windowPlot(_dm, standalone=False, color=green[1], label='Single')
	_dm = dm.select('cond == "dual"')
	windowPlot(_dm, standalone=False, color=orange[1], label='Dual')
	plt.legend()
	plot.save('loadPlotWindow', show=True)
	
def masterPlot(dm, standalone=True, color=blue[1], label=None):
	
	"""
	Creates a graph in which the effect of pupil size on saliency is shown
	separately for each saccade in a trial.
	
	Arguments:
	dm			--	A DataMatrix.
	
	Keyword arguments:
	standalone	--	Indicates whether this is a standalone plot, in which case
					it will create and save the plot, or not. (default=True)
	color		--	Plot color. (default=blue[1])
	label		--	Line label. (default=None)
	"""
	
	if standalone:
		plot.new()
	xData = []
	yData = []
	eData = []
	for saccNr in [None] + range(1, maxSacc+1):
		if saccNr == None:
			_dm = dm
		else:
			_dm = dm.select('saccNr == %d' % saccNr)
		s, p, lo, up = stats.effectSlope(_dm)
		if saccNr == None:
			plt.errorbar(-2, s, yerr=[[s-lo], [up-s]], fmt='o-', color=color)
		else:
			xData.append(saccNr)
			yData.append(s)
			eData.append([lo, up])
	xData = np.array(xData)
	yData = np.array(yData)
	eData = np.array(eData)
	plt.fill_between(xData, eData[:,0], eData[:,1], color=color, alpha=.25)
	plt.plot(xData, yData, 'o-', color=color, label=label)
	plt.axhline(0, linestyle='--', color='black')
	plt.xlabel('Saccade number')
	plt.ylabel('Partial effect')
	plt.xlim(-2.5, maxSacc+.5)
	if standalone:
		plot.save('masterPlot', show=True)
	
def pupilSizePlot(dm, **args):
	
	"""Plots pupil size as a function of saccade number."""
	
	dvPlot(dm, 'pupilSize', **args)
	
def salFromPlot(dm, **args):
	
	"""Plots saliency as a function of saccade number."""
	
	dvPlot(dm, 'salFrom', **args)
	
def windowPlot(dm, standalone=True, color=blue[1], label=None):
	
	"""
	Creates a graph in which the effect of pupil size on saliency is shown
	separately for each temporal displacement. I.e. the effect of pupil size on
	trial N on saliency on trial N+1, etc.
	
	Arguments:
	dm		--	A DataMatrix.
	
	Keyword arguments:
	standalone	--	Indicates whether this is a standalone plot, in which case
					it will create and save the plot, or not. (default=True)
	color		--	Plot color. (default=blue[1])
	label		--	Line label. (default=None)
	"""
	
	if standalone:
		plot.new()
	windowRange = range(-5, 6)
	dm = dm.intertrialer(['file', 'trialId', 'saccNr'], stats.dv, \
		_range=windowRange)
	xData = []
	yData = []
	eData = []
	for r in windowRange:
		if r == 0:
			_dv = stats.dv
		elif r < 0:
			_dv = '%s_m%d' % (stats.dv, -1*r)
		else:
			_dv = '%s_p%d' % (stats.dv, r)
		print 'dv = %s' % _dv
		s, p, lo, up = stats.effectSlope(dm, _dv=_dv)
		print s
		xData.append(r)
		yData.append(s)
		eData.append([lo, up])
	xData = np.array(xData)
	yData = np.array(yData)
	eData = np.array(eData)
	plt.fill_between(xData, eData[:,0], eData[:,1], color=color, alpha=.25)
	plt.plot(windowRange, yData, 'o-', color=color, label=label)
	plt.axhline(linestyle='--', color='black')
	plt.xlabel('Pupil-size timepoint relative to saliency timepoint')
	plt.ylabel('Partial effect of pupil size')
	plt.xticks(xData)
	if standalone:
		plot.save('windowPlot', show=True)
		
# Determine experiment and make available to other modules
if 'exp1' in sys.argv:
	exp = 'exp1'
elif 'exp2' in sys.argv:
	exp = 'exp2'
elif 'exp3' in sys.argv:
	exp = 'exp3'
else:
	raise Exception('You must specify an experiment!')
plot.exp = exp
stats.exp = exp

# Sanity check
if maxSacc != 20:
	warnings.warn('For production, maxSacc should be set to 20 (is now %d)!' \
		% maxSacc)
