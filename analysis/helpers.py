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
import analysis
from analysis import plot, stats
# Direct import so that we can invoke it from the command line
from analysis.stats import modelBuild, matchCond

# The maximum saccade number to include in masterplot (production value=20)
maxSacc = 20

def _exp1(dm):

	"""Performs the full analysis for experiment 1."""

	assert(analysis.exp == 'exp1')
	# Generic
	masterPlot(dm)
	pupilSizePlot(dm)
	salFromPlot(dm)
	windowPlot(dm)

def _exp2(dm):

	"""Performs the full analysis for experiment 2."""

	assert(analysis.exp == 'exp2')
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

	assert(analysis.exp in ['exp3', 'exp3.matched'])
	# Generic
	masterPlot(dm)
	pupilSizePlot(dm)
	salFromPlot(dm)
	windowPlot(dm)
	# Experiment specific
	loadPerf(dm)
	loadPlot(dm)
	loadPlotPupilSize(dm)
	loadPlotSalFrom(dm)
	loadPlotWindow(dm)

def crossExp(dm):

	"""
	Performs a cross-experimental analysis, calculating the partial effect of
	pupilSize on salFrom for exp 1, exp2, exp 3 (single), and exp 3 (dual).

	Note: This should be called as the last part of the chain and requires
	exp 1.

	Arguments:
	dm		--	A DataMatrix.
	"""

	# Has to be called as the final analysis for exp 1
	assert(analysis.exp == 'exp1')
	assert('crossExp' == sys.argv[-1])
	# First the saccade number plot. This only includes Experiment 1 and 2.
	plot.new()
	masterPlot(dm, standalone=False, color=blue[1], label='Exp 1')
	analysis.exp = 'exp2'
	dm = filter(getDataMatrix())
	masterPlot(dm, standalone=False, color=orange[1], label='Exp 2')
	plt.legend(frameon=False)
	analysis.exp = 'expCross'
	plot.save('saccNrPlot', show=True)

	# Now the main master plot
	plot.new()
	# Exp 1
	analysis.exp = 'exp1'
	dm = filter(getDataMatrix())
	s, p, lo, up = stats.effectSlope(dm)
	plt.bar(0, s, edgecolor='black', color=blue[1], width=.8)
	plt.plot([.4, .4], [lo, up], '-', color='black')
	# Exp 2
	analysis.exp = 'exp2'
	dm = filter(getDataMatrix())
	s, p, lo, up = stats.effectSlope(dm)
	plt.bar(1, s, edgecolor='black', color=orange[1], width=.8)
	plt.plot([1.4, 1.4], [lo, up], '-', color='black')
	# Exp 3, separately for single and dual cond
	analysis.exp = 'exp3'
	dm = filter(getDataMatrix())
	_dm = dm.select('cond == "single"')
	s, p, lo, up = stats.effectSlope(_dm)
	plt.bar(2, s, edgecolor='black', color=green[2], width=.8)
	plt.plot([2.4, 2.4], [lo, up], '-', color='black')
	_dm = dm.select('cond == "dual"')
	s, p, lo, up = stats.effectSlope(_dm)
	plt.bar(3, s, edgecolor='black', color=green[2], width=.8)
	plt.plot([3.4, 3.4], [lo, up], '-', color='black')
	plt.axhline(linestyle='--', color='black')
	plt.xticks( [.4, 1.4, 2.4, 3.4], ['Exp 1', 'Exp 2', 'Exp 3 (single)', \
		'Exp 3 (dual)'])
	plt.xlim(-.5, 4.3)
	analysis.exp = 'expCross'
	plot.save('masterPlot', show=True)

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
	if analysis.exp in ['exp3', 'exp3.matched']:
		dm = dm.select('trialId > 3')
	# Add eccentricity columns
	print 'Adding eccentricity information ...'
	dm = dm.addField('eccFrom', dtype=float)
	dm['eccFrom'] = np.sqrt( (dm['fromX']-analysis.w/2.)**2 + \
		(dm['fromY']-analysis.h/2.)**2)
	dm = dm.addField('eccTo', dtype=float)
	dm['eccTo'] = np.sqrt( (dm['toX']-analysis.w/2.)**2 + \
		(dm['toY']-analysis.h/2.)**2)
	print 'Done'
	return dm

def getDataMatrix():

	"""
	Reads the data for the current experiment.

	Returns:
	A DataMatrix.
	"""

	print 'Reading ...'
	dm = CsvReader('data/%s.fix.csv' % analysis.exp).dataMatrix()
	print 'Done'
	return dm

def loadHist(dm):

	"""
	Shows distribution plots of saccNr, pupilSize, and salFrom for the single
	and dual-task conditions.

	Note: This is only applicable for experiment 3.

	Arguments:
	dm		--	A DataMatrix.
	"""

	assert(analysis.exp in ['exp3', 'exp3.matched'])

	plot.new(size=plot.hi)

	dmSingle = dm.select("cond == 'single'")
	dmDual = dm.select("cond == 'dual'")

	plt.subplot(3,1,1)
	ySingle = []
	yDual = []
	for i in range(1, maxSacc+1):
		ySingle.append(len(dmSingle.select('saccNr == %d' % i)))
		yDual.append(len(dmDual.select('saccNr == %d' % i)))
	plt.plot(ySingle, ',-', color=blue[1], label='Single')
	plt.plot(yDual, ',-', color=green[1], label='Dual')
	plt.title('N per saccNr')
	plt.legend(frameon=False)

	plt.subplot(3,1,2)
	ySingle = []
	yDual = []
	for i in range(0,255):
		ySingle.append(len(dmSingle.select('salFrom == %d' % i)))
		yDual.append(len(dmDual.select('salFrom == %d' % i)))
	plt.plot(ySingle, ',-', color=blue[1], label='Single')
	plt.plot(yDual, ',-', color=green[1], label='Dual')
	plt.title('N per salFrom')
	plt.gca().set_yscale('log')
	plt.legend(frameon=False)

	plt.subplot(3,1,3)
	plt.hist(dmSingle['_pupilSize'], bins=100, color=blue[1], label='single', \
		histtype='stepfilled', alpha=.5)
	plt.hist(dmDual['_pupilSize'], bins=100, color=green[1], label='dual', \
		histtype='stepfilled', alpha=.5)
	plt.title('pupilSize')
	plt.legend(frameon=False)

	plot.save('loadHist', show=True)

def instructionPlot(dm):

	"""
	Plots the effect of pupil size on saliency for different task instructions.
	Also builds optimal models for all instrunctions.

	Note: This is only applicable for experiment 2.

	Arguments:
	dm		--	A DataMatrix.
	"""

	assert(analysis.exp == 'exp2')
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
	plt.legend(frameon=False)
	plot.save('instructionPlot', show=True)

def loadPerf(dm):

	"""
	Analyzes the behavioral perform for the different memory-load conditions.

	Note: This is only applicable to experiment 3.

	Arguments:
	dm		--	A DataMatrix.
	"""

	assert(analysis.exp in ['exp3', 'exp3.matched'])
	# Process the visual-search performance. Due to a bug in the experiment,
	# the actual response is not retrievable. However, we can retrieve RTs and
	# whether a timeout occurred.
	_dm = CsvReader('data/exp3.data.csv').dataMatrix()
	_dm = _dm.addField('search_timeout', dtype=int)
	_dm['search_timeout'][np.where(_dm['search_rt'] > 19999)] = 1
	pm = PivotMatrix(_dm, ['cond'], ['subject_nr'], dv='search_timeout')
	pm.save('output/exp3/searchTimeout.csv')
	pm._print('Visual search timeout')
	_dm = _dm.select('search_timeout == 0')
	pm = PivotMatrix(_dm, ['cond'], ['subject_nr'], dv='search_rt')
	pm.save('output/exp3/searchRT.csv')
	pm._print('Visual search RTs (non-timeout only)')
	# Process the digit count performance. We first need to do some recoding
	# to make sure that the response is an int.
	_dm = _dm.select('cond == "dual"', verbose=False)
	_dm = _dm.addField('count_correct', dtype=int, default=0)
	for i in _dm.range():
		try:
			int(_dm['count_response'][i])
		except:
			# If the response is not an int, it's definitely incorrect
			continue
		if int(_dm['count_response'][i]) == _dm['digitCount'][i]:
			_dm['count_correct'][i] = 1
	pm = PivotMatrix(_dm, ['subject_nr'], ['subject_nr'], dv='count_correct')
	pm.save('output/exp3/countPerf.csv')
	pm._print('Digit count performance (dual-task only)')

def loadPlot(dm):

	"""
	Plots the effect of pupil size on saliency for different memory-load
	conditions, where lines correspond to load conditions. Also builds optimal
	models for the two conditions.

	Note: This is only applicable to experiment 3.

	Arguments:
	dm		--	A DataMatrix.
	"""

	assert(analysis.exp in ['exp3', 'exp3.matched'])
	modelBuild(dm.select('cond == "single"'), suffix='.single')
	modelBuild(dm.select('cond == "dual"'), suffix='.dual')
	plot.new()
	_dm = dm.select('cond == "single"')
	masterPlot(_dm, standalone=False, color=green[1], label='Single')
	_dm = dm.select('cond == "dual"')
	masterPlot(_dm, standalone=False, color=orange[1], label='Dual')
	plt.legend(frameon=False)
	plot.save('loadPlot', show=True)

def loadPlotPupilSize(dm):

	"""
	Creates pupil-size plots for the two load conditions, and performs an LME.

	Arguments:
	dm		--	A DataMatrix.
	"""

	assert(analysis.exp in ['exp3', 'exp3.matched'])
	# LME
	R.load(dm)
	_dm = R.lmer('pupilSize ~ cond + (1|file) + (1|scene)', nsim=nsim)
	_dm.save('output/%s/pupilSize.cond.csv' % analysis.exp)
	print _dm
	# Plot
	plot.new()
	_dm = dm.select('cond == "single"')
	pupilSizePlot(_dm, standalone=False, color=green[1], label='Single')
	_dm = dm.select('cond == "dual"')
	pupilSizePlot(_dm, standalone=False, color=orange[1], label='Dual')
	plt.legend(frameon=False)
	plot.save('loadPlotPupilSize', show=True)

def loadPlotSalFrom(dm):

	"""
	Creates saliency plots for the two load conditions, and performs an LME.

	Arguments:
	dm		--	A DataMatrix.
	"""

	assert(analysis.exp in ['exp3', 'exp3.matched'])
	# LME
	stats.R.load(dm)
	_dm = stats.R.lmer('salFrom ~ cond + (1|file) + (1|scene)', nsim=stats.nsim)
	_dm.save('output/%s/salFrom.cond.csv' % analysis.exp)
	print _dm

	plot.new()
	y1 = dm.select('cond == "single"')['salFrom'].mean()
	y2 = dm.select('cond == "dual"')['salFrom'].mean()
	my = .5*(y1 + y2)
	dy = y2 - y1
	y1A = my + .5 * _dm['ci95up'][1]
	y1B = my + .5 * _dm['ci95lo'][1]
	y2A = my - .5 * _dm['ci95up'][1]
	y2B = my - .5 * _dm['ci95lo'][1]
	plt.bar(0, y1, color=green[1])
	plt.plot([.4, .4], [y1A, y1B], '-', color='black')
	plt.bar(1, y2, color=orange[1])
	plt.plot([1.4, 1.4], [y2A, y2B], '-', color='black')
	plt.ylim(13, 16)
	plt.xlim(-.5, 2.3)
	plt.xticks([.4, 1.4], ['Single', 'Dual'])
	plt.ylabel('Saliency (arbitrary units)')
	plot.save('barPlotSalFrom', show=True)
	# Saccade number plot
	plot.new()
	_dm = dm.select('cond == "single"')
	salFromPlot(_dm, standalone=False, color=green[1], label='Single')
	_dm = dm.select('cond == "dual"')
	salFromPlot(_dm, standalone=False, color=orange[1], label='Dual')
	plt.legend(frameon=False)
	plot.save('loadPlotSalFrom', show=True)

def loadPlotWindow(dm):

	"""
	Creates a two-line window plot for each load condition

	Arguments:
	dm		--	A DataMatrix.
	"""

	assert(analysis.exp in ['exp3', 'exp3.matched'])
	plot.new()
	_dm = dm.select('cond == "single"')
	windowPlot(_dm, standalone=False, color=green[1], label='Single')
	_dm = dm.select('cond == "dual"')
	windowPlot(_dm, standalone=False, color=orange[1], label='Dual')
	plt.legend(frameon=False)
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

# Sanity check
if maxSacc != 20:
	warnings.warn('For production, maxSacc should be set to 20 (is now %d)!' \
		% maxSacc)
