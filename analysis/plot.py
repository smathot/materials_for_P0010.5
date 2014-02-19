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
import numpy as np
import analysis
from matplotlib import pyplot as plt

plt.rc('font', family='Arial', size=10)

hi = 8, 24
xxl = 24,12
xl = 24,4
l = 16, 4
r = 8, 4
hi = 6, 8

def new(size=r):

	"""
	Creates a new figure.

	Keyword arguments:
	size	--	The figure size. (default=(12,8))

	"""

	plt.figure(figsize=size)

def save(name, show=False):

	"""
	Saves the current figure to the correct folder, depending on the active
	experiment.

	Arguments:
	name	--	The name for the figure.

	Keyword arguments:
	show	--	Indicates whether the figure should be shown as well.
				(default=False)
	"""

	try:
		os.makedirs('plot/svg/%s' % analysis.exp)
	except:
		pass
	try:
		os.makedirs('plot/png/%s' % analysis.exp)
	except:
		pass
	pathSvg = 'plot/svg/%s/%s.svg' % (analysis.exp, name)
	pathPng = 'plot/png/%s/%s.png' % (analysis.exp, name)
	plt.savefig(pathSvg)
	plt.savefig(pathPng)
	if show:
		plt.show()
	else:
		plt.clf()
