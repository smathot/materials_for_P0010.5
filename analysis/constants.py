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
from exparser.TangoPalette import *

# The maximum saccade number to include in masterplot (production value=20)
maxSacc = 20
# The range of displacements for `windowPlot()`
windowRange = range(-5, 6)
# The upper and lower limit for the slope axis in the plots
slopeLim = {
	'exp1' : (-2, 7),
	'exp2' : (-2, 7),
	'exp3' : (-.5, 2),
	}
slopeTicks = {
	'exp1' : [0, 2, 4, 6],
	'exp2' : [0, 2, 4, 6],
	'exp3' : [0, .5, 1, 1.5],
	}
# Line colors
exp1Col = blue[1]
exp2Col = orange[1]
exp3SingleCol = green[2]
exp3DualCol = red[2]
fractalCol = orange[1]
sceneCol = orange[2]
pupilMode = 'diameter'
 # The best transform is selected based on exp1
pupilTransform = 'pupilSize5'
pupilZTransform = True
# Plot dimensions
widePlot = 8, 4
smallPlot = 4, 4
bigPlot = 8, 8
# Indicates whether the plots should be shown
show = '--show' in sys.argv
# The random effects part of the model
modelRandomEffects = '(1+pupilSize|file)'
# All fixed effects that should be considered by the model-construction
# algorithm. Note that we now exclude `to[X]` fixed effects, because they
# correlate too highly with the `from[X]` effects.
modelCandidateFixedEffects = ['saccNr', 'lumFrom', 'eccFrom', 'fromX',
	'fromY', 'iSacc', 'size', 'pupilSize']
# Determine experiment and make available to other modules. The experiments also
# had different display resolutions.
if 'exp1' in sys.argv:
	exp = 'exp1'
	w, h = 1280, 1024
elif 'exp2' in sys.argv:
	exp = 'exp2'
	w, h = 1024, 768
elif 'exp3' in sys.argv:
	exp = 'exp3'
	w, h = 1280, 1024
elif 'dummy' in sys.argv:
	exp = None
	w, h = None, None
else:
	raise Exception('You must specify an experiment!')
