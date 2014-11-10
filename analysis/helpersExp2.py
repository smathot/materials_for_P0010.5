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

import analysis
from analysis import stats
from analysis.constants import *
from exparser import Plot
from exparser.TangoPalette import *
from matplotlib import pyplot as plt

def exp2InstructionPlot(dm):

	"""
	desc:
		Plots the effect of pupil size on saliency for different task
		instructions.

	arguments:
		dm:
			type:	DataMatrix
	"""

	assert(exp == 'exp2')
	Plot.new(size=smallPlot)
	for color, fmt, sceneType in [(fractalCol, 'o-', 'fractal'),
		(sceneCol, 's:', 'scene')]:
		lSlope = []
		if sceneType == 'fractal':
			x = -.1
		else:
			x = .1
		lX = []
		for inst in ['free', 'search', 'memory']:
			lX.append(x)
			_dm = dm.select('inst == "%s"' % inst).select(
				'sceneType == "%s"' % sceneType)
			s, t, lo, up = stats.effectSlope(_dm)
			lSlope.append(s)
			plt.plot([x, x], [lo, up], '-', color=color)
			x += 1
		plt.plot(lX, lSlope, fmt, color=color, label=sceneType.capitalize()+'s')
	plt.xticks(range(0,3), ['Free', 'Search', 'Memory'])
	plt.yticks([0, 2, 4, 6])
	plt.ylabel('Partial slope')
	plt.xlabel('Task')
	plt.xlim(-.5, 2.5)
	plt.ylim(slopeLim)
	plt.axhline(0, color='black', linestyle='--')
	plt.legend(frameon=False, loc='upper left')
	Plot.save('instructionPlot', folder=exp, show=show)

def exp2ModelBuild(dm):

	"""
	desc:
		Creates optimal models for exp 2. A full interactive model for the
		full dataset, and non-interactive models for each of the subsets,
		split by scene type and instruction.

	arguments:
		dm:
			type:	DataMatrix.
	"""

	assert(exp == 'exp2')
	modelRandomEffects = '(1|file)'
	modelCandidateFixedEffects = stats.modelCandidateFixedEffects[:-1]

	lfe = stats.modelBuild(dm, suffix='.full',
		modelRandomEffects=modelRandomEffects,
		modelCandidateFixedEffects=modelCandidateFixedEffects)
	model = 'salFrom ~ %s + pupilSize*inst*sceneType + (1+pupilSize+inst+sceneType|file)' \
		% (' + '.join(lfe))
	lm = stats.R.lmer(model)
	lm._print('Indirect model')
	lm.save('output/exp2/model.indirect.interactionMainRandom.csv')
	model = 'salFrom ~ pupilSize*inst*sceneType + (1+pupilSize+inst+sceneType|file)'
	lm = stats.R.lmer(model)
	lm._print('Direct model')
	lm.save('output/exp2/model.direct.interactionMainRandom.csv')

	model = 'salFrom ~ %s + pupilSize*inst + pupilSize*sceneType + (1+pupilSize+inst+sceneType|file)' \
		% (' + '.join(lfe))
	lm = stats.R.lmer(model)
	lm._print('Indirect model')
	lm.save('output/exp2/model.indirect.splitInteractionMainRandom.csv')
	model = 'salFrom ~ pupilSize*inst + pupilSize*sceneType + (1+pupilSize+inst+sceneType|file)'
	lm = stats.R.lmer(model)
	lm._print('Direct model')
	lm.save('output/exp2/model.direct.splitInteractionMainRandom.csv')

	model = 'salFrom ~ %s + pupilSize + (1+pupilSize|file)' % (' + '.join(lfe))
	lm = stats.R.lmer(model)
	lm._print('Direct model')
	lm.save('output/exp2/model.indirect.csv')
	model = 'salFrom ~ pupilSize + (1+pupilSize|file)'
	lm = stats.R.lmer(model)
	lm._print('Direct model')
	lm.save('output/exp2/model.direct.csv')

	for sceneType in dm.unique('sceneType'):
		for inst in dm.unique('inst'):
			_dm = dm.select('sceneType == "%s"' % sceneType) \
				.select('inst == "%s"' % inst)
			lfe = stats.modelBuild(_dm, suffix='.%s.%s' % (sceneType, inst),
				modelRandomEffects=modelRandomEffects,
				modelCandidateFixedEffects=modelCandidateFixedEffects)
			model = 'salFrom ~ %s + pupilSize + (1+pupilSize|file)' \
				% (' + '.join(lfe))
			lm = stats.R.lmer(model)
			lm._print('Indirect model')
			lm.save('output/exp2/model.indirect.%s.%s.csv' % (sceneType, inst))
			model = 'salFrom ~ pupilSize + (1+pupilSize|file)'
			lm = stats.R.lmer(model)
			lm._print('Direct model')
			lm.save('output/exp2/model.direct.%s.%s.csv' % (sceneType, inst))

	for sceneType in dm.unique('sceneType'):
		_dm = dm.select('sceneType == "%s"' % sceneType)
		lfe = stats.modelBuild(_dm, suffix='.%s' % sceneType,
			modelRandomEffects=modelRandomEffects,
			modelCandidateFixedEffects=modelCandidateFixedEffects)
		model = 'salFrom ~ %s + pupilSize + (1+pupilSize|file)' \
			% (' + '.join(lfe))
		lm = stats.R.lmer(model)
		lm._print('Indirect model')
		lm.save('output/exp2/model.indirect.%s.csv' % sceneType)
		model = 'salFrom ~ pupilSize + (1+pupilSize|file)'
		lm = stats.R.lmer(model)
		lm._print('Direct model')
		lm.save('output/exp2/model.direct.%s.csv' % sceneType)

	for inst in dm.unique('inst'):
		_dm = dm.select('inst == "%s"' % inst)
		lfe = stats.modelBuild(_dm, suffix='.%s' % inst,
			modelRandomEffects=modelRandomEffects,
			modelCandidateFixedEffects=modelCandidateFixedEffects)
		model = 'salFrom ~ %s + pupilSize + (1+pupilSize|file)' \
			% (' + '.join(lfe))
		lm = stats.R.lmer(model)
		lm._print('Indirect model')
		lm.save('output/exp2/model.indirect.%s.csv' % inst)
		model = 'salFrom ~ pupilSize + (1+pupilSize|file)'
		lm = stats.R.lmer(model)
		lm._print('Direct model')
		lm.save('output/exp2/model.direct.%s.csv' % inst)
