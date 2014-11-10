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

from analysis.constants import *
from analysis import stats
import numpy as np

def exp1BestPupil(dm):

	"""
	desc:
		Determines which of the various pupil-size transforms is the best
		predictor of saliency.

	arguments:
		dm:
			type:	DataMatrix.
	"""

	modelRandomEffects = '(1|file)'
	modelCandidateFixedEffects = stats.modelCandidateFixedEffects[:-1]
	lfe = stats.modelBuild(dm, suffix='.full',
		modelRandomEffects=modelRandomEffects,
		modelCandidateFixedEffects=modelCandidateFixedEffects)
	model = 'salFrom ~ %s + %%s + (1+%%s|file)' % (' + '.join(lfe))
	stats.R.load(dm)
	for m in range(1, 7):
		_model = model % ('pupilSize%d' % m, 'pupilSize%d' % m)
		lm = stats.R.lmer(_model, lmerVar='model%d' % m)
		lm._print('model%d' % m)
		lm.save('output/%s/bestPupil/lmer.pupilSize%d.csv' % (exp, m))
	m1 = 1
	for m2 in range(2, 7):
		am = stats.R.anova('model%s' % m1, 'model%s' % m2)
		am._print('%s - %s' % (m1, m2))
		am.save('output/%s/bestPupil/anova.pupilSize%d-%d.csv' \
			% (exp, m1, m2))

def exp1ModelBuild(dm):

	"""
	desc:
		Creates optimal models for exp 3. A full interactive model for the
		full dataset, and non-interactive models for each of the subsets,
		split by scene type and instruction.

	arguments:
		dm:
			type:	DataMatrix.
	"""

	assert(exp in ['exp1', 'expAll'])
	modelRandomEffects = '(1|file)'
	modelCandidateFixedEffects = stats.modelCandidateFixedEffects[:-1]

	lfe = stats.modelBuild(dm, suffix='.full',
		modelRandomEffects=modelRandomEffects,
		modelCandidateFixedEffects=modelCandidateFixedEffects)

	model = 'salFrom ~ %s + pupilSize + (1+pupilSize|file)' % (' + '.join(lfe))
	lm = stats.R.lmer(model)
	lm._print('Indirect model')
	lm.save('output/exp1/model.indirect.csv')

	model = 'salFrom ~ pupilSize + (1+pupilSize|file)'
	lm = stats.R.lmer(model)
	lm._print('Direct model')
	lm.save('output/exp1/model.direct.csv')
