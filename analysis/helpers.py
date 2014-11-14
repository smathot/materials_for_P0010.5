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

from constants import *
from analysis import stats
from exparser import Plot
from exparser.CsvReader import CsvReader
from exparser.Cache import cachedDataMatrix
from matplotlib import pyplot as plt
import numpy as np

@cachedDataMatrix
def filter(dm):

	"""
	desc:
		Filters and pre-processes the data.

	arguments:
		dm:
			desc:	Data.
			type:	DataMatrix

	returns:
		desc:	Data.
		type:	DataMatrix
	"""

	# For expAll, the data has already been filtered
	if exp == 'expAll':
		return dm
	# Remove practice trials for exp 3
	if exp == 'exp3':
		dm = dm.select('trialId > 3')
	# For exp 2, add the sceneType information
	if exp == 'exp2':
		print 'Adding sceneType information ...'
		dm = dm.addField('sceneType', dtype=str)
		for i in dm.range():
			if dm['scene'][i][0] == 'F':
				dm['sceneType'][i] = 'fractal'
			else:
				dm['sceneType'][i] = 'scene'
		print 'Done'
	# For exp 3, pupil size was recorded in diameter, instead of area, so we
	# need to convert. Since the units are abitrary, we don't need to take into
	# account PI. We can just square it and then turn it way down so the values
	# don't become too high. There are also some artefacts in the pupil size
	# measurements of exp 3, notably
	dm = dm.selectByStdDev([], 'pupilSize', 3., verbose=True)
	if pupilMode == 'area':
		if exp == 'exp3':
			dm = dm.addField('pupilDiam', dtype=np.float64)
			dm['pupilDiam'] = dm['pupilSize']
			dm['pupilSize'] = (.008*dm['pupilSize'])**2
	elif pupilMode == 'diameter':
		if exp != 'exp3':
			dm['pupilSize'] = np.sqrt(dm['pupilSize'])
	else:
		raise Exception('Invalid pupilMode: %s' % pupilMode)
	# Add different pupil size transforms
	for m in range(1, 7):
		dm = dm.addField('pupilSize%d' % m, dtype=float)
	dm['pupilSize1'] = dm['pupilSize']
	dm['pupilSize2'] = dm['pupilSize'] ** 2.
	dm['pupilSize3'] = dm['pupilSize'] ** 3.
	dm['pupilSize4'] = dm['pupilSize'] ** .5
	dm['pupilSize5'] = dm['pupilSize'] ** -1
	dm['pupilSize6'] = np.log(dm['pupilSize'])
	dm['pupilSize'] = dm[pupilTransform]
	if pupilZTransform:
		print('Before Z transform: M = %.4f, SD = %.4f' \
			% (dm['pupilSize'].mean(), dm['pupilSize'].std()))
		dm['pupilSize'] -= dm['pupilSize'].mean()
		dm['pupilSize'] /= dm['pupilSize'].std()
		print('After Z transform: M = %.4f, SD = %.4f' \
			% (dm['pupilSize'].mean(), dm['pupilSize'].std()))
	# Add eccentricity columns
	print 'Adding eccentricity information ...'
	dm = dm.addField('eccFrom', dtype=float)
	dm['eccFrom'] = np.sqrt( (dm['fromX']-w/2.)**2 + \
		(dm['fromY']-h/2.)**2)
	dm = dm.addField('eccTo', dtype=float)
	dm['eccTo'] = np.sqrt( (dm['toX']-w/2.)**2 + \
		(dm['toY']-h/2.)**2)
	print 'Done'
	return dm

@cachedDataMatrix
def getDataMatrix():

	"""
	desc:
		Reads the data for the current experiment.

	returns:
		desc:	Data.
		type:	DataMatrix
	"""

	print 'Reading ...'
	dm = CsvReader('data/%s.fix.csv' % exp).dataMatrix()
	print 'N = %d' % len(dm)
	print 'Done'
	return dm

def saccadePlot(dm, standalone=True, color=blue[1], label=None):

	"""
	desc:
		Creates a graph in which the effect of pupil size on saliency is shown
		separately for each saccade in a trial.

	arguments:
		dm:
			desc:	Data
			type:

	keywords:
		standalone:
			desc:	Indicates whether this is a standalone plot, in which case
					it will create and save the plot, or not.
			type:	bool
		color:
			desc:	Plot color.
			type:	[str, unicode]
		label:
			desc:	Line label.
			type:	[str, unicode]
	"""

	if standalone:
		Plot.new(size=widePlot)
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
			if standalone:
				x = -1
			elif exp == 'exp1':
				x = -1.2
			else:
				x = -.8
			plt.errorbar(x, s, yerr=[[s-lo], [up-s]], capsize=0, fmt='o-',
				color=color)
		else:
			xData.append(saccNr)
			yData.append(s)
			eData.append([lo, up])
	xData = np.array(xData)
	yData = np.array(yData)
	eData = np.array(eData)
	plt.fill_between(xData, eData[:,0], eData[:,1], color=color, alpha=.1)
	plt.plot(xData, yData, 'o-', color=color, label=label)
	plt.axhline(0, linestyle='--', color='black')
	plt.xlabel('Saccade number')
	plt.xlim(-2, maxSacc+1)
	plt.xticks([-1]+range(1, 21), ['Full']+range(1, 21))
	plt.ylabel('Partial slope')
	plt.yticks(slopeTicks[exp])
	plt.ylim(slopeLim[exp])
	if standalone:
		Plot.save('saccadePlot', folder=exp, show=show)

def windowPlot(dm, standalone=True, color=blue[1], label=None):

	"""
	desc:
		Creates a graph in which the effect of pupil size on saliency is shown
		separately for each temporal displacement. I.e. the effect of pupil size
		on trial N on saliency on trial N+1, etc.

	arguments:
		dm:
			type:	DataMatrix

	keywords:
		standalone:
			desc:	Indicates whether this is a standalone plot, in which case
					it will create and save the plot, or not.
			type:	bool
		color:
			desc:	Plot color.
			type:	[str, unicode]
		label:
			desc:	Line label.
			type:	[str, unicode]
	"""

	if standalone:
		Plot.new(widePlot)
	dm = dm.intertrialer(['file', 'trialId', 'saccNr'], 'salFrom',
		_range=windowRange)
	xData = []
	yData = []
	eData = []
	for r in windowRange:
		if r == 0:
			_dv = 'salFrom'
		elif r < 0:
			_dv = 'salFrom_m%d' % (-1*r)
		else:
			_dv = 'salFrom_p%d' % r
		print 'dv = %s' % _dv
		s, t, lo, up = stats.effectSlope(dm, dv=_dv)
		print s
		xData.append(r)
		yData.append(s)
		eData.append([lo, up])
	xData = np.array(xData)
	yData = np.array(yData)
	eData = np.array(eData)
	plt.fill_between(xData, eData[:,0], eData[:,1], color=color, alpha=.1)
	plt.plot(windowRange, yData, 'o-', color=color, label=label)
	plt.axhline(linestyle='--', color='black')
	plt.xlabel('Pupil-size timepoint relative to saliency timepoint')
	plt.xticks(windowRange)
	plt.xlim(windowRange[0], windowRange[-1])
	plt.ylabel('Partial slope')
	plt.yticks(slopeTicks[exp])
	plt.ylim(slopeLim[exp])
	if standalone:
		Plot.save('windowPlot', folder=exp, show=show)
