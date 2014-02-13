#-*- coding:utf-8 -*-

import os
import numpy as np
from matplotlib import pyplot as plt

plt.rc('font', family='Arial', size=10)

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
		os.makedirs('plot/svg/%s' % exp)
	except:
		pass
	try:
		os.makedirs('plot/png/%s' % exp)
	except:
		pass
	pathSvg = 'plot/svg/%s/%s.svg' % (exp, name)
	pathPng = 'plot/png/%s/%s.png' % (exp, name)
	plt.savefig(pathSvg)
	plt.savefig(pathPng)
	if show:
		plt.show()
	else:
		plt.clf()
