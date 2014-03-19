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

import os
import sys
import warnings
import numpy as np
from scipy.spatial.distance import cdist
from matplotlib import pyplot as plt
from exparser.RBridge import RBridge
from exparser.DataMatrix import DataMatrix
from exparser.Cache import cachedDataMatrix
import analysis

# The number of simulations for the p-value estimation (production value=10000)
nsim = 10000
# Dependent and independent variables.
dv = 'salFrom'
iv = 'pupilSize'
# The random effects part of the model
modelRandomEffects = '(1+%s|file)' % iv
# Determines whether we should use `pvals.fnc()` to estimate p-values or use the
# standard-error-based p-values of `getSummary.mer()`.
modelPvals = False
# All fixed effects that should be considered by the model-construction
# algorithm. Note that we now exclude `to[X]` fixed effects, because they
# correlate too highly with the `from[X]` effects.
modelCandidateFixedEffects = ['saccNr', 'lumFrom', 'eccFrom', 'fromX', \
	'fromY', 'iSacc', 'size', 'pupilSize']

def effectSlope(dm, _dv=dv):

	"""
	Determines the slope of the partial effect of pupilSize on saliency.

	Arguments:
	dm		--	A DataMatrix.

	Keyword arguments:
	_dv	--	The dependent variable. (default=dv)

	Returns:
	A (slope, p, ci96lo, ci95up) tuple with the slope, p-value, and confidence
	interval.
	"""

	R.load(dm)
	_dm = R.lmer(formula(dm, _dv=_dv), nsim=nsim, pvals=modelPvals)
	_dm = _dm.select('effect == "pupilSize"', verbose=False)
	return _dm['est'][0], _dm['p'][0], _dm['ci95lo'][0], _dm['ci95up'][0]

def fixedEffects():

	"""
	Specifies the fixed effects for the model, which depends on the experiment.

	Important note: When modelCandidateFixedEffects or modelRandomEffects are
	changed, these fixed effects should be estimated again using `modelBuild()`.

	Returns:
	A list of fixed effects.
	"""

	if analysis.exp == 'exp1':
		return ['trialId', 'saccNr', 'lumFrom', 'eccFrom', 'fromX', 'fromY', \
			'iSacc', 'size']
	if analysis.exp == 'exp2':
		return ['trialId', 'lumFrom', 'eccFrom', 'fromY', 'size']
	if analysis.exp in ['exp3', 'exp3.matched']:
		return ['trialId', 'saccNr', 'lumFrom', 'eccFrom', 'fromX', 'fromY', \
			'iSacc', 'size']

def formula(dm, _dv=dv, partial=True):

	"""
	Generates the R formula for the current experiment.

	Arguments:
	dm		--	A DataMatrix.

	Keyword arguments:
	_dv		--	The dependent variable. (default=dv)
	partial	--	Indicates whether other fixed effects should be included
				for the purpose of partialling. (default=True)

	Returns:
	A string with the R formula.
	"""

	if partial:
		# Make sure that we only include fixed effects that actually occur multiple
		# times in the data.
		lfe = []
		for fe in fixedEffects():
			if dm.count(fe) > 1:
				lfe.append(fe)
			else:
				print 'Excluding %s as fixed effect' % fe
		f = '%s ~ %s + %s + %s' % (_dv, ' + '.join(lfe), iv, modelRandomEffects)
	else:
		f = '%s ~ %s + %s' % (_dv, iv, modelRandomEffects)
	print 'Formula = %s' % f
	return f

def dvMatch(dm, _dv, maxDiff=None):

	"""
	Matches the single and dual task conditions in Experiment 3 based on a
	specific dv.

	Arguments:
	dm		--	A DataMatrix.
	_dv		--	The dv to match on.
	maxDiff	--	The maximum-difference threshold or None to match by .1*stdev.
				(default=None)

	Returns:
	A DataMatrix with all unmatchable rows removed.
	"""

	assert(analysis.exp in ['exp3', 'exp3.matched'])
	if '__match__' not in dm.columns():
		dm = dm.addField('__match__')
	dm['__match__'] = 0
	if maxDiff == None:
		maxDiff = .1 * dm[_dv].std()
	print 'maxDiff(%s) = %.4f' % (_dv, maxDiff)
	dm1 = dm.select('cond == "single"', verbose=False)
	dm2 = dm.select('cond == "dual"', verbose=False)
	a1 = dm1[_dv]
	a2 = dm2[_dv]
	a1.shape = 	len(a1), 1
	a2.shape = 	len(a2), 1
	print 'Calculating distance matrix ...'
	d = cdist(a1, a2)
	print 'Done!'
	i = 0
	while False in np.isnan(d):
		c, r = np.where(d == np.nanmin(d))
		c = c[0]
		r = r[0]
		diff = d[c,r]
		if diff > maxDiff:
			print 'Break!'
			break
		dm1['__match__'][c] = 1
		dm2['__match__'][r] = 1
		d[c] = np.nan
		d[:,r] = np.nan
		if i % 100 == 0:
			print '%.5d\t%.5d\t%.5d\t%.4f' % (i, c, r, diff)
		i += 1
	dm1 = dm1.select('__match__ == 1')
	dm2 = dm2.select('__match__ == 1')
	return dm1 + dm2

def matchCond(dm):

	"""
	Matches the single-task and dual-task conditions in Experiment 3 based on
	pupilSize and salFrom. This function will set the current experiment to
	`exp3.matched`.

	All trials that cannot be matched are discarded.

	Note: this is only applicable to exp 3.

	Arguments:
	dm		--	A DataMatrix.

	Returns:
	A DataMatrix that contains only the matched trials.
	"""

	assert(analysis.exp == 'exp3')
	analysis.exp = 'exp3.matched'
	lBefore = len(dm)
	cachePath = 'cache/matchCond.npy'
	if '--no-cache' not in sys.argv and os.path.exists(cachePath):
		print 'Retrieving from cache (%s) ...' % cachePath
		matchDm = DataMatrix(cachePath)
	else:
		matchDm = None
		for _dm in dm.group('file'):
			_dm = dvMatch(_dm, 'salFrom')
			_dm = dvMatch(_dm, 'pupilSize')
			if matchDm == None:
				matchDm = _dm
			else:
				matchDm += _dm
		matchDm.save(cachePath)
	lAfter = len(matchDm)
	print 'Matched %d of %d trials (%.2f%%)' % (lAfter, lBefore, \
		100.*lAfter/lBefore)
	return matchDm

def modelBuild(dm, suffix=''):

	"""
	Incrementally builds the optimal model that contains only fixed effects that
	significantly contribute to the model quality. The results of this model
	should be used by fixedEffects().

	Arguments:
	dm		--	A DataMatrix.

	Keyword arguments:
	suffix	--	A suffix to label and save the resulting model. (default='')
	"""

	# We include trialId by default, to have at least one fixed effect to begin
	# with. This is ok, because trialId is always included anyway.
	lfe = ['trialId']
	R.load(dm)
	for fe in modelCandidateFixedEffects:
		f1 = '%s ~ %s + %s' % (dv, ' + '.join(lfe), modelRandomEffects)
		f2 = '%s ~ %s + %s' % (dv, ' + '.join(lfe+[fe]), modelRandomEffects)
		print '\nComparing:'
		print f1
		print f2
		dm1 = R.lmer(f1, lmerVar='lmer1', nsim=nsim, pvals=modelPvals)
		dm2 = R.lmer(f2, lmerVar='lmer2', nsim=nsim, pvals=modelPvals)
		_dm = R.anova('lmer1', 'lmer2')
		_dm._print(sign=5)
		p = float(_dm['Pr(>Chisq)'][1])
		if p < .05:
			print 'Including %s' % fe
			lfe.append(fe)
			dmBest = dm2
		else:
			print 'Not including %s' % fe
			dmBest = dm1
	dmBest._print(title='Best model for %s%s' % (analysis.exp, suffix))
	dmBest.save('output/%s/bestModel%s.csv' % (analysis.exp, suffix))

def formatDm(dm, lm):

	"""
	Formats an LME table for the manuscript.

	Arguments:
	dm		--	The full DataMatrix.
	lm		--	The lmer outpur as a DataMatrix.

	Returns:
	A nicely formatted DataMatrix.
	"""

	lm = lm[1:-3]
	lm = lm.selectColumns(['effect', 't', 'se', 'est'])
	lm = lm.addField('ANS', dtype=str, default='0')
	for i in lm.range():
		effect = lm['effect'][i]
		if ':' in effect:
			# The ANS is not applicable to interactions
			lm['ANS'][i] = '-'
		else:
			std = dm[effect].std()
			lm['ANS'][i] = np.abs(lm['est'][i]*std)
	lm.rename('effect', 'Factor')
	lm.rename('t', '*t* value')
	lm.rename('se', 'SE')
	lm.rename('est', 'Slope')
	return lm

def modelTables(dm):

	"""
	Prepares the model tables for the manuscript. These are written directly
	to the manuscript tables folder.

	Arguments:
	dm		--	A DataMatrix.
	"""

	@cachedDataMatrix
	def getLmDirect(dm):
		return R.lmer(formula(dm, partial=False), nsim=nsim, pvals=modelPvals)
	@cachedDataMatrix
	def getLmPartial(dm):
		return R.lmer(formula(dm), nsim=nsim, pvals=modelPvals)

	if analysis.exp == 'exp3':

		R.load(dm.select('cond == "single"'))
		lmDirect = getLmDirect(dm, cacheId='lmDirect.single.%s' % analysis.exp)
		lmDirect = formatDm(dm, lmDirect)
		lmDirect._print(sign=5)
		lmDirect.save(analysis.manuscriptTablesFolder+'%s.direct.single.csv' \
			% analysis.exp)
		lmPartial = getLmPartial(dm, cacheId='lmPartial.single.%s' % analysis.exp)
		lmPartial = formatDm(dm, lmPartial)
		lmPartial.save(analysis.manuscriptTablesFolder+'%s.partial.single.csv' \
			% analysis.exp)
		lmPartial._print(sign=5)

		R.load(dm.select('cond == "dual"'))
		lmDirect = getLmDirect(dm, cacheId='lmDirect.dual.%s' % analysis.exp)
		lmDirect = formatDm(dm, lmDirect)
		lmDirect._print(sign=5)
		lmDirect.save(analysis.manuscriptTablesFolder+'%s.direct.dual.csv' \
			% analysis.exp)
		lmPartial = getLmPartial(dm, cacheId='lmPartial.dual.%s' % analysis.exp)
		lmPartial = formatDm(dm, lmPartial)
		lmPartial.save(analysis.manuscriptTablesFolder+'%s.partial.dual.csv' \
			% analysis.exp)
		lmPartial._print(sign=5)

	else:

		R.load(dm)
		lmDirect = getLmDirect(dm, cacheId='lmDirect.%s' % analysis.exp)
		lmDirect = formatDm(dm, lmDirect)
		lmDirect._print(sign=5)
		lmDirect.save(analysis.manuscriptTablesFolder+'%s.direct.csv' \
			% analysis.exp)

		lmPartial = getLmPartial(dm, cacheId='lmPartial.%s' % analysis.exp)
		lmPartial = formatDm(dm, lmPartial)
		lmPartial.save(analysis.manuscriptTablesFolder+'%s.partial.csv' \
			% analysis.exp)
		lmPartial._print(sign=5)

# Sanity checks
if nsim != 10000 and modelPvals:
	warnings.warn( \
		'For production, if modelPvals is True, then nsim should be set to 10000 (is now %d)!' \
		% nsim)

# Start the connection to R
R = RBridge()
