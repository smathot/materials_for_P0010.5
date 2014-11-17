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

from exparser import Plot
from exparser.CsvReader import CsvReader
from analysis import helpers, constants, stats
from matplotlib import pyplot as plt
from scipy.stats import linregress
import numpy as np

def crossExpSaccadePlot(dm):

	"""
	desc:
		Creates a saccade plot with the Exp. 1 and 2 as individual lines.

	arguments:
		dm:
			type:	DataMatrix
	"""

	assert(constants.exp == 'exp1')
	Plot.new(constants.widePlot)
	helpers.saccadePlot(dm, standalone=False, color=constants.exp1Col,
		label='Exp. 1')
	constants.exp = 'exp2'
	dm = helpers.getDataMatrix(cacheId='data.%s' % constants.exp)
	dm = helpers.filter(dm, cacheId='filter.%s' % constants.exp)
	helpers.saccadePlot(dm, standalone=False, color=constants.exp2Col,
		label='Exp. 2')
	plt.legend(frameon=False)
	Plot.save('saccadePlot', folder='crossExp', show=constants.show)

def crossExpWindowPlot(dm):

	"""
	desc:
		Creates a window plot with the Exp. 1 and 2 as individual lines.

	arguments:
		dm:
			type:	DataMatrix
	"""

	assert(constants.exp == 'exp1')
	Plot.new(constants.widePlot)
	helpers.windowPlot(dm, standalone=False, color=constants.exp1Col,
		label='Exp. 1')
	constants.exp = 'exp2'
	dm = helpers.getDataMatrix(cacheId='data.%s' % constants.exp)
	dm = helpers.filter(dm, cacheId='filter.%s' % constants.exp)
	helpers.windowPlot(dm, standalone=False, color=constants.exp2Col,
		label='Exp. 2')
	plt.legend(frameon=False)
	Plot.save('windowPlot', folder='crossExp', show=constants.show)

def simpleContour(dm, bins=75, title=''):

	"""
	desc:
		Creates a single contour-correlation plot.

	arguments:
		dm:
			type:	DataMatrix

	keywords:
		bins:
			type:	int
		title:
			type:	[str, unicode]
	"""

	x = dm['pupilSize1']
	x -= x.mean()
	x /= x.std()
	y = dm['salFrom']
	h, xe, ye = np.histogram2d(x, y, bins=bins)
	h = np.rot90(h)
	plt.imshow(np.log(h), extent=[xe.min(), xe.max(), ye.min(), ye.max()],
		aspect='auto', interpolation='gaussian')
	s, i, r, p, se = linregress(x, y)
	yfit = xe*s + i
	plt.plot(xe, yfit, '-', color='white', linewidth=3)
	plt.plot(xe, yfit, '--', color='black', linewidth=1)
	plt.xlim(-2.5, 2.5)
	plt.ylim(0, 255)
	plt.xlabel('Pupil size (Z)')
	plt.ylabel('Fixation saliency (arbitrary units)')
	plt.title(title + ' (r=%.4f, p=%.4f)' % (r, p))

def crossExpContour(dm):

	"""
	desc:
		Plots a multipanel contour plot depicting the correlation between
		pupil size and fixation saliency for each experiment.

	arguments:
		dm:
			type:	DataMatrix
	"""

	assert(constants.exp == 'exp1')
	Plot.new(constants.bigPlot)
	plt.subplot(221)
	simpleContour(dm, title='Exp. 1')
	constants.exp = 'exp2'
	dm = helpers.getDataMatrix(cacheId='data.%s' % constants.exp)
	dm = helpers.filter(dm, cacheId='filter.%s' % constants.exp)
	plt.subplot(222)
	simpleContour(dm, title='Exp. 2')
	constants.exp = 'exp3'
	dm = helpers.getDataMatrix(cacheId='data.%s' % constants.exp)
	dm = helpers.filter(dm, cacheId='filter.%s' % constants.exp)
	plt.subplot(223)
	simpleContour(dm.select('cond == "single"'), title='Exp. 3 single')
	plt.subplot(224)
	simpleContour(dm.select('cond == "dual"'), title='Exp. 3 dual')
	Plot.save('correlationPlot', folder='crossExp', show=constants.show)

def crossExpDescriptives(dm):

	for exp in ['exp1', 'exp2', 'exp3']:
		dm = CsvReader('data/%s.data.csv' % exp).dataMatrix()
		if exp == 'exp1':
			dm = dm.select('trialType == "control"')
		#elif exp == 'exp3':
			#print dm.collapse(['cond'], 'rt')
			#stats.R.load(dm)
			#lm = stats.R.lmer('rt ~ cond + (1+cond|subject_nr)')
			#print lm
		rt = dm['rt']
		print 'Exp = %s' % exp
		print 'N = %d' % len(rt)
		print 'RT = %.2f ms (%.2f)' % (rt.mean(), rt.std())
		a = np.loadtxt('data/%s.fixdur.csv' % exp)
		print 'Fixdur = %.2f ms (%.2f)' % (a.mean(), a.std())
