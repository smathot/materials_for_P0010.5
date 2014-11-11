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
from analysis import helpers, constants
from matplotlib import pyplot as plt

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
