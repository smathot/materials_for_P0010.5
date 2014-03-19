#!/usr/bin/env python
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
from analysis import helpers, exp
dm = helpers.getDataMatrix()
dm = helpers.filter(dm, cacheId='filter.%s' % exp)
for i in sys.argv:
	if hasattr(helpers, i):
		retval = getattr(helpers, i)(dm)
		if retval != None:
			dm = retval
