# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;streamer

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasStreamerVersion)#
#echo(__FILEPATH__)#
"""

from dNG.pas.runtime.value_exception import ValueException
from .abstract import Abstract

class AbstractEncapsulated(Abstract):
#
	"""
The abstract streamer encapsulates another streamer for transforming it.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, streamer):
	#
		"""
Constructor __init__(AbstractEncapsulated)

:param streamer: Encapsulated streamer instance

:since: v0.1.00
		"""

		if (not isinstance(streamer, Abstract)): raise ValueException("Given streamer is not supported")

		Abstract.__init__(self)

		self.streamer = streamer
		"""
Encapsulated streamer instance
		"""
	#

	def __getattr__(self, name):
	#
		"""
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Session attribute
:since:  v0.1.00
		"""

		return getattr(self.streamer, name)
	#

	def __next__(self):
	#
		"""
python.org: Return the next item from the container.

:return: (bytes) Response data
:since:  v0.1.00
		"""

		data = self.read()

		if (data is None):
		#
			self.close()
			raise StopIteration()
		#

		return data
	#
#

##j## EOF