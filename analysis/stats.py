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

import warnings
from exparser.RBridge import RBridge

# The number of simulations for the p-value estimation (production value=10000)
nsim = 100
# Dependent and independent variables.
dv = 'salFrom'
iv = 'pupilSize'

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
	_dm = R.lmer(formula(dm, _dv=_dv), nsim=nsim)
	_dm = _dm.select('effect == "pupilSize"', verbose=False)
	return _dm['est'][0], _dm['p'][0], _dm['ci95lo'][0], _dm['ci95up'][0]

def fixedEffects():
	
	"""
	Specifies the fixed effects for the model, which depends on the experiment.
	
	Returns:
	A list of fixed effects.
	"""
	
	if exp == 'exp1':
		return ['trialId', 'saccNr', 'lumFrom', 'fromX', 'fromY', 'iSacc', \
			'size']
	if exp == 'exp2':
		return ['trialId', 'saccNr', 'lumFrom', 'lumTo', 'fromY', 'size']
	if exp == 'exp3':
		return ['trialId', 'saccNr', 'lumFrom', 'fromX', 'fromY', 'iSacc', \
			'size']

def formula(dm, _dv=dv):
	
	"""
	Generates the R formula for the current experiment.
	
	Arguments:
	dm	--	A DataMatrix.
	
	Keyword arguments:
	_dv	--	The dependent variable. (default=dv)
	
	Returns:
	A string with the R formula.
	"""
	
	# Make sure that we only include fixed effects that actually occur multiple
	# times in the data.
	lfe = []
	for fe in fixedEffects():
		if dm.count(fe) > 1:
			lfe.append(fe)
		else:
			print 'Excluding %s as fixed effect' % fe
	f = '%s ~ %s + %s + (1|file) + (1|scene)' % (_dv, ' + '.join(lfe), iv)
	print f
	return f

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
	
	fixedEffects = ['saccNr', 'lumFrom', 'lumTo', 'fromX', 'fromY', 'toX', \
		'toY', 'iSacc', 'size', 'pupilSize']
	# We include trialId by default, to have at least one fixed effect to begin
	# with. This is ok, because trialId is always included anyway.
	lfe = ['trialId']
	R.load(dm)
	for fe in fixedEffects:
		f1 = '%s ~ %s + (1|file) + (1|scene)' % (dv, ' + '.join(lfe))
		f2 = '%s ~ %s + (1|file) + (1|scene)' % (dv, ' + '.join(lfe+[fe]))
		print '\nComparing:'
		print f1
		print f2
		dm1 = R.lmer(f1, lmerVar='lmer1', nsim=nsim)
		dm2 = R.lmer(f2, lmerVar='lmer2', nsim=nsim)
		_dm = R.anova('lmer1', 'lmer2')
		print _dm
		p = float(_dm['Pr(>Chisq)'][1])
		if p < .05:
			print 'Including %s' % fe
			lfe.append(fe)
			dmBest = dm2
		else:
			print 'Not including %s' % fe
			dmBest = dm1
	dmBest._print(title='Best model for %s%s' % (exp, suffix))
	dmBest.save('output/%s/bestModel%s.csv' % (exp, suffix))
	
# Sanity checks
if nsim != 10000:
	warnings.warn('For production, nsim should be set to 10000 (is now %d)!' \
		% nsim)

# Start the connection to R
R = RBridge()
