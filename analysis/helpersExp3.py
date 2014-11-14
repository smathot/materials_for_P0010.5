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

from analysis import stats
from analysis.constants import *
from exparser import Plot
from matplotlib import pyplot as plt

def exp3ModelBuild(dm):

	"""
	desc:
		Creates optimal models for exp 3. A full interactive model for the
		full dataset, and non-interactive models for each of the subsets,
		split by scene type and instruction.

	arguments:
		dm:
			type:	DataMatrix.
	"""

	assert(exp == 'exp3')
	modelRandomEffects = '(1|file)'
	modelCandidateFixedEffects = stats.modelCandidateFixedEffects[:-1]

	lfe = stats.modelBuild(dm, suffix='.full',
		modelRandomEffects=modelRandomEffects,
		modelCandidateFixedEffects=modelCandidateFixedEffects)

	model = 'salFrom ~ %s + cond + (1+cond|file)' % (' + '.join(lfe))
	lm = stats.R.lmer(model)
	lm._print('Indirect model')
	lm.save('output/exp3/model.cond.indirect.csv')

	model = 'salFrom ~ cond + (1+cond|file)'
	lm = stats.R.lmer(model)
	lm._print('Direct model')
	lm.save('output/exp3/model.cond.direct.csv')

	model = 'salFrom ~ %s + pupilSize*cond + (1+pupilSize+cond|file)' \
		% (' + '.join(lfe))
	lm = stats.R.lmer(model)
	lm._print('Indirect model')
	lm.save('output/exp3/model.indirect.interactionMainRandom.csv')

	model = 'salFrom ~ pupilSize*cond + (1+pupilSize+cond|file)'
	lm = stats.R.lmer(model)
	lm._print('Direct model')
	lm.save('output/exp3/model.direct.interactionMainRandom.csv')

	model = 'salFrom ~ %s + pupilSize + (1+pupilSize|file)' % (' + '.join(lfe))
	lm = stats.R.lmer(model)
	lm._print('Indirect model')
	lm.save('output/exp3/model.indirect.csv')

	model = 'salFrom ~ pupilSize + (1+pupilSize|file)'
	lm = stats.R.lmer(model)
	lm._print('Direct model')
	lm.save('output/exp3/model.direct.csv')

	for cond in dm.unique('cond'):
		_dm = dm.select('cond == "%s"' % cond)
		lfe = stats.modelBuild(_dm, suffix='.%s' % cond,
			modelRandomEffects=modelRandomEffects,
			modelCandidateFixedEffects=modelCandidateFixedEffects)
		model = 'salFrom ~ %s + pupilSize + (1+pupilSize|file)' \
			% (' + '.join(lfe))
		lm = stats.R.lmer(model)
		lm._print('Indirect model')
		lm.save('output/exp3/model.indirect.%s.csv' % cond)
		model = 'salFrom ~ pupilSize + (1+pupilSize|file)'
		lm = stats.R.lmer(model)
		lm._print('Direct model')
		lm.save('output/exp3/model.direct.%s.csv' % cond)

def exp3SaccadePlot(dm):

	"""
	desc:
		Creates a saccade plot with the different task conditions as individual
		lines.

	arguments:
		dm:
			type:	DataMatrix
	"""

	from analysis import helpers
	dmSingle = dm.select('cond == "single"')
	dmDual = dm.select('cond == "dual"')
	Plot.new(widePlot)
	helpers.saccadePlot(dmSingle, standalone=False, color=exp3SingleCol,
		label='Single task')
	helpers.saccadePlot(dmDual, standalone=False, color=exp3DualCol,
		label='Dual task')
	plt.legend(frameon=False)
	Plot.save('saccadePlot.task', folder=exp, show=show)

def exp3WindowPlot(dm):

	"""
	desc:
		Creates a window plot with the different task conditions as individual
		lines.

	arguments:
		dm:
			type:	DataMatrix
	"""

	from analysis import helpers
	dmSingle = dm.select('cond == "single"')
	dmDual = dm.select('cond == "dual"')
	Plot.new(widePlot)
	helpers.windowPlot(dmSingle, standalone=False, color=exp3SingleCol,
		label='Single task')
	helpers.windowPlot(dmDual, standalone=False, color=exp3DualCol,
		label='Dual task')
	plt.legend(frameon=False)
	Plot.save('windowPlot.task', folder=exp, show=show)
